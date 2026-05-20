"""
X-Read -- Read-only X/Twitter reader for forge-brain capitalization.

Defensive wrapper around twitter-api-client.
Only 3 read functions exposed via CLI. No POST/LIKE/FOLLOW anywhere in this file.

Architectural note:
- Scraper: read public content (no auth required for most, cookies improve rate limits)
- Account: authenticated session -- used ONLY for home_latest_timeline
  The Account class CAN post/like/follow, but this file never calls those methods.
  The CLI entrypoint only routes to: tweet | timeline | user | check

Cookies file (claude-forge/.claude/secrets/x-cookies.json):
{
  "ct0": "...",
  "auth_token": "..."
}

Modes:
- tweet <url>   : raw API JSON response
- pretty <url>  : clean dict {author, text, media+local_path, urls, stats}
                  Images auto-downloaded to .claude/skills/x-read/downloads/
- timeline [N]  : home feed
- user <h> [N]  : tweets from @handle
- check         : verify cookies + package
"""
import json
import sys
from pathlib import Path

# Resolve cookies relative to this file: skills/x-read/reader.py -> .claude/secrets/x-cookies.json
# This keeps cookies inside claude-forge (gitignored) instead of ~/.claude/
COOKIES_PATH = Path(__file__).resolve().parent.parent.parent / "secrets" / "x-cookies.json"


def _load_cookies() -> dict:
    if not COOKIES_PATH.exists():
        print(f"ERROR: cookies not found at {COOKIES_PATH}", file=sys.stderr)
        print("Setup guide: .claude/skills/x-read/references/cookie-setup.md", file=sys.stderr)
        sys.exit(2)
    try:
        return json.loads(COOKIES_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERROR: invalid JSON in cookies file: {e}", file=sys.stderr)
        sys.exit(2)


def _check():
    """Check prerequisites without making any API call."""
    if not COOKIES_PATH.exists():
        print(f"ERROR: cookies not found at {COOKIES_PATH}", file=sys.stderr)
        print("Setup guide: .claude/skills/x-read/references/cookie-setup.md", file=sys.stderr)
        sys.exit(2)
    try:
        import twitter  # noqa: F401
    except ImportError:
        print("ERROR: pip install twitter-api-client", file=sys.stderr)
        sys.exit(1)
    print("OK: cookies found and twitter-api-client installed")


def _require_package():
    """Fail early with a clear message if twitter-api-client is missing."""
    try:
        import twitter  # noqa: F401
    except ImportError:
        print("ERROR: twitter-api-client not installed. Run:", file=sys.stderr)
        print('  pip install "twitter-api-client>=0.10.20,<0.12.0"', file=sys.stderr)
        sys.exit(1)


def read_tweet(url: str) -> dict:
    """Read one tweet by URL. Returns raw API response dict."""
    _require_package()
    from twitter.scraper import Scraper

    tweet_id_str = url.rstrip("/").split("/")[-1].split("?")[0]
    try:
        tweet_id = int(tweet_id_str)
    except ValueError:
        print(f"ERROR: cannot extract tweet ID from URL: {url}", file=sys.stderr)
        sys.exit(1)

    cookies = _load_cookies()
    s = Scraper(cookies=cookies, pbar=False, save=False)
    results = s.tweets_by_ids([tweet_id])
    return results[0] if results else {}


def read_timeline(limit: int = 20) -> list:
    """Read home timeline (authenticated). Read-only wrapper around Account.home_latest_timeline.

    Note: home_latest_timeline is on Account (not Scraper). Account is instantiated
    with cookies only -- no username/password. Write methods (tweet/like/follow)
    are available on Account but are never called from this file.
    """
    _require_package()
    from twitter.account import Account

    cookies = _load_cookies()
    acct = Account(cookies=cookies, pbar=False, save=False)

    if hasattr(acct, "home_latest_timeline"):
        return acct.home_latest_timeline(limit=limit)
    elif hasattr(acct, "home_timeline"):
        return acct.home_timeline(limit=limit)
    else:
        print(
            "ERROR: home_latest_timeline not available on Account -- "
            "check twitter-api-client version (need >=0.10.20)",
            file=sys.stderr,
        )
        sys.exit(3)


def read_user_tweets(handle: str, limit: int = 10) -> list:
    """Read public tweets from a user handle (no @ prefix needed)."""
    _require_package()
    from twitter.scraper import Scraper

    handle = handle.lstrip("@")
    cookies = _load_cookies()
    s = Scraper(cookies=cookies, pbar=False, save=False)

    users = s.users_by_login([handle])
    if not users:
        print(f"ERROR: user not found: @{handle}", file=sys.stderr)
        sys.exit(1)

    # Extract user ID -- structure varies by package version, try common paths
    user = users[0]
    user_id = None
    try:
        user_id = int(user["data"]["user"]["result"]["rest_id"])
    except (KeyError, TypeError, ValueError):
        try:
            user_id = int(user.get("rest_id") or user.get("id") or user.get("id_str", 0))
        except (TypeError, ValueError):
            print(
                f"ERROR: cannot extract user_id from response. "
                f"First 200 chars: {json.dumps(user, default=str)[:200]}",
                file=sys.stderr,
            )
            sys.exit(1)

    tweets = s.tweets([user_id], limit=limit)
    return tweets


def _extract_tweet(t: dict) -> dict:
    """Extract clean tweet data: author, text, urls expanded, media downloaded."""
    legacy = t.get("legacy", {})
    user = t.get("core", {}).get("user_results", {}).get("result", {}).get("legacy", {})

    # Expand URLs (replace t.co with real URLs in text)
    text = legacy.get("full_text", "")
    urls = legacy.get("entities", {}).get("urls", [])
    for u in urls:
        if u.get("url") and u.get("expanded_url"):
            text = text.replace(u["url"], u["expanded_url"])

    # Media (photos/videos)
    media = []
    for m in legacy.get("extended_entities", {}).get("media", []):
        item = {"type": m.get("type"), "url": m.get("media_url_https")}
        if m.get("video_info"):
            variants = sorted(
                [v for v in m["video_info"].get("variants", []) if v.get("bitrate")],
                key=lambda v: v.get("bitrate", 0),
                reverse=True,
            )
            if variants:
                item["video_url"] = variants[0]["url"]
        media.append(item)

    return {
        "author": "@" + user.get("screen_name", "?"),
        "name": user.get("name"),
        "date": legacy.get("created_at"),
        "text": text,
        "media": media,
        "external_urls": [u.get("expanded_url") for u in urls if u.get("expanded_url")],
        "stats": {
            "likes": legacy.get("favorite_count"),
            "retweets": legacy.get("retweet_count"),
            "replies": legacy.get("reply_count"),
            "views": t.get("views", {}).get("count"),
        },
    }


def _download_media(url: str, dest_dir: Path) -> Path | None:
    """Download a media URL to dest_dir. Returns local path or None on error."""
    try:
        import httpx
    except ImportError:
        return None
    dest_dir.mkdir(parents=True, exist_ok=True)
    filename = url.rstrip("/").split("/")[-1].split("?")[0]
    if "." not in filename:
        filename += ".jpg"
    local = dest_dir / filename
    if local.exists():
        return local
    try:
        r = httpx.get(url, timeout=15, follow_redirects=True)
        r.raise_for_status()
        local.write_bytes(r.content)
        return local
    except Exception as e:
        print(f"WARNING: failed to download {url}: {e}", file=sys.stderr)
        return None


def pretty_tweet(url: str, download: bool = True) -> dict:
    """Read tweet and return clean dict with downloaded media paths."""
    raw = read_tweet(url)
    if not raw or "data" not in raw:
        print("ERROR: empty response", file=sys.stderr)
        sys.exit(1)
    t = raw["data"]["tweetResult"][0]["result"]
    if t.get("__typename") == "TweetUnavailable":
        return {"error": "Tweet unavailable (deleted, private, or suspended)", "raw": t}
    extracted = _extract_tweet(t)
    if download and extracted["media"]:
        media_dir = Path(__file__).resolve().parent / "downloads"
        for m in extracted["media"]:
            local = _download_media(m["url"], media_dir)
            if local:
                m["local_path"] = str(local)
    return extracted


def main():
    if len(sys.argv) < 2:
        print("Usage: reader.py {tweet|pretty|timeline|user|check} [args]", file=sys.stderr)
        print("  tweet <url>            -- raw API response (JSON)", file=sys.stderr)
        print("  pretty <url>           -- clean extract + download media locally", file=sys.stderr)
        print("  timeline [N]           -- read N home feed tweets (default 20)", file=sys.stderr)
        print("  user <handle> [N]      -- read N tweets from @handle (default 10)", file=sys.stderr)
        print("  check                  -- verify cookies + package (no API call)", file=sys.stderr)
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "check":
        _check()
        return

    if mode == "tweet":
        if len(sys.argv) < 3:
            print("ERROR: tweet mode requires a URL argument", file=sys.stderr)
            sys.exit(1)
        result = read_tweet(sys.argv[2])

    elif mode == "pretty":
        if len(sys.argv) < 3:
            print("ERROR: pretty mode requires a URL argument", file=sys.stderr)
            sys.exit(1)
        result = pretty_tweet(sys.argv[2])

    elif mode == "timeline":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 20
        result = read_timeline(limit)

    elif mode == "user":
        if len(sys.argv) < 3:
            print("ERROR: user mode requires a handle argument", file=sys.stderr)
            sys.exit(1)
        handle = sys.argv[2]
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        result = read_user_tweets(handle, limit)

    else:
        print(f"ERROR: unknown mode '{mode}'. Valid: tweet | timeline | user | check", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
