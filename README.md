# InvoicePilot AI

Enterprise agentic AI system for invoice processing. A document (PDF,
image, or plain text) goes in; a structured extraction, validation
report, policy check, risk score, and final recommendation come out —
with a full audit trail of every step the agent took.

## Architecture

```
Upload → DocumentLoader → InvoiceAgent (Planner + SkillRegistry)
                              │
       ┌─────────────┬────────┼─────────────┬──────────────┬──────────┐
   extract_invoice validate_invoice policy_engine risk_assessment  recommendation → audit_logger
   (LLMService/Router)  (InvoiceValidator) (InvoicePolicyEngine) (InvoiceRiskEngine) (InvoiceRecommendationEngine)
```

- **`app/documents`** – Loads PDFs (PyMuPDF), images, and text files into
  a normalized `Document` object. MIME type detection is centralized in
  `documents/utils.py` (`DocumentMimeType` is the single source of truth).
- **`app/agent`** – The orchestrator. `Planner` builds an ordered list of
  skills; `InvoiceAgent` executes them against a shared `AgentContext`,
  with per-step retry and required/optional handling.
- **`app/services/llm`** – Provider-agnostic LLM layer. `LLMRouter` picks
  a provider based on document type (vision vs. text), retries on
  timeout, and fails over to the next configured provider on error.
  Providers: Gemini (vision + text), Groq, NVIDIA NIM (text-only).
- **`app/skills`** – Thin adapters that call the business engines below
  and record an `AgentEvent` on the context.
- **`app/validators`, `app/policies`, `app/risk`, `app/recommendations`,
  `app/audit`** – The actual business logic, each independently
  testable and injected via `app/bootstrap.py`.
- **`app/api`** – FastAPI app: `/health`, `/upload`, `/process-invoice`.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

cp .env.example .env
# then edit .env and add at least one provider API key
```

At least one of `GEMINI_API_KEY`, `GROQ_API_KEY`, `NVIDIA_API_KEY` must
be set for invoice extraction to work. The app itself starts fine with
none configured — providers without a key are simply skipped, and
`/health` will show which ones are active.

## Running

```bash
uvicorn app.api.main:app --reload
```

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Health check: http://127.0.0.1:8000/health

## Endpoints

| Method | Path              | Description                                   |
|--------|-------------------|------------------------------------------------|
| GET    | `/health`         | Liveness check + which LLM providers are active |
| POST   | `/upload`         | Validate & stage a document (no agent run)     |
| POST   | `/process-invoice`| Full pipeline: extract → validate → policy → risk → recommend → audit |

## Docker

```bash
docker build -t invoicepilot-ai .
docker run --env-file .env -p 8000:8000 invoicepilot-ai
```

## Notes on this stabilization pass

This codebase went through a full stabilization pass covering document
loading, the agent runtime, the LLM provider layer, error handling, and
the API surface. A few of the bugs found and fixed along the way:

- `app/documents/utils.py` imported a `DocumentMimeType` type that
  didn't exist anywhere in the codebase (it was called `DocumentType`)
  — this alone broke every import of `app.documents`.
- `app/agent/__init__.py` imported `EventLogger`, which was never
  defined in `event.py` — broke every import of `app.agent`.
- `InvoiceAgent.process()` iterated the planner's `PlanStep` objects as
  if they were raw skill-name strings, and the planner's step names
  (`apply_policy`, `assess_risk`, ...) didn't match the names skills
  were actually registered under (`policy_engine`, `risk_assessment`,
  ...) — every workflow run would have raised `KeyError`.
- `GeminiProvider` called `document.mime_type.value`, but `mime_type`
  is a plain string on `Document`, not an enum.
- `GeminiProvider` imported a `build_prompt` function that doesn't
  exist in `prompt_manager.py`.
- LLM providers crashed the entire application at startup if any one
  API key was missing; a missing key now just disables that provider.

Given this sandbox has no network access, the fixes above were
verified by full syntax compilation (`py_compile`) and a static
cross-module import check (every `from app.x import y` resolves to a
name that actually exists in `x`), plus manual tracing of the runtime
call graph. They have not been exercised against live LLM APIs —
please do a real end-to-end run with a configured API key before
treating this as production-ready.
