from __future__ import annotations

from collections import OrderedDict
from time import monotonic


class InvalidIdCache:
    """TTL cache for Discord IDs that recently failed validation or lookup."""

    def __init__(self, max_size: int = 50_000, ttl_seconds: float = 3600) -> None:
        if max_size < 1:
            raise ValueError("max_size must be at least 1")
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be greater than 0")

        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self._entries: OrderedDict[int, float] = OrderedDict()

    def add(self, discord_id: int) -> None:
        self._prune_expired()
        normalized_id = self._normalize(discord_id)
        self._entries[normalized_id] = monotonic() + self.ttl_seconds
        self._entries.move_to_end(normalized_id)

        while len(self._entries) > self.max_size:
            self._entries.popitem(last=False)

    def contains(self, discord_id: int) -> bool:
        normalized_id = self._normalize(discord_id)
        expires_at = self._entries.get(normalized_id)

        if expires_at is None:
            return False
        if expires_at <= monotonic():
            del self._entries[normalized_id]
            return False

        self._entries.move_to_end(normalized_id)
        return True

    def discard(self, discord_id: int) -> None:
        self._entries.pop(self._normalize(discord_id), None)

    def clear(self) -> None:
        self._entries.clear()

    def __len__(self) -> int:
        self._prune_expired()
        return len(self._entries)

    @staticmethod
    def _normalize(discord_id: int) -> int:
        try:
            normalized_id = int(discord_id)
        except (TypeError, ValueError) as exc:
            raise ValueError("discord_id must be an integer-like value") from exc

        if normalized_id <= 0:
            raise ValueError("discord_id must be positive")
        return normalized_id

    def _prune_expired(self) -> None:
        now = monotonic()
        expired_ids = [
            discord_id
            for discord_id, expires_at in self._entries.items()
            if expires_at <= now
        ]

        for discord_id in expired_ids:
            del self._entries[discord_id]
