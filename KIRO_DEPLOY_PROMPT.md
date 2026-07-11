Paste this to Kiro now, before touching the DigitalOcean console.

---

Three things to fix before we deploy. I checked the actual files, not the summary from last session, and found the first two didn't actually land.

1. `backend/services/agent_client.py` still has the old wrong Santa Barbara phone number (`(805) 882-4532`) in `_get_jury_phone()`, and still has hardcoded real-looking phone numbers for LA, SF, Fresno, and Inyo. The earlier fix prompt asked for South County `(805) 882-4530` as the default SB number, and `"NOT_VERIFIED_STUB"` in place of the LA/SF/Fresno/Inyo numbers. Please make those two edits for real this time, then paste me the actual content of the `_get_jury_phone()` function afterward so I can confirm it directly instead of taking a summary of it.

2. Same file — the refusal-detection keyword list in `_parse_agent_response()` still doesn't include phrases like "i can't give legal advice" or "i cannot give legal advice." If that heuristic tightening was made in a prior session, it isn't in this file. Add it back and confirm by pasting the updated `refusal_signals` list.

3. `backend/main.py` has no static file serving. Only `/api/*` and `/health` are registered, so `/` currently 404s even though `frontend/app.js` assumes same-origin (`API_BASE = ''`). Add this after the existing `app.include_router(...)` calls, so `/api` routes keep priority over the catch-all:
   ```python
   from fastapi.staticfiles import StaticFiles
   app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
   ```

After all three: restart uvicorn, open `http://localhost:8080/` in an actual browser tab (not just hitting `/health` with curl) and confirm the real frontend loads and can complete a full chip-tap round trip. Then re-run `test_sb_agent.py` and paste the full output, especially the two refusal cases.

Once that's confirmed, also do this repo setup for deploy:
- Add a `Procfile` at the repo root: `web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
- Confirm there's no `.git` folder yet (there wasn't as of this check). Run `git init`, `git add .`, and make a first commit. Don't push yet, I'll create the GitHub repo and give you the remote URL first.
