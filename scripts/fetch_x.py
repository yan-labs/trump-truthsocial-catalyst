#!/usr/bin/env python3
"""Fetch @realDonaldTrump from xreach, with bounded public fallbacks.

The xreach bird connector can return a successful JSON response containing an
old timeline or fail authentication. When that happens, try an independent
RSS-Bridge Atom timeline, then discover public status ids from the X profile
and read their Jina status pages. If all timeline views are stale or blocked,
FxTwitter/VxTwitter can still verify the exact saved status, but that last
check deliberately does not claim that the account is current.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

try:
    from .public_x_profile import fetch_public_posts
except ImportError:  # pragma: no cover - supports direct script execution
    from public_x_profile import fetch_public_posts


ACCOUNT = "realDonaldTrump"
ACCOUNT_ID = "25073877"
PROFILE_READER_URL = "https://r.jina.ai/http://x.com/realDonaldTrump"
STATUS_READER_PREFIX = "https://r.jina.ai/http://x.com/realDonaldTrump/status/"
RSS_BRIDGE_URL = (
    "https://rss-bridge.org/bridge01/?action=display&bridge=Twitter&"
    "context=By+username&u=realDonaldTrump&format=Atom"
)
FXTWITTER_STATUS_PREFIX = "https://api.fxtwitter.com/status/"
VXTWITTER_STATUS_PREFIX = "https://api.vxtwitter.com/realDonaldTrump/status/"
X_URL_PREFIX = "https://x.com/realDonaldTrump/status/"
ATOM_NS = "http://www.w3.org/2005/Atom"
MAX_DIRECT_AGE = timedelta(days=7)


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def parse_time(value: Any) -> datetime | None:
    if not value or not isinstance(value, str):
        return None
    candidate = value.strip()
    try:
        parsed = datetime.fromisoformat(candidate.replace("Z", "+00:00"))
    except ValueError:
        try:
            parsed = parsedate_to_datetime(candidate)
        except (TypeError, ValueError, IndexError):
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def iso_time(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def item_time(item: dict[str, Any]) -> datetime | None:
    return parse_time(item.get("createdAtISO")) or parse_time(item.get("createdAt"))


def sort_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(items, key=lambda item: item_time(item) or datetime.min.replace(tzinfo=timezone.utc), reverse=True)


def load_state(path: Path) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8") as handle:
            value = json.load(handle)
        return value if isinstance(value, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def previous_x_state(state: dict[str, Any]) -> tuple[str, datetime | None]:
    health = state.get("source_health", {})
    x_state = health.get("x_reach", {}) if isinstance(health, dict) else {}
    if not isinstance(x_state, dict):
        x_state = {}
    previous_id = str(x_state.get("latest_returned_id") or state.get("last_tweet_id") or "")
    previous_time = parse_time(x_state.get("latest_returned_time"))
    return previous_id, previous_time


def run_xreach() -> tuple[list[dict[str, Any]], str | None]:
    try:
        result = subprocess.run(
            ["xreach", "tweets", f"@{ACCOUNT}", "-n", "40", "--json"],
            capture_output=True,
            text=True,
            timeout=35,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return [], f"xreach unavailable: {exc.__class__.__name__}"
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip().replace("\n", " ")[:240]
        return [], f"xreach failed ({result.returncode}): {detail}"
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        return [], f"xreach returned invalid JSON: {exc.msg}"
    items = payload.get("items") if isinstance(payload, dict) else payload
    if not isinstance(items, list):
        return [], "xreach JSON did not contain an items list"
    return [item for item in items if isinstance(item, dict) and item.get("id")], None


def fetch_reader(url: str) -> str:
    result = subprocess.run(
        ["curl", "-L", "-sS", "--max-time", "35", "-A", "Mozilla/5.0", url],
        capture_output=True,
        text=True,
        timeout=40,
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip().replace("\n", " ")[:240]
        raise RuntimeError(f"curl failed ({result.returncode}): {detail}")
    return result.stdout


def fetch_json(url: str) -> dict[str, Any]:
    raw = fetch_reader(url)
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON from {url}: {exc.msg}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"JSON from {url} was not an object")
    if payload.get("code") not in (None, 200):
        raise ValueError(f"API returned code {payload.get('code')} from {url}")
    return payload


def profile_status_id(profile_text: str) -> str | None:
    pattern = re.compile(r"https?://(?:x|twitter)\.com/realDonaldTrump/status/(\d+)")
    match = pattern.search(profile_text)
    return match.group(1) if match else None


def clean_html(value: str) -> str:
    value = html.unescape(value or "")
    value = re.sub(r"<br\s*/?>", " ", value, flags=re.IGNORECASE)
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def atom_value(entry: ElementTree.Element, name: str) -> str:
    node = entry.find(f"{{{ATOM_NS}}}{name}")
    return "".join(node.itertext()).strip() if node is not None else ""


def atom_status_id(entry: ElementTree.Element) -> str | None:
    candidates = [atom_value(entry, "id")]
    candidates.extend(
        link.attrib.get("href", "")
        for link in entry.findall(f"{{{ATOM_NS}}}link")
    )
    for candidate in candidates:
        match = re.search(r"https?://(?:x|twitter)\.com/realDonaldTrump/status/(\d+)", candidate)
        if match:
            return match.group(1)
    return None


def rss_bridge_items(feed_text: str) -> list[dict[str, Any]]:
    try:
        root = ElementTree.fromstring(feed_text)
    except ElementTree.ParseError as exc:
        raise ValueError(f"RSS-Bridge returned invalid Atom: {exc}") from exc
    if root.tag.rsplit("}", 1)[-1] != "feed":
        raise ValueError("RSS-Bridge response was not an Atom feed")

    items: list[dict[str, Any]] = []
    for entry in root.findall(f"{{{ATOM_NS}}}entry"):
        status_id = atom_status_id(entry)
        published_time = parse_time(atom_value(entry, "published"))
        if not status_id or not published_time:
            continue
        content = clean_html(atom_value(entry, "content"))
        title = clean_html(atom_value(entry, "title"))
        author_name = clean_html(atom_value(entry, "author"))
        media = [
            link.attrib["href"]
            for link in entry.findall(f"{{{ATOM_NS}}}link")
            if link.attrib.get("rel") == "enclosure" and link.attrib.get("href")
        ]
        items.append(
            {
                "id": status_id,
                "text": content or title,
                "createdAt": published_time.strftime("%a %b %d %H:%M:%S +0000 %Y"),
                "createdAtISO": iso_time(published_time),
                "user": {
                    "restId": ACCOUNT_ID,
                    "screenName": ACCOUNT,
                    "name": "Donald J. Trump",
                },
                "isRetweet": author_name.startswith("RT:"),
                "isQuote": False,
                "isReply": False,
                "media": media,
                "urls": [],
                "sourceUrl": f"{X_URL_PREFIX}{status_id}",
            }
        )
    if not items:
        raise ValueError("RSS-Bridge feed contained no realDonaldTrump status entries")
    return items


def fetch_rss_bridge() -> list[dict[str, Any]]:
    return rss_bridge_items(fetch_reader(RSS_BRIDGE_URL))


def fallback_item(status_id: str, status_text: str) -> dict[str, Any] | None:
    published = re.search(r"^Published Time:\s*(\S+)", status_text, flags=re.MULTILINE)
    published_time = parse_time(published.group(1)) if published else None
    if not published_time:
        return None

    title = re.search(r'^# Donald J\. Trump on X:\s*"(.*)"\s*$', status_text, flags=re.MULTILINE)
    text = title.group(1).strip() if title else ""
    return {
        "id": status_id,
        "text": text,
        "createdAt": published_time.strftime("%a %b %d %H:%M:%S +0000 %Y"),
        "createdAtISO": iso_time(published_time),
        "user": {
            "restId": ACCOUNT_ID,
            "screenName": ACCOUNT,
            "name": "Donald J. Trump",
        },
        "isRetweet": False,
        "isQuote": False,
        "isReply": False,
        "media": [],
        "urls": [],
        "sourceUrl": f"{X_URL_PREFIX}{status_id}",
    }


def api_status_item(
    payload: dict[str, Any], expected_id: str, source: str
) -> dict[str, Any] | None:
    if source == "fxtwitter":
        raw = payload.get("tweet")
        if not isinstance(raw, dict):
            return None
        status_id = str(raw.get("id") or "")
        created_value = raw.get("created_at")
        author = raw.get("author") if isinstance(raw.get("author"), dict) else {}
        text = str(raw.get("text") or "")
        media_raw = raw.get("media") if isinstance(raw.get("media"), dict) else {}
        media = media_raw.get("all") if isinstance(media_raw.get("all"), list) else []
        is_quote = raw.get("quote") is not None
        is_reply = raw.get("replying_to") is not None
    else:
        raw = payload
        status_id = str(raw.get("tweetID") or "")
        created_value = raw.get("date")
        author = {
            "screen_name": raw.get("user_screen_name"),
            "name": raw.get("user_name"),
            "id": ACCOUNT_ID,
        }
        text = str(raw.get("text") or "")
        media = raw.get("mediaURLs") if isinstance(raw.get("mediaURLs"), list) else []
        is_quote = raw.get("qrt") is not None
        is_reply = raw.get("replyingToID") is not None

    created_time = parse_time(created_value)
    screen_name = str(author.get("screen_name") or "")
    if (
        status_id != expected_id
        or not created_time
        or screen_name.lower() != ACCOUNT.lower()
    ):
        return None
    return {
        "id": status_id,
        "text": text,
        "createdAt": created_time.strftime("%a %b %d %H:%M:%S +0000 %Y"),
        "createdAtISO": iso_time(created_time),
        "user": {
            "restId": str(author.get("id") or ACCOUNT_ID),
            "screenName": screen_name or ACCOUNT,
            "name": str(author.get("name") or "Donald J. Trump"),
        },
        "isRetweet": bool(raw.get("retweet") or raw.get("retweetURL")),
        "isQuote": is_quote,
        "isReply": is_reply,
        "media": media,
        "urls": [],
        "sourceUrl": f"{X_URL_PREFIX}{status_id}",
    }


def fetch_exact_status(status_id: str) -> tuple[str, dict[str, Any]]:
    if not status_id.isdigit():
        raise ValueError("saved X status id is not numeric")
    errors: list[str] = []
    for source, prefix in (
        ("fxtwitter", FXTWITTER_STATUS_PREFIX),
        ("vxtwitter", VXTWITTER_STATUS_PREFIX),
    ):
        try:
            item = api_status_item(fetch_json(f"{prefix}{status_id}"), status_id, source)
            if item is None:
                raise ValueError("response did not match the saved account or id")
            return source, item
        except (OSError, RuntimeError, ValueError, TimeoutError) as exc:
            errors.append(f"{source}: {exc}")
    raise RuntimeError("; ".join(errors))


def public_item_for_output(item: dict[str, Any]) -> dict[str, Any]:
    """Keep public fallback rows compatible with the wrapper's legacy shape."""
    output = dict(item)
    author = item.get("author") if isinstance(item.get("author"), dict) else {}
    output["user"] = {
        "restId": str(author.get("id") or ACCOUNT_ID),
        "screenName": str(author.get("screenName") or ACCOUNT),
        "name": str(author.get("name") or "Donald J. Trump"),
    }
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", default="data/sync_state.json", help="sync_state.json path")
    args = parser.parse_args()

    state = load_state(Path(args.state))
    previous_id, previous_time = previous_x_state(state)
    checked_time = now_iso()
    direct_items, direct_error = run_xreach()
    direct_items = sort_items(direct_items)
    direct_latest = direct_items[0] if direct_items else None
    direct_latest_time = item_time(direct_latest or {})
    checked_dt = parse_time(checked_time)
    direct_is_recent = bool(
        direct_latest_time
        and checked_dt
        and timedelta(0) <= checked_dt - direct_latest_time <= MAX_DIRECT_AGE
    )

    direct_is_new = bool(
        direct_latest
        and direct_latest_time
        and direct_is_recent
        and (previous_time is None or direct_latest_time > previous_time)
    )
    if direct_is_new:
        output = {
            "checked_time": checked_time,
            "status": "available",
            "source": "xreach",
            "freshness": "new_posts",
            "items": direct_items,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0

    fallback_error = direct_error or (
        f"xreach latest is not newer than stored {previous_id or 'no prior id'}"
    )
    fallback_errors = [fallback_error]
    timeline_observations: dict[str, Any] = {}

    try:
        rss_items = sort_items(fetch_rss_bridge())
        rss_latest = rss_items[0]
        rss_latest_time = item_time(rss_latest)
        rss_is_new = bool(
            rss_latest_time
            and (previous_time is None or rss_latest_time > previous_time)
        )
        timeline_observations["rss_bridge"] = {
            "status": "new_posts" if rss_is_new else "stale",
            "latest_id": rss_latest.get("id"),
            "latest_time": iso_time(rss_latest_time),
            "item_count": len(rss_items),
        }
        if rss_is_new:
            output = {
                "checked_time": checked_time,
                "status": "available_fallback",
                "source": "rss_bridge",
                "freshness": "new_posts",
                "direct_warning": fallback_error,
                "items": rss_items,
            }
            print(json.dumps(output, ensure_ascii=False, indent=2))
            return 0
    except (OSError, RuntimeError, ValueError, TimeoutError) as exc:
        fallback_errors.append(f"RSS-Bridge timeline failed: {exc}")

    try:
        public_items, public_diagnostic = fetch_public_posts(
            ACCOUNT, ACCOUNT_ID, "Donald J. Trump", limit=12
        )
        public_items = [public_item_for_output(item) for item in sort_items(public_items)]
        public_latest = public_items[0] if public_items else None
        public_latest_time = item_time(public_latest or {})
        public_is_new = bool(
            public_latest_time
            and (previous_time is None or public_latest_time > previous_time)
        )
        timeline_observations["x_public_profile"] = {
            "status": "new_posts" if public_is_new else "stale",
            "latest_id": (public_latest or {}).get("id"),
            "latest_time": iso_time(public_latest_time),
            "item_count": len(public_items),
            "diagnostic": public_diagnostic,
        }
        if public_is_new:
            output = {
                "checked_time": checked_time,
                "status": "available_fallback",
                "source": "x_public_profile+jina_status",
                "freshness": "new_posts",
                "direct_warning": fallback_error,
                "timeline_observations": timeline_observations,
                "items": public_items,
            }
            print(json.dumps(output, ensure_ascii=False, indent=2))
            return 0
    except (OSError, RuntimeError, ValueError, TimeoutError) as exc:
        fallback_errors.append(f"Public X profile/status failed: {exc}")

    try:
        profile_text = fetch_reader(PROFILE_READER_URL)
        status_id = profile_status_id(profile_text)
        if not status_id:
            raise ValueError("Jina profile did not expose a realDonaldTrump status URL")
        status_text = fetch_reader(f"{STATUS_READER_PREFIX}{status_id}")
        item = fallback_item(status_id, status_text)
        if item is None:
            raise ValueError("Jina status page did not expose a published timestamp")
        fallback_time = item_time(item)
        is_new = bool(
            fallback_time
            and (previous_time is None or fallback_time > previous_time)
        )
        output = {
            "checked_time": checked_time,
            "status": "available_fallback" if is_new else "verified_no_new_posts",
            "source": "jina_profile_status",
            "freshness": "new_posts" if is_new else "no_new_posts",
            "direct_warning": fallback_error,
            "timeline_observations": timeline_observations,
            "items": [item],
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0
    except (OSError, RuntimeError, ValueError, TimeoutError) as exc:
        fallback_errors.append(f"Jina profile/status failed: {exc}")

    if previous_id:
        try:
            exact_source, exact_item = fetch_exact_status(previous_id)
            output = {
                "checked_time": checked_time,
                "status": "stale_unverified",
                "source": f"{exact_source}_status",
                "freshness": "exact_status_only",
                "warning": "Known saved X status verified; no public timeline established",
                "direct_warning": fallback_error,
                "fallback_errors": fallback_errors,
                "timeline_observations": timeline_observations,
                "items": [exact_item],
            }
            print(json.dumps(output, ensure_ascii=False, indent=2))
            return 0
        except (OSError, RuntimeError, ValueError, TimeoutError) as exc:
            fallback_errors.append(f"Exact-status APIs failed: {exc}")

    output = {
        "checked_time": checked_time,
        "status": "stale_unverified",
        "source": "xreach",
        "freshness": "unverified",
        "warning": "No public timeline freshness established",
        "fallback_errors": fallback_errors,
        "timeline_observations": timeline_observations,
        "items": direct_items,
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
