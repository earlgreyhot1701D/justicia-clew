# kb_setup/ingest_notes.md

*This file is the actual proof behind the STUB claim "remaining 52 counties, pipeline is identical, document the one command it would take." Drop this into `/kb_setup/ingest_notes.md` in the repo.*

## The one command per county

Creating a Knowledge Base is one control-plane API call. Auth is `DIGITALOCEAN_TOKEN` (a DO personal access token from the console's API/Tokens page), not the inference key and not an agent key.

```bash
curl -s -X POST https://api.digitalocean.com/v2/gen-ai/knowledge_bases \
  -H "Authorization: Bearer $DIGITALOCEAN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "kb-<county>",
    "embedding_model_uuid": "'"$EMBEDDING_MODEL_UUID"'",
    "project_id": "'"$DO_PROJECT_ID"'",
    "region": "tor1",
    "datasources": [{"web_crawler_data_source": {"base_url": "<county-jury-page-url>"}}]
  }'
```

Fill in `EMBEDDING_MODEL_UUID` and `DO_PROJECT_ID` once (same for every county), swap `<county>` and `<county-jury-page-url>` per county. That's the whole ingestion step — the rest (attach an agent to the new KB + `kb-statewide`, grab its endpoint/key, add one entry to `county_domains.json`, add two env vars) is console clicks plus a JSON edit, no new code.

## Demo counties — verified source URLs

| County | Jury page URL | Spanish reality (Spike 4) |
|---|---|---|
| Santa Barbara | santabarbara.courts.ca.gov jury services page | TBD |
| Los Angeles | `https://www.lacourt.ca.gov/pages/lp/juror-services` (also allowlist legacy `lacourt.org`) | TBD |
| San Francisco | `https://sf.courts.ca.gov/divisions/jury-services` | TBD |
| Fresno | `https://www.fresno.courts.ca.gov/divisions/jury-service` (singular, not "services") | TBD |
| Inyo | `https://www.inyo.courts.ca.gov/general-information/jury-service` (nested under general-information, not divisions) | TBD |

## Console defaults (so you don't re-decide this per county)

- Embeddings model: **GTE Large EN v1.5**, same one for every KB (locked per-KB, can't change later, no reason to vary it while everything's English).
- Reranking: **None**. Reversible later from KB settings if retrieval quality needs it, not worth the per-retrieval cost or complexity now.
- Data source: **web/sitemap URL**, pointed straight at the county's jury services page. Not file upload, not Spaces/Dropbox/S3.
- Crawl scope: **"URL and all linked pages in path"** (not seed-only, not domain-wide, not subdomains). Catches tab-style sub-pages under the same path without pulling in the whole unrelated court site.
- Embedded media indexing: **off**. Header/footer nav links: **off**. Both just add noise/cost for a government site's decorative icons and generic site nav.
- Region: **TOR1**, same one for every KB (county + statewide). Corrected from an earlier wrong call, sfo3 seemed sensible for hackathon-venue proximity, but DO's own console flagged that most Agent Platform infrastructure runs in TOR1, and a KB in a different region adds latency between the agent and its own knowledge base on every retrieval, that matters far more than laptop-to-DO distance. They also share one underlying OpenSearch database per region, deleting that database takes every KB on it with it, so don't scatter counties across regions either.
- After each county's crawl finishes: spot-check one known fact (parking address, a phone number) actually made it into the indexed content. If it's missing, that content was probably a separate URL the path scope didn't reach, add it as one more data source on the same KB rather than re-crawling broader.

## Statewide KB

`kb-statewide` ingests `https://selfhelp.courts.ca.gov/jury-services`, the specific "California Courts self-help center" your contract and mockup name, not the general `courts.ca.gov` judicial-branch page. Same `web_crawler_data_source` shape, one KB, attached to all five county agents.

## Direct KB retrieve endpoint (verification tool, not app runtime)

`kb-sb`'s retrieve endpoint: `https://kbaas.do-ai.run/v1/a540e458-7cd5-11f1-aee4-4e013e2ddde4/retrieve`. This hits the knowledge base directly and returns raw matching chunks, no agent, no LLM-written answer. It's not part of the app's request flow, `agent_client.py` still talks to the agent endpoint, not this. Use it as the fast way to run the "did a known fact actually get indexed" spot-check: curl this with a test query (like "parking") and confirm real chunks come back before assuming the agent isn't grounding well.

## Shared OpenSearch database

All six KBs (5 county + statewide) attach to the same existing OpenSearch database created with `kb-sb` (`knowledge-base-07102026`, TOR1), not a new one each time. Pick "existing" on the database step for every KB after the first.

## Gotchas (carried over from the DO reference doc, they'll bite here specifically)

- KB creation and agent creation are two different systems: KB creation is the control-plane API above (`DIGITALOCEAN_TOKEN`), calling the finished agent uses the agent's own access key, issued when you create it, not the DO token and not the inference key.
- Calling an agent needs `?agent=true` on the URL to actually run retrieval, easy to forget since it's not in the base chat/completions shape.
- If ingestion returns clean but oddly-chunked text, that's Spike 1's actual failure mode, don't wait until Block 2 to notice.
