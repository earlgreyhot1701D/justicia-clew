# Kiro hooks — self-QA, 2 max

*Replaces the contract's "fresh Claude session per block" QA gate with something Kiro runs itself. This is a real speed trade: less certainty per check, way less wall-clock per check. Given the deadline, that's the right trade.*

Grounded in Kiro's actual hook system (trigger types, agent-prompt vs shell-command actions), not guessed. One honest gap below on exactly how hard "blocking" is for the first hook — flagged where it matters.

---

## Hook 1 — Block Gate (runs itself, before every new task)

**Trigger:** `Pre Task Execution` — fires right before Kiro starts the next spec task. Since your blocks roughly map to Kiro's spec tasks, this lands at the same point your manual per-block gate used to.

**Fastest way to create it:** open Kiro's hook creator and describe it in plain language (Kiro can write the JSON for you), don't hand-author JSON under time pressure. Paste this:

> Before starting the next task, review the code changed in the task that just finished against these rules: (1) Scope adherence — nothing outside this task changed, no NEVER-list item got built (no accounts, no history, no legal-advice or excusal logic, no native app, no scraping outside official court/Judicial Council domains, no unlabeled machine translation), and any STUB item is interface-plus-comment only, not partially built. (2) Security — textContent only, never innerHTML, no eval, all API keys and DO tokens stay in server-side env vars, try/catch on every fetch, input validation on the URL field against the court-domain allowlist. (3) Accessibility — semantic HTML, labeled inputs, 44px+ touch targets, WCAG AA contrast, keyboard reachable. (4) Error states — no failure path renders a blank screen. A STUB gap (a feature marked STUB and left as interface + comment) is expected and should PASS, it is not a failure. Report PASS or FAIL per category with file and line evidence. If any category genuinely FAILs, say so clearly and do not proceed to the next task until it's addressed. If all four PASS, say so and continue.

**Honest gap:** Kiro's docs list `Pre Task Execution` among the trigger types that *can* block, but the concrete "exit code 2 blocks execution" mechanic in their docs is described mainly for shell-command actions, not agent-prompt actions like this one. In practice this hook will reliably get its findings in front of Kiro before the next task starts and the prompt explicitly tells it not to proceed on FAIL, but I can't promise it's a hard system-level stop the way `Pre Task Execution` blocking is for a shell command. Treat it as a strong nudge you're very likely to see, not an unbypassable gate. Given the deadline, that's still much faster than your manual process and worth the small loss of certainty.

---

## Hook 2 — Pre-Submission Lock (run once, by hand, right before you hit submit)

**Trigger:** `Manual Trigger` — you fire this on demand, not tied to any task boundary. Run it once, deliberately, before Devpost submission.

**Prompt:**

> Check the current state of the whole app, not just the latest change, against these six items only. They do not get cut no matter what else is stubbed: (1) refusal behavior returns the real county phone number for at least one refusal case. (2) Every non-refusal answer shows the exact source quote and labels itself county-site vs statewide Judicial Council, never blended silently. (3) The trust banner and "not legal advice" footer text are present, in both languages if the language toggle is live. (4) Every fetch has a try/catch with a real, meaningful error message on failure, never a blank screen. (5) Accessibility baseline holds: semantic HTML, labeled inputs, 44px+ touch targets, contrast, full keyboard navigation. (6) The independence disclaimer text is in the footer and in the README. Report PASS or FAIL per item with file evidence. Be strict here, this is the last check before submission.

That's the two-hook budget. Everything else about QA reverts to you eyeballing Kiro's output as it works, which you'd be doing anyway.
