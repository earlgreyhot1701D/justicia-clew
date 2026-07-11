Paste this into Kiro after dropping in every doc listed below. Don't walk through it step by step yourself, let Kiro read everything and self-organize.

---

You're building Justicia Clew, a jury-duty information web app. I'm giving you every doc you need before you touch anything.

**Docs provided, read all of them first:**
- `SCOPE_CONTRACT.md` — the frozen product spec. This is law. MUST items get built. STUB items get an interface plus a comment, never a partial build. NEVER items never get built, full stop, no matter how convenient it seems.
- `MOCKUP.html` — the approved, signed-off UI. Port it faithfully, don't redesign it, don't improve on it.
- `ARCHITECTURE.md` — the technical translation of the contract: repo layout, API routes, DigitalOcean Gradient AI integration details, env var names.
- `KIRO_HOOKS.md` — two hook definitions.
- `SUBMISSION_CUTLINE.md` — tonight's actual scope, one real county end to end, everything else genuinely stubbed, not just documented as stub.
- `kb_setup/ingest_notes.md` — real DO endpoints, region, and gotchas already hit tonight.
- `BLOCK0_CHECKLIST.md` — what's already done in the DO console vs what's left locally.
- `README.md` — current stub, keep it honest as you go.

**Do this in order, and use your own judgment on how to organize your context, don't ask me to micromanage it:**

1. Set up persistent context: put `SCOPE_CONTRACT.md` and `ARCHITECTURE.md` into your steering configuration so their rules stay active on every task, not just this first one. Everything else is a regular file you reference when relevant.

2. Create the two hooks described in `KIRO_HOOKS.md`, exactly as specified: a `Pre Task Execution` hook that self-QAs the diff from the task that just finished against scope/security/accessibility/error-state rules before letting the next task start, and a `Manual Trigger` hook, for me to run myself right before Devpost submission, that checks only the six never-cut items. Confirm both exist before writing any application code.

3. Scaffold the repo exactly per `ARCHITECTURE.md`'s layout (Block 0). FastAPI skeleton, CORS locked to `ALLOWED_ORIGIN`, `GET /health`, `.env.example` with the exact variable names from the doc. Real value for tonight: `AGENT_ENDPOINT_SB=https://yznehwdlkq7phehm4rqhowdn.agents.do-ai.run`. I'll paste the access key into my local `.env` myself, it's not in any doc you're reading.

4. Port `MOCKUP.html` into `frontend/index.html`, `app.js`, `styles.css` (Block 1). Mock data stays mock at this step, no API calls yet. Preserve every accessibility detail already in the mockup exactly as built, don't add or remove anything.

5. Per `SUBMISSION_CUTLINE.md`: wire Santa Barbara for real, and only Santa Barbara. Replace the mock `renderChips`/`openAnswer` functions with real calls through `agent_client.py` per `ARCHITECTURE.md`'s sketch, plain `httpx`, `?agent=true` on the URL, SB's own endpoint and key. LA, SF, Fresno, Inyo, and the statewide KB stay fully stubbed tonight, don't build toward them.

6. Self-check against your Block Gate hook's rules after each step above without waiting for me to ask.

Ask me only if something isn't covered by these docs. Otherwise, go.
