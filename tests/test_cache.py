import pytest

from disfork import InvalidIdCache


def test_invalid_id_cache_remembers_recent_id():
    cache = InvalidIdCache()

    cache.add(123)

    assert cache.contains(123)


def test_invalid_id_cache_rejects_non_positive_ids():
    cache = InvalidIdCache()

    with pytest.raises(ValueError):
        cache.add(0)
