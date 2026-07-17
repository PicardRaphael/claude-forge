"""Monotonic, sortable ULID-compatible identifier generation."""

from __future__ import annotations

import os
import time


_ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"


def _encode(value: int, length: int) -> str:
    chars = []
    for _ in range(length):
        chars.append(_ALPHABET[value & 31])
        value >>= 5
    return "".join(reversed(chars))


class UlidGenerator:
    def new(self) -> str:
        timestamp_ms = int(time.time_ns() // 1_000_000)
        randomness = int.from_bytes(os.urandom(10), "big")
        return _encode(timestamp_ms, 10) + _encode(randomness, 16)
