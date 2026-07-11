"""STUB: Rate limiting interface.

Implementation note: When filled in (Block 3 if time allows), use a simple
in-memory sliding window per IP. FastAPI dependency injection pattern:
    async def check_rate_limit(request: Request) -> None:
        # raise HTTPException(429) if over limit

For production: replace with Redis-backed limiter or DO App Platform's
built-in rate limiting if available.
"""


async def check_rate_limit(request) -> None:
    """STUB: Rate limit check. Currently a no-op pass-through."""
    # TODO: Implement sliding window rate limiting per IP
    # Suggested limits: 30 requests/minute per IP for /api/ask,
    # 60 requests/minute for /api/chips
    pass
