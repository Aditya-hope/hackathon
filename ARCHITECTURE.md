# Architecture — InvoicePilot AI

Track A: Business Process Automation. InvoicePilot AI takes a real,
manual, repetitive back-office workflow — accounts-payable invoice
intake — and rebuilds it as an agent-driven pipeline where every
step is traced, every automated decision is explained, and anything
above policy risk is queued for a human to approve or reject before
it counts as final.

## 1. The workflow being automated

Manual accounts-payable invoice processing today looks like: someone
opens an email or a scanned PDF, keys the invoice fields into a
spreadsheet or ERP by hand, eyeballs whether the numbers look right,
checks it against a purchase order if they remember to, and files it.
Mistakes and duplicate payments slip through because there's no
consistent, auditable check at each step.

InvoicePilot AI replaces that with:

```
Document (PDF / image / pasted text)
        │
        ▼
  DocumentLoader              — normalizes the input into one Document type
        │
        ▼
  InvoiceAgent  (Planner + SkillRegistry)
        │
        ├─ extract_invoice        LLM pulls structured fields out of raw text/image
        ├─ vendor_lookup          matches/creates a vendor record, flags new vendors
        ├─ validate_invoice       required-field + sanity checks → pass/fail
        ├─ duplicate_detection    exact + suspected duplicate-submission detection
        ├─ policy_engine          business rules (PO threshold, GST, currency, …)
        ├─ risk_assessment        rolls all of the above into one risk score/level
        ├─ recommendation         AUTO-APPROVE / NEEDS-REVIEW / REJECT
        ├─ approval_queue         queues anything that needs a human decision
        └─ audit_logger           writes an immutable event trail for the run
        │
        ▼
  ProcessInvoiceResponse — every field above, plus the full step-by-step
  event log, returned to the frontend and to the AI Copilot
```

Every one of those nine steps is a named, independently testable unit
(a **skill**). Nothing about the outcome is decided by a single opaque
LLM call — extraction is the only step that calls an LLM at all; every
decision after that (validate, detect duplicates, apply policy, score
risk, recommend, queue for approval) is deterministic business logic a
judge can read line by line. That's the traceability the brief asks
for: pick any invoice in the History tab and you can see exactly which
skill ran, in what order, what it decided, and why.

## 2. Where a human is in the loop

Per the brief's "what good looks like" for Track A — *"a judge should
be able to follow how a decision was made, see where a human approved
it, and trust that nothing happened silently"*:

- The `recommendation` skill never auto-executes a payment. It only
  ever produces one of `AUTO_APPROVE`, `NEEDS_REVIEW`, or `REJECT`.
- Anything not a clean `AUTO_APPROVE` is written to the **Approval
  Queue** (`app/approval`) with the reason attached, and sits there
  until a person calls `POST /approvals/{id}/approve` or `/reject`
  from the Approvals tab in the UI.
- Every approval/rejection is recorded with `decided_by` and
  `decision_notes`, so the audit trail shows who made the call, not
  just what the model suggested.
- The `audit_logger` skill writes a permanent event for every run,
  independent of the outcome, so even an auto-approved invoice has a
  full record of the steps that led there.

## 3. Tech stack

| Layer | Choice | Why |
|---|---|---|
| Backend | Python 3.11+, FastAPI, Pydantic v2 | async I/O for LLM calls, automatic OpenAPI docs (`/docs`), typed request/response models |
| Document parsing | PyMuPDF (`pymupdf`) | text + image extraction from PDFs without external services |
| LLM providers | Google Gemini, Groq, NVIDIA NIM — via a provider-agnostic router | free tiers per the hackathon's rate-limit guidance; automatic failover if one provider is rate-limited or down |
| Frontend | React 19 + TypeScript, Vite, Tailwind CSS | fast dev loop, typed components |
| E2E testing | Playwright | drives the real UI in a browser, runs headless in CI |
| Backend testing | pytest | pure-logic unit tests, no network/LLM calls needed |
| CI/CD | GitHub Actions | `backend-ci.yml` (lint + pytest), `e2e-tests.yml` (Playwright), `deploy.yml` (frontend → GitHub Pages) |
| Backend hosting | Docker image, deployable to Render / any container host | `Dockerfile` included at `InvoicePilot_AI_Stabilized_v4/Agentic_Ai/` |

## 4. Data model

The system is intentionally stateless/in-memory for the hackathon
timeframe (no DB dependency to stand up) — every store is a small,
swappable in-process repository behind an interface, so a real
database can be dropped in later without touching callers.

**`Invoice`** (`app/schemas/invoice.py`) — the structured output of
extraction: `vendor_name`, `invoice_number`, `invoice_date`,
`due_date`, `currency`, `subtotal`, `tax`, `total_amount`,
`gst_number`, `purchase_order`, `payment_terms`, `line_items`
(`LineItem[]`: description, quantity, unit_price, amount), and a
`confidence` score from the extraction step.

**`AgentContext`** (`app/agent/context.py`) — the single object that
flows through every skill in the pipeline. It accumulates: the
loaded `Document`, the extracted `Invoice`, `ValidationResult`,
`DuplicateResult`, `PolicyResult`, `RiskResult`, the final
recommendation, a list of `AgentEvent`s (one per skill executed, with
timestamp/status/message), warnings, errors, per-skill timings, and
run `metadata` (execution id, provider used, retry count). This is
what makes a run fully replayable and auditable after the fact — the
API returns this context, not just a final verdict.

**`Vendor`** (`app/vendors/vendor_record.py`) — accumulated per
vendor across runs: name, GST number, status, total invoices,
total spend, currencies seen, first/last seen dates. Lets the system
flag a vendor as "new" (higher risk) vs. established.

**`ApprovalItem`** (`app/approval/approval_item.py`) — one row in the
human review queue: the invoice summary, risk level/score, the reason
it needs review, its status (pending/approved/rejected), and who
decided it and when.

**`AuditRecord`** (`app/audit/audit_record.py`) — the permanent,
append-only log entry written for every completed or failed run.

## 5. Module layout

```
InvoicePilot_AI_Stabilized_v4/Agentic_Ai/
├── app/
│   ├── agent/         orchestrator: Planner, InvoiceAgent, AgentContext, execution store
│   ├── skills/         thin adapters — one per pipeline step, each wraps a business engine
│   ├── validators/      field-level validation rules
│   ├── policies/        business rule engine (PO threshold, GST, currency)
│   ├── risk/            risk scoring engine
│   ├── recommendations/ auto-approve / needs-review / reject decision
│   ├── duplicates/       duplicate-submission detection
│   ├── vendors/          vendor repository
│   ├── approval/         human-in-the-loop approval queue
│   ├── audit/            audit trail service + logger
│   ├── documents/        PDF/image/text loading & normalization
│   ├── services/llm/     provider-agnostic LLM layer (Gemini / Groq / NVIDIA) with routing + failover
│   ├── assistant/        AI Copilot — natural-language Q&A over a processed invoice
│   ├── prompts/          all LLM prompt templates, centralized
│   ├── schemas/          Pydantic models (Invoice, chat, API responses)
│   ├── core/             settings, constants, logging
│   ├── api/              FastAPI routes, request/response models, exception handlers
│   └── bootstrap.py      dependency-injection container — wires every engine, skill,
│                          the planner and the agent together at startup
├── tests/                pytest unit tests (validators, policy, risk, duplicates, planner, API)
├── frontend/
│   ├── src/InvoicePilotAI.jsx   main app (Upload, History, Approvals, Vendors, Copilot, Settings)
│   └── e2e/                     Playwright end-to-end specs
├── requirements.txt
├── Dockerfile
└── .env.example
```

## 6. API surface

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | liveness + which LLM providers are configured |
| POST | `/upload` | validate & stage a document without running the agent |
| POST | `/process-invoice` | run one uploaded file through the full pipeline |
| POST | `/process-invoices` | same, batched — up to 50 files, independent per-file results |
| POST | `/process-invoice-text` | run pasted/typed invoice text through the same pipeline |
| GET/POST | `/vendors`, `/vendors/{name}` | vendor database |
| GET | `/approvals`, `/approvals/{id}` | human review queue |
| POST | `/approvals/{id}/approve` \| `/reject` | record a human decision |
| POST | `/chat` | AI Copilot — ask questions about a processed invoice |
| GET/DELETE | `/chat/{id}/history` | Copilot conversation history |
| DELETE | `/executions/{id}` | remove a processed invoice from History |

Full interactive docs are auto-generated by FastAPI at `/docs` once
the backend is running.

## 7. Design decisions worth calling out

- **LLM calls are isolated to one skill.** `extract_invoice` is the
  only step that talks to a model. Every downstream decision
  (validation, policy, risk, recommendation) is ordinary Python
  logic — reviewable, testable without an API key, and immune to the
  model changing its mind between requests.
- **Provider failover, not a single point of failure.** `LLMRouter`
  picks a provider per document type and falls over to the next
  configured provider on timeout/error, matching the hackathon's
  "split providers by job" guidance — a rate-limited provider doesn't
  take the whole app down.
- **Offline demo mode in the frontend.** The console can run through
  sample invoices, a mock approval queue, and mock Copilot answers
  entirely client-side, so the app is demoable even if the deployed
  backend is asleep, unreachable, or has no provider keys configured
  during the live demo.
- **Required vs. optional skills with per-step retry.** `Planner`
  marks each step required/optional with a retry count; a failed
  optional step is recorded as a warning and skipped rather than
  aborting the whole run, while a failed required step (e.g.
  extraction) stops the pipeline and is reported, not silently
  swallowed.
