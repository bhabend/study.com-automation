# Study.com Automation System (Gemini)

This repository implements the Study.com automation workflow (fetch → extract → score → rewrite with Gemini → docs/diff → outputs + UI) described in the workflow document. See the uploaded automation workflow for full design details. :contentReference[oaicite:1]{index=1}

## Quick facts
- LLM Provider: Gemini (Google Generative API)
- UI: Streamlit (simple dashboard + uploader)
- Output: Processed Google Sheet, before/after Word docs, diffs
- Human-in-the-loop: Light QA step (manual review) before publishing

## Environment variables required (set in GitHub / Render / local .env)
- `GOOGLE_SERVICE_ACCOUNT_JSON` (full JSON content of service account for Sheets + Generative API)
- `GOOGLE_SHEET_ID`
- `LLM_PROVIDER` = `gemini`
- `GEMINI_MODEL` = e.g. `models/text-bison-001` or your chosen model name
- `SERPAPI_KEY` (optional, for backlink enrichment)
