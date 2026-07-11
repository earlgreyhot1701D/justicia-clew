"""Rate limiting for /api/ask, the only route that calls the metered DO agent.

Simple in-memory sliding window per client IP. Single-process, resets on
restart, not distributed. That's an intentional tradeoff for a short-lived
hackathon demo, not long-term production, a Redis-backed limiter would be
the real fix if this app lived past submission day.
"""

import time
from collections import defaultdict

_WINDOW_SECONDS = 60
_MAX_REQUESTS = 10
_hits = defaultdict(list)


def check_rate_limit(client_id: str) -> bool:
    """Return True if this client is within the allowed rate, False if it
    should be blocked. Caller is responsible for raising the HTTP error."""
    now = time.time()
    window_start = now - _WINDOW_SECONDS
    hits = _hits[client_id]
    while hits and hits[0] < window_start:
        hits.pop(0)
    if len(hits) >= _MAX_REQUESTS:
        return False
    hits.append(now)
    return True
