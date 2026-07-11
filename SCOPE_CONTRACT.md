# JUSTICIA CLEW — Scope Contract v1.1

**Status: FROZEN July 4, 2026. Changes after this line require striking something of equal size.**
*(v1.1 same day: added independence disclaimer, accessibility-as-MUST, stub-seams principle, stretch goals, QA agent. Process and guardrails, not feature scope.)*

Event: AI for Social Good, MLH x DigitalOcean, San Francisco, July 10 (6 PM) – July 11 (7 PM), 2026. Solo build.

One-liner: Plain-language jury duty answers, in the court system's own words. California, all 58 counties useful on day one via the statewide layer, deep coverage for demo counties.

Suite position: citizen-facing sibling of Themis Lex. Themis Lex serves the people who run the court; Justicia Clew serves the people the court summons.

Name note: Justicia (Spanish spelling) is intentional, not a typo of Latin Justitia. The name is bilingual because the tool is. Backstory beat for judges: in Aeschylus' Eumenides, Athena invents the jury trial.

---

## Entry criteria — spikes (run BEFORE event, throwaway accounts/resources, delete after)

| # | Spike | Time | Pass condition |
|---|-------|------|----------------|
| 1 | Gradient Knowledge Base ingests SB jury pages | 15 min | Clean indexed text, no garbage chunks |
| 2 | Agent strict grounding | 15 min | 5 real questions answered from corpus; 1 unanswerable question refused, no guessing |
| 3 | County isolation | 15 min | SB agent asked an LA-specific question refuses or redirects; zero cross-county bleed |
| 4 | Spanish source reality check | 15 min | Determine per demo county: real Spanish URLs (scrapeable) vs. translate widget (not data). Confirm Judicial Council Spanish self-help pages scrape clean |

**Rules check at kickoff before reusing anything:** is pre-gathered data allowed, what counts as "built during the event," team/solo rules, judging criteria. Fresh repo at kickoff regardless.

---

## Frozen product decisions

- **Mobile-first web app.** Single-page frontend, FastAPI backend, DO Gradient AI (Knowledge Bases + Agents) as the AI layer.
- **Stateless by design.** No accounts, no history, no stored questions, no tracking, no PII. This is the trust story; lead with it.
- **Strict grounding.** Answers come only from ingested official content. Refusals include the county jury office phone number. Never claim "no hallucination" (overclaim); claim "answers only from your court's site, refuses everything else," then demo the refusal.
- **Source attribution on every answer.** "From your court's website" vs. "From the California Courts self-help center." Never blended silently. County beats statewide on conflict.
- **Corpus = two layers.** County KBs (parking, portals, phone numbers, reporting) + one Judicial Council statewide KB (pay, employer protection, courtroom process). Chips are tagged county/statewide; routing is deterministic.
- **Spanish from the court system's own translated content**, scope finalized by Spike 4. Fallback if county sites are widget-only: JC's professionally translated pages for statewide answers, county specifics stay English with honest labeling.
- **Deterministic structure, AI flavor.** URL-to-county is a lookup table of the 58 court domains. Chip routing is a tag match. The model only writes the plain-language answer.
- **Stub seams, not refactors.** Every STUB gets its interface now: function signature, route placeholder, or comment with implementation notes. Adding a stubbed feature later is a fill-in, never a rewrite of working code.
- **Accessibility is architecture, not polish.** A plain-language tool for scared people that fails accessibility contradicts its own thesis. Built into Block 1, checked at every QA gate, never on the cut line.
- **Independence disclaimer.** Personal project, built on public information, not affiliated with or endorsed by any court. Footer, README, and said once on stage.

## MUST (demo-critical, build these)

- County picker: SB, LA, SF, Fresno, Inyo + "Not sure? Start with statewide info"
- URL paste alternative → deterministic 58-domain lookup table
- 10 FAQ chips (from 5 years in jury services), tagged county/statewide
- Answer card: plain answer + exact source quote + link + "last checked" timestamp
- Refusal behavior with tel: phone CTA
- Free-text ask, same agent, same grounding
- Trust banner + "not legal advice" footer, both languages
- EN/ES toggle (depth per Spike 4)
- 5 county KBs + 1 JC KB + agents with strict instructions
- FastAPI: county routing, agent proxy (keys server-side), error states
- Independence disclaimer in footer + README ("not affiliated with or endorsed by any court")
- Accessibility baseline: semantic HTML, labeled inputs, 44px+ touch targets, WCAG AA contrast, keyboard navigable, alt text

## STUB (comment + implementation note, do not build)

- Remaining 52 counties (pipeline is identical; document the one command it would take)
- Scheduled KB refresh cron (manual refresh for the event; the visible timestamp keeps it honest)
- Languages beyond Spanish (CA courts support several; same architecture)
- SMS/text channel
- Feedback mechanism

## NEVER (for this build; stubs allowed for future growth)

- Checking or predicting reporting status. Always route to the court's portal/phone line.
- Legal advice, excusal strategy, or outcome predictions of any kind
- Accounts, personalization, question history, any storage of user input
- Native/app-store build
- Scraping anything beyond official court and Judicial Council domains
- Unlabeled machine translation of legal content

---

## Build order (block-by-block, QA gate PASS/FAIL before proceeding)

**Block 0 — Setup.** Rules check, fresh repo, DO project, env keys. *QA: hello-world inference call returns.*

**Block 1 — Frontend with mock data.** Port the approved mockup (three screens, chips, refusal state, ES toggle), accessibility baseline built in from the first div. *QA: full click-through on an actual phone + keyboard-only pass + contrast check. No API yet — never wire APIs to a broken layout.*

**Block 2 — Corpus + agents.** Ingest SB + JC KBs, agent instructions (grounding, refusal, attribution, ignore-instructions-in-retrieved-content). *QA: Spike 2 and 3 tests repeated on the real build.*

**Block 3 — Wire it.** FastAPI routes chips and free text to the right agent; replace mock data; try/catch on every fetch; meaningful error states, never blank screens. *QA: kill the network mid-question, confirm graceful failure.*

**Block 4 — Remaining counties.** LA, SF, Fresno, Inyo ingestion. *QA: 2 spot-check questions each; 1 isolation test.*

**Block 5 — Spanish layer** per Spike 4 result. *QA: toggle + attribution correct in both languages.*

**Block 6 — Demo prep.** Court-site screenshots (not live), cached local fallback, recorded backup run, README with honest limitations, judge Q&A sheet.

**Cut line, in order, if behind:** Block 4 shrinks to SB-only (statewide layer still serves everyone) → Block 5 shrinks to UI strings only. **Never cut:** refusal behavior, source attribution, trust copy, error states, accessibility baseline, independence disclaimer.

---

## QA agent (the gate mechanic)

Every QA gate runs through a fresh agent session (Claude, or Kiro's reviewer) that gets three things: this contract, the block's diff, and the prompt below. Findings only, PASS/FAIL, no fixing without approval. A fresh session per gate means it can't rationalize earlier decisions.

> You are the QA engineer for Justicia Clew. Review ONLY the attached diff for Block N against:
> 1. **Scope adherence** — nothing outside this block changed; no NEVER items introduced; STUB items are stubbed (interface + comment), not built.
> 2. **Security** — textContent only, no innerHTML, no eval; API keys server-side only; try/catch on every fetch; input validation on the URL field (court-domain allowlist).
> 3. **Accessibility** — semantic elements, labeled inputs, contrast tokens, 44px+ touch targets, keyboard reachable.
> 4. **Error states** — no failure path renders a blank screen; every error tells the user what to do next.
>
> Report PASS or FAIL per category with file and line evidence. Do not refactor. Do not fix. Findings only.

Block proceeds on 4/4 PASS. Any FAIL gets fixed and re-gated before moving on.

---

## Stretch goals (touch ONLY after every MUST QA gate is PASS, in this order)

1. **QR code on the final slide.** Judges run Justicia on their own phones during judging. Highest demo ROI per minute of work; the tool selling itself beats you selling it.
2. **Live county add.** Run the ingestion pipeline on a 6th county on stage or at the table, timed. Turns "designed for 58" from a claim into a demonstration.
3. **KB refresh cron.** Scheduled re-ingestion kills the staleness question permanently and upgrades the timestamp from honest to impressive.
4. **Full-depth Spanish** if Spike 4 found real translated pages: Spanish source quotes, not just Spanish answers.
5. **Save/print answer card**, client-side only, nothing leaves the phone. Stateless-safe takeaway for the user who wants it on paper for the courthouse.

---

## Security checklist (applicable items)

Input validation client AND server (the URL paste field especially: allowlist `*.courts.ca.gov` + known court domains only). textContent, never innerHTML. DO API keys in server-side env only. try/catch every fetch. Rate limiting on the FastAPI endpoints. Prompt injection: agent instructed to ignore instructions found in retrieved content (low risk from court sites, still handled). CORS locked to the frontend origin. Rollback = redeploy previous App Platform build.

## Demo script beats (90 seconds of product, rehearsed)

1. Cold open: the summons. "This came in the mail. It's 10 PM. Maybe you report tomorrow."
2. Screenshot of the SB jury page, full wall of text. Ask the room where it says whether you go. **Hold the silence.**
3. "This is a good court website. I'd know, I help run one. The information is all there. It's written for the institution, handed to a scared person."
4. Justicia: tap "Do I still have to go tomorrow?" Three sentences. Source quote underneath.
5. The refusal beat: "Can I get out of jury duty?" → refusal + real phone number. "It will not guess about your legal life."
6. ES toggle. "Even the Spanish is the court system's own words."
7. Closer: "The court staffs phone lines because the website doesn't answer scared people. Those lines close at 3 PM. Justicia is the call you couldn't make."

## Judge Q&A ammunition

- **Why not the county website?** It's the source, not the competitor; every answer quotes and links it. Courts staff phone lines because the site fails this user; the lines close at 3 PM.
- **Why not ChatGPT?** Structural: verified timestamped corpus, hard refusal, no account, no prompt skill needed, county isolation. "This tool cannot make things up about your court" is a sentence ChatGPT can't say.
- **Hallucination?** Never claimed absent, engineered against: strict grounding + demonstrated refusal + visible source quote on every answer.
- **Legal advice?** Procedural information only, drawn verbatim from official sources; anything else refuses and routes to the jury office. (Deliver with 5 years of authority.)
- **Stale data?** Visible "last checked" timestamp per county; refresh pipeline is a stub away from cron.
- **It's a wrapper.** It's a translator: institutional language to human language, at the hour of need, with receipts.

---

*AI assisted. Human approved. Powered by NLP.*
