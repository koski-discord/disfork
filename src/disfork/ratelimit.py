from __future__ import annotations

from collections import defaultdict, deque
from time import monotonic
from typing import Deque


class RateLimitBucket:
    """Sliding-window rate limiter keyed by action name or Discord route."""

    def __init__(self, limit: int, window_seconds: float) -> None:
        if limit < 1:
            raise ValueError("limit must be at least 1")
        if window_seconds <= 0:
            raise ValueError("window_seconds must be greater than 0")

        self.limit = limit
        self.window_seconds = window_seconds
        self._hits: defaultdict[str, Deque[float]] = defaultdict(deque)

    def allow(self, key: str = "default") -> bool:
        hits = self._hits[key]
        self._prune(hits)

        if len(hits) >= self.limit:
            return False

        hits.append(monotonic())
        return True

    def remaining(self, key: str = "default") -> int:
        hits = self._hits[key]
        self._prune(hits)
        return max(0, self.limit - len(hits))

    def reset_after(self, key: str = "default") -> float:
        hits = self._hits[key]
        self._prune(hits)

        if len(hits) < self.limit:
            return 0

        return max(0, self.window_seconds - (monotonic() - hits[0]))

    def clear(self, key: str | None = None) -> None:
        if key is None:
            self._hits.clear()
            return

        self._hits.pop(key, None)

    def _prune(self, hits: Deque[float]) -> None:
        cutoff = monotonic() - self.window_seconds
        while hits and hits[0] <= cutoff:
            hits.popleft()
