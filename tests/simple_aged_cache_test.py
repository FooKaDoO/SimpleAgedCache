import pytest
from datetime import datetime, timedelta
from cache import SimpleAgedCache


class MockClock:
    def __init__(self):
        self.offset_duration = timedelta(0)

    def now(self):
        return datetime.utcnow() + self.offset_duration

    def offset(self, offset):
        self.offset_duration = offset


@pytest.fixture
def empty_cache():
    return SimpleAgedCache()


@pytest.fixture
def nonempty_cache():
    cache = SimpleAgedCache()
    cache.put("aKey", "aValue", 2000)
    cache.put("anotherKey", "anotherValue", 4000)
    return cache


def test_is_empty(empty_cache, nonempty_cache):
    assert empty_cache.is_empty()
    assert not nonempty_cache.is_empty()


def test_size(empty_cache, nonempty_cache):
    assert empty_cache.size() == 0
    assert nonempty_cache.size() == 2


def test_get(empty_cache, nonempty_cache):
    assert empty_cache.get("aKey") is None
    assert nonempty_cache.get("aKey") == "aValue"
    assert nonempty_cache.get("anotherKey") == "anotherValue"


def test_get_expired():
    clock = MockClock()
    expired = SimpleAgedCache(clock.now)
    expired.put("aKey", "aValue", 2000)
    expired.put("anotherKey", "anotherValue", 4000)

    clock.offset(timedelta(milliseconds=3000))

    assert expired.size() == 1
    assert expired.get("anotherKey") == "anotherValue"
