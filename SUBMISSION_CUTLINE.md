# Revised cut line — one real slice, stub the rest

*Your contract's cut line was reactive: "if behind, Block 4 shrinks to SB-only, then Block 5 shrinks to UI strings only." Given the 2pm deadline plus a 2-hour tinker window after, I'd flip that from a fallback into the plan from the start. This is a bigger cut than the contract currently says, flagging it as a deliberate call for you to confirm, not something I'm quietly deciding for you.*

## Ship by 2pm (Devpost submission)

1. **Frontend, fully ported** (Block 1) — you're most of the way there already, the mockup is the real UI.
2. **One real vertical slice: Santa Barbara only.** Collapse Blocks 2 and 3 into "SB county KB + agent, wired end to end, mock data gone for SB." This is the one county that has to actually work against real DO infrastructure.
3. **The six never-cut items, working on the real SB slice, not the mock:** refusal behavior with real phone number, source attribution, trust banner + "not legal advice" footer, error states (no blank screens), accessibility baseline, independence disclaimer. Hook 2 above is the check for exactly this.
4. **Devpost write-up + whatever media the submission form asks for** (screenshots, a short demo clip, description). I haven't confirmed this event's exact Devpost form fields, since we already found one wrong hackathon page earlier, so check the actual form directly rather than trust anything I'd guess here.

## Stub now, tinker after 2pm

- **LA, SF, Fresno, Inyo** — full stub, not "shrink to," genuinely push past submission. Statewide layer still answers general questions for every county per the contract, so this isn't a broken promise, it's the documented STUB path.
- **Spanish beyond the toggle UI already in the mockup** — real grounded Spanish answers wait for the tinker window.
- **Rate limiting, KB refresh cron, SMS, feedback mechanism** — already STUB/future-growth per your contract, unchanged.
- **Recorded backup demo run, judge Q&A sheet** — nice to have if the tinker window allows, not a submission blocker.

## Why this is worth doing on purpose instead of waiting to fall behind

Your stretch goal #2 is literally "live county add, timed, on stage or at the table." If your 2-hour tinker window includes any judge Q&A or table time after 2pm, adding a 6th county live in front of a judge using the exact one-command pipeline in `kb_setup/ingest_notes.md` is a stronger demo beat than having quietly pre-built 5 counties nobody watches you build. Starting from "1 real county, rest honestly stubbed" sets that beat up instead of accidentally spending your last hours polishing counties no one sees you add.

Say the word if you'd rather keep the original reactive cut line instead, this is a bigger deviation from the frozen contract than "shrink Block 4," so it's your call to make, not mine to assume.
