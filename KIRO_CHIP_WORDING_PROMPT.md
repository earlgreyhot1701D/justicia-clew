Paste this to Kiro. Small wording change, verify before committing.

---

One wording fix across two files. "Fire" reads too harsh for this context, softening it to match language already used elsewhere in the project.

1. `data/faq_chips.json` — find chip-3 and change its `question` field from:
`"Can my employer fire me for jury duty?"`
to:
`"Is my job protected while I'm on jury duty?"`
Leave the `id`, `tag`, and `county` fields on that chip untouched. Paste the full updated chip-3 line back so it can be checked.

2. `kb_setup/sb-jury-services-source.md` — find the sentence that reads:
`This is the legal basis for the common "can my employer fire me for jury duty" question.`
and change it to:
`This is the legal basis for the common "is my job protected while I'm on jury duty" question.`
This is an editorial note inside the knowledge base source document, not the actual California Government Code text quoted above it in that section, so only that one sentence changes. Do not touch the Government Code 12945.8 language itself.

Before making any changes, grep the whole repo (excluding test files) for the word "fire" case-insensitive and report every match found, so we can confirm these are the only two user-facing/KB-facing spots. Test files (`test_kb_check.py`, `test_sb_agent.py`) can stay as-is since they're internal, not shown to users.

After both edits, paste the actual updated content of both changed lines from the files themselves (not a summary) so the change can be confirmed against disk. Then run `test_kb_check.py` once to make sure the chip-3 change didn't break anything, and if the knowledge base needs to reindex to pick up the source doc wording change, note that too.

If everything checks out, commit and push:
```
git add data/faq_chips.json kb_setup/sb-jury-services-source.md
git commit -m "soften fire wording in employer chip and KB source note"
git push
```
Report back the actual file contents you saw for both changed lines, the test result, and whether the push succeeded.
