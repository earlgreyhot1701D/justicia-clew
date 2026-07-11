Paste this to Kiro. This is the last pass on the refusal heuristic today, don't keep iterating on it past this.

---

You're right about the two missing phrases, add these five to `refusal_signals` in `backend/services/agent_client.py`:

```python
"i can't advise",
"i cannot advise",
"i can't predict",
"i cannot predict",
"not in my knowledge",
```

Do NOT add `"contact the court"`, `"call the court"`, `"call south county"`, or `"call north county"`. Those are too generic, real grounded answers (like the parking and reporting-status answers) can legitimately mention calling or contacting the court as part of a genuinely good answer, and adding those phrases would very likely start mislabeling more good answers as refusals, the same false-positive problem already flagged on chip-7 and chip-8.

After adding just the five phrases above: restart uvicorn, run `test_sb_agent.py` one more time, and confirm both "Can I get out of jury duty?" and "What are the odds I'll be selected?" now come back as refusals with the phone number and hours attached. Paste the full test output.

Once that passes, this heuristic is done for today. Commit and push:
```
git add .
git commit -m "add missing refusal phrases for excusal and prediction questions"
git push
```
Then stop, don't keep tuning `refusal_signals` further, we're moving to the demo and writeup next.
