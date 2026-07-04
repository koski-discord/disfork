# disfork

`disfork` is a small Discord bot library built around the parts of `discord.py`
that tend to matter once a bot starts getting real traffic: caching, rate limits,
and avoiding wasteful API calls.

For now, it stays close to `discord.py` instead of trying to replace the whole
thing on day one. The plan is to keep the familiar feel, then add the pieces I
wish were easier to control in bigger bots.

## What it does

- remembers Discord IDs that already failed lookup, so the bot does not keep
  asking for the same bad data over and over
- gives you simple rate-limit buckets for actions you want to keep under control
- keeps the code small enough to read without digging through a huge framework
- leaves room to become a fuller fork later, if that ends up being worth it

## Install

```bash
pip install -e .
```

## Example

```python
from disfork import InvalidIdCache, RateLimitBucket

invalid_ids = InvalidIdCache(max_size=10_000, ttl_seconds=3600)

if invalid_ids.contains(123):
    print("Skip the lookup; this ID failed recently.")

bucket = RateLimitBucket(limit=5, window_seconds=10)

if bucket.allow("send:welcome-message"):
    print("send it")
```

## Notes

This is early and intentionally plain. I would rather keep the first versions
boring and easy to inspect than pretend it is a finished Discord framework.

Things I want to add next:

- optional `discord.Client` and `commands.Bot` helpers
- counters for cache hits, misses, and blocked actions
- retry helpers for Discord API edge cases
- a clearer path if this becomes a real `discord.py` fork
