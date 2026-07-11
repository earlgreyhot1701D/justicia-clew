Paste this to Kiro. Inspection first, then a small local test, then push, don't skip ahead.

---

Claude made four direct edits to the repo just now, outside this session, to address findings from the adversarial QA pass. Read all four files fresh from disk and confirm what's actually there before anything else:

1. `backend/services/rate_limit.py` — should now be a real in-memory sliding-window limiter, 10 requests/minute per client ID, not the old `pass`-only stub. Paste the actual current content.

2. `backend/routes/ask.py` — should now import `Request` from fastapi and `check_rate_limit` from `rate_limit`, take a `request: Request` parameter, check the rate limit before the county lookup and return a 429 if exceeded, and log agent errors with `print(f"agent_client error: {e}")` in the except block. Paste the actual current content.

3. `frontend/index.html` — the `#es` language toggle button should now have `disabled`, `aria-disabled="true"`, and a `title` attribute explaining Spanish isn't fully implemented yet. The four screen headings (`#title`, `#loadingTitle`, `#questionTitle`, `#asked`) should each have `tabindex="-1"`. Confirm these are actually present.

4. `frontend/app.js` — the `show()` function should now prefer `h1,h2` over other focusable elements when picking what to focus after a screen transition. Paste the actual current function.

Once you've confirmed all four match, do one local test specific to the new rate limiter (this is a one-time functional check, not a load test, so it's fine despite the earlier "no bulk traffic" instruction for the QA pass): with uvicorn running locally, send 11 sequential requests to `/api/ask` with the same question and confirm the 11th one comes back with a `429` and the "Too many questions too quickly" message, while the first 10 succeed normally. Then run `test_sb_agent.py` once as usual to confirm nothing else broke.

If all of that checks out, commit and push:
```
git add .
git commit -m "add real rate limiting, fix focus-on-heading a11y bug, disable Spanish toggle"
git push
```
Report back the actual file contents you saw, the rate-limit test result, and whether the push succeeded.
