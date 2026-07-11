# Justicia Clew

Plain-language jury duty answers, in the court system's own words. Built for California, all 58 counties useful on day one via the statewide layer, deep coverage for demo counties (Santa Barbara, Los Angeles, San Francisco, Fresno, Inyo).

Citizen-facing sibling of Themis Lex. Themis Lex serves the people who run the court, Justicia Clew serves the people the court summons.

## What it does

You pick your county (or paste the court URL from your summons), tap a question or type your own, and get a plain-language answer with the exact source quote underneath. If the answer isn't in the court's own published pages, Justicia says so and gives you the jury office phone number instead of guessing.

## What it is not

Not legal advice. Not affiliated with or endorsed by any court. Not a prediction of whether you'll be called in, that's always the court's own portal or phone line. Not a place that remembers anything about you: no accounts, no history, no stored questions, no tracking.

## How it works

- Mobile-first web app, FastAPI backend, DigitalOcean Gradient AI (Knowledge Bases + Agents) as the AI layer.
- Answers are grounded only in ingested official content from each county's court site and the California Courts self-help center. Nothing else.
- Every answer names its source: your court's website, or the statewide Judicial Council site. Never blended silently.

## Independence disclaimer

This is a personal project, built on publicly available information. It is not affiliated with, endorsed by, or reviewed by any California court, the Judicial Council, or any county jury services office.

## Honest limitations

*(fill in during Block 6 — demo prep. Keep this section truthful, not marketing copy. Known candidates: only 5 of 58 counties have live data at demo time, remaining 52 use an identical but not-yet-run ingestion pipeline; refresh is manual, not scheduled; Spanish depth depends on Spike 4 findings.)*

## Status

Built solo for AI for Social Good, MLH x DigitalOcean, San Francisco, July 2026.

---

*AI assisted. Human approved. Powered by NLP.*
