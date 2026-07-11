Paste this to Kiro now, before doing anything else.

---

Heads up before we continue: I made direct edits to four files myself just now, outside of this session, because the last round of fixes you reported as done weren't actually landing on disk. Reload these four files from disk before touching any of them, don't rely on whatever version you have cached from earlier in this session, or we'll end up overwriting real work again:

1. `data/faq_chips.json` — now has exactly 7 chips: chip-1, chip-2, chip-3, chip-5, chip-6, chip-7, chip-8. Chip-4 (pay), chip-9 (phone), chip-10 (medical condition) were removed, no grounded content for those yet.

2. `backend/models/schemas.py` — `RefusalResponse` now has an `hours` field (`hours: str = ""`), in addition to `refusal`, `message`, `phone`.

3. `backend/services/agent_client.py` — `_get_jury_phone()` is corrected to `"SB": "(805) 882-4530"` with `"NOT_VERIFIED_STUB"` for LA/SF/Fresno/Inyo. A new `_get_jury_hours()` function was added right after it, returning office hours paired with the phone number. `refusal_signals` now also includes `"i can't give"`, `"i cannot give"`, `"i can't tell you"`, `"i cannot tell you"`. The refusal dict returned from `_parse_agent_response()` now includes `"hours": hours` alongside `"phone": phone`.

4. `frontend/app.js` — three changes: a new `resetQuestionInput()` function clears the question box and disables the ask button, called from the `homeBtn`, `.toLanding`, and `answerBack` click handlers so the input never carries over between sessions. A new `renderParagraphs(container, text)` helper splits response text on newlines and appends one `<p>` per line (still `textContent` only, never `innerHTML`), used in place of single flat paragraphs for both the answer and refusal message. The refusal block and the network-error fallback block both now render an `hours` line under the phone link.

Read all four files now and confirm back to me what you actually see in each, the real current content, not a summary. Once that's confirmed, restart uvicorn locally and re-run `test_sb_agent.py` to make sure everything still passes with these changes in place, then we'll decide what's next together.
