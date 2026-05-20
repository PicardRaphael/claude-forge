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


def main():
    if len(sys.argv) < 2:
        print("Usage: reader.py {tweet|timeline|user|check} [args]", file=sys.stderr)
        print("  tweet <url>            -- read one tweet by URL", file=sys.stderr)
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
