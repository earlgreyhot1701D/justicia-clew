# Block 0 checklist — literal, in order

*Matches contract Block 0: "Rules check, fresh repo, DO project, env keys. QA: hello-world inference call returns."*

*Corrected after you sent the real DO reference doc — the version below replaces guesses from generic web search (which mostly failed to fetch) with the actual API shape. There's also a fuller version of this same reference already saved in this project as `digitalocean-ai-hackathon-guide.md`, worth checking directly if anything below is ambiguous.*

## 1. Credits, before anything else

- [ ] Confirm what the actual credit amount and redemption path are for your event — the reference doc mentions $200 in credits to start and a $600 prize for best use of DigitalOcean AI, but confirm the code/link with your organizers, don't assume it's the same one I found on a Devpost page (you already flagged that page might've been the wrong event).
- [ ] Redeem at the DigitalOcean console, new or existing account both work per the reference doc.
- [ ] If you already have a DO account, confirm the code applies to it. If it's new-account-only and yours won't take it, decide now whether to spin up a fresh account.

## 2. DigitalOcean account + billing

- [ ] Log in (or sign up) at cloud.digitalocean.com.
- [ ] Go to **Billing**, redeem the credit, confirm it shows in your balance.
- [ ] Add a payment method anyway even with credit applied.
- [ ] Note any credit expiration date somewhere you'll actually see it.

## 3. Fresh project

- [ ] Create a new **Project** named `justicia-clew`. Matches your contract's "fresh repo at kickoff regardless" rule, extended to cloud resources too.

## 4. Two keys, not one — get both now

- [ ] **Model access key** (for the sanity check + optional direct calls): left nav → **Inference › Serverless Inference** → Get Started tab → **Create a Model Access Key**. Export as `DIGITAL_OCEAN_MODEL_ACCESS_KEY`.
- [ ] **Personal access token** (for creating Knowledge Bases via the control-plane API): console → **API** → **Tokens** → generate one. Export as `DIGITALOCEAN_TOKEN`. This is a *different* credential from the model access key, don't conflate them, they hit different endpoints (`inference.do-ai.run` vs `api.digitalocean.com`).
  - **Scopes: Custom, not Full Access, not Read Only.** Search "genai" and check all 4 (create/read/update/delete), that's the only resource this token is actually for. Leave `genai_genie` and everything else (billing, droplet, kubernetes, app, etc.) unchecked.
  - DO's console will flag 3 more as required to make that selection work: `regions:read`, `sizes:read`, `actions:read`. Accept those, they're read-only metadata lookups (data center regions, Droplet plan sizes, operation status events), not scope creep, DO's own dependency check, not an extra ask.
  - **Final scope set for this token:** `genai` (C/R/U/D) + `regions:read` + `sizes:read` + `actions:read`. If anything else in the build ever throws a 403 against `api.digitalocean.com`, that's your first check, whatever new call you're making needs a scope not in this list, add it there rather than jumping to Full Access.
- [ ] Sanity check both work: a call against `https://inference.do-ai.run/v1/chat/completions` with the model key, using `anthropic-claude-haiku-4.5` as the model, since that's what the county agents will run. curl, the OpenAI SDK, or DO's own `pydo` client all work here, `pydo`'s `client.inference.create_chat_completion(...)` is a fine choice if that's what the console handed you. If that returns text, your account plumbing is confirmed before you touch anything county-specific.

## 5. First Knowledge Base — minimum plumbing only

*Ruthless scoping call: the full Spike 1/2/3 verification below is already scheduled to happen for real at Block 2 ("QA: Spike 2 and 3 tests repeated on the real build," straight from the contract). Doing it twice, once here and once there, is the waste. Here, just get it existing.*

- [ ] Create Knowledge Base #1 for Santa Barbara using the control-plane call in `kb_setup/ingest_notes.md` (or the console UI if that's faster). Point it at the SB jury page.
- [ ] Confirm ingestion finished. Don't stop to inspect chunk quality, that's Block 2's job.

## 6. First Agent — minimum plumbing only

- [ ] Create an Agent in the console, attach `kb-sb`.
- [ ] Paste in the four grounding/refusal instruction lines from `ARCHITECTURE.md`.
- [ ] Send it one message in the Playground, just to confirm it responds with something. Not the full 5-question-plus-refusal test, that's Block 2.
- [ ] Grab that agent's own endpoint URL + its own access key from the agent's detail page. Export as `AGENT_ENDPOINT_SB` / `AGENT_ACCESS_KEY_SB`.
- [ ] Remember `?agent=true` on the URL when calling it later, without it retrieval doesn't run.

## 7. Local repo + env

- [ ] Fresh git repo, scaffold the layout from `ARCHITECTURE.md`.
- [ ] `.env` populated with the real SB agent endpoint + key (copy `.env.example`, confirm `.env` is in `.gitignore` before your first commit). The model key and DO token can also live here locally, they just never travel to App Platform's deployed env config.
- [ ] Install Block 0 dependencies: fastapi, uvicorn, python-dotenv, httpx.

## 8. QA gate — hello-world inference call

- [ ] `uvicorn backend.main:app --port 8080` boots locally with no errors (port 8080 to match what App Platform expects later).
- [ ] `GET /health` returns 200.
- [ ] One direct call to the SB agent's endpoint (curl or a throwaway script, doesn't need FastAPI yet) with `?agent=true` returns a real, grounded answer. That's the actual "hello-world inference call returns" bar from the contract.
