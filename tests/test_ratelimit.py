from disfork import RateLimitBucket


def test_rate_limit_bucket_blocks_after_limit():
    bucket = RateLimitBucket(limit=2, window_seconds=60)

    assert bucket.allow("lookup")
    assert bucket.allow("lookup")
    assert not bucket.allow("lookup")


def test_rate_limit_bucket_tracks_keys_separately():
    bucket = RateLimitBucket(limit=1, window_seconds=60)

    assert bucket.allow("one")
    assert bucket.allow("two")
    assert not bucket.allow("one")
