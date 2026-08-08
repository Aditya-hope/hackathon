# PRD — InvoicePilot AI

Track A: Business Process Automation. This document specifies what
InvoicePilot AI does, for whom, and how each requirement is verified
— written against the actual implementation in this repo, not an
aspirational version of it. Pair with `ARCHITECTURE.md` (how it's
built) and `AGENTS_AND_SKILLS.md` (the agent/skill breakdown).

## 1. Problem

Manual accounts-payable invoice intake — someone opens a PDF or
scanned image, keys the fields into a spreadsheet or ERP by hand,
eyeballs whether it looks right, checks it against a purchase order
if they remember to — is slow and inconsistent, and has no reliable,
auditable check against duplicate payments, missing purchase orders,
or policy violations. Mistakes are found after the money has left.

## 2. Goal

Give a finance/AP team an agent-driven intake pipeline that: extracts
invoice data automatically, applies the same validation and policy
checks every time, flags risk consistently, and routes anything above
a safe threshold to a human — while keeping a full, readable trail of
what happened and why for every single invoice, auto-approved or not.

## 3. Users

| Persona | Wants |
|---|---|
| **AP clerk** | Upload an invoice (PDF/image/text) and get structured, checked data back in seconds instead of typing it in by hand. |
| **AP manager / finance reviewer** | A queue of only the invoices that actually need a human decision, with the reasoning already laid out, so they're not re-checking every invoice from scratch. |
| **Auditor / compliance reviewer** | For any invoice, after the fact: what was extracted, what was checked, what the risk score was, who approved or rejected it, and when. |
| **Hackathon judge** | A working system where they can trace one invoice through every step and trust nothing was decided silently. |

## 4. Scope

### 4.1 In scope (implemented and testable today)

- Upload a single invoice or a batch, as PDF, PNG/JPG, or plain text
  (`SUPPORTED_TYPES` in the frontend; `PDFLoader`/`ImageLoader`/`TextLoader`
  on the backend), or paste invoice text directly.
- LLM-based structured extraction of vendor, invoice number, date,
  line items, subtotal, tax, total, currency, purchase order, and GST
  number — via a provider-agnostic router (Gemini → Groq → NVIDIA NIM)
  with automatic failover if one provider is down or rate-limited.
- Deterministic validation of the extracted fields (required-field and
  sanity checks).
- Deterministic duplicate detection: exact match (same vendor + same
  invoice number) and suspected match (same vendor + same amount +
  same date, different invoice number).
- Deterministic policy checks: purchase order required above
  ₹50,000; GST number required; non-local currency flagged for
  review.
- Deterministic risk scoring (0–100) rolling up validation failures,
  policy flags, invoice value, duplicate status, and new-vendor
  status into LOW / MEDIUM / HIGH / CRITICAL.
- A recommendation (`AUTO_APPROVE` / `NEEDS_REVIEW` / `REJECT`) derived
  from the above — never a raw LLM opinion.
- A human approval queue: anything not a clean auto-approve waits for
  a person to approve or reject, with the decision, reviewer, and
  notes recorded.
- A full step-by-step audit log per invoice, independent of outcome.
- An AI Copilot chat scoped to one invoice's real extracted data
  (explicitly instructed not to invent information), with a fully
  offline mock-answer mode when no backend is reachable.
- An offline/demo mode across the whole app (sample-data processing,
  a mock approval queue, mock Copilot answers) so the console is
  fully demoable with no backend, no API keys, and no network.

### 4.2 Explicitly out of scope (v1)

- Real payment execution — the system recommends and routes; it never
  moves money.
- Persistent storage across restarts — execution history, vendor
  records, and duplicate fingerprints are in-memory in this version
  and reset when the backend restarts.
- Configurable-per-organization policy rules — the three policy rules
  and all thresholds are hardcoded constants, not admin-editable.
- Authentication / role-based access control — there is no login;
  anyone with the URL can approve or reject.
- Multi-currency conversion — currency is detected and flagged, not
  converted.

## 5. Functional requirements — user stories & acceptance criteria

### US-1: Upload and extract an invoice
**As an** AP clerk, **I want to** upload a PDF, image, or text invoice
**so that** I don't have to key its fields in by hand.

- **AC1** — Given a supported file type (`.pdf`, `.png`, `.jpg`,
  `.jpeg`, `.txt`) under 25 MB, when I upload it and run the agent,
  the system returns vendor name, invoice number, date, line items,
  and total amount without manual entry.
- **AC2** — Given an unsupported file type, the upload is rejected
  before it's queued, with a clear reason shown.
- **AC3** — Given the configured LLM provider is unreachable, the
  system fails over to the next configured provider automatically,
  without the user having to retry manually.
- **AC4** — Given no provider is reachable, the failure is shown
  per-invoice, not as a silent hang or a crash of the whole page.

### US-2: Catch problems before a human has to
**As an** AP manager, **I want** every invoice checked the same way
**so that** I'm not relying on someone remembering to check it.

- **AC1** — Given an invoice missing a required field (vendor name,
  invoice number, date, or total), validation records an error and
  the risk score increases by a fixed amount per error.
- **AC2** — Given an invoice over ₹50,000 with no purchase order
  number, the policy engine flags it and the recommendation is never
  a clean auto-approve.
- **AC3** — Given an invoice with the same vendor and invoice number
  as one already on file, it is flagged as an exact duplicate; given
  the same vendor, amount, and date but a different invoice number,
  it is flagged as a suspected duplicate.
- **AC4** — Given a risk score of 80 or higher, the level shown is
  CRITICAL; 60–79 is HIGH; 30–59 is MEDIUM; below 30 is LOW — the
  same score always produces the same level.

### US-3: Only see what actually needs a decision
**As an** AP manager, **I want** a queue of only the invoices that
need my judgment **so that** I'm not re-reviewing everything.

- **AC1** — Given an invoice's recommendation is `AUTO_APPROVE`, it
  does **not** appear in the Approval Queue.
- **AC2** — Given an invoice's recommendation is `NEEDS_REVIEW` or
  `REJECT`, it appears in the Approval Queue with the risk level and
  the reasons attached, so the reviewer isn't starting from zero.
- **AC3** — Given a reviewer approves or rejects an item, the
  decision, the reviewer's name, and any notes are recorded against
  that invoice and the item leaves the pending queue.

### US-4: Trust the decision after the fact
**As an** auditor, **I want to** see exactly what happened for any
invoice **so that** I can verify nothing was decided silently.

- **AC1** — Given any processed invoice, the History tab shows every
  pipeline step that ran, in order, with each step's outcome.
- **AC2** — Given an invoice was auto-approved, the audit trail exists
  and is just as complete as for one that went to a human — outcome
  never determines whether it's logged.
- **AC3** — Given an approval/rejection decision, the audit trail
  distinguishes "the model recommended X" from "a human decided Y."

### US-5: Ask questions about a specific invoice
**As an** AP clerk, **I want to** ask follow-up questions about one
invoice **so that** I don't have to re-derive why it was flagged.

- **AC1** — Given a processed invoice is selected, asking "why wasn't
  this approved?" returns an answer grounded in that invoice's actual
  validation/policy/risk results, not a generic response.
- **AC2** — Given the backend is unreachable, the Copilot still
  answers using a deterministic mock response built from the same
  invoice data, rather than failing outright.
- **AC3** — Given no invoice has been processed yet, the Copilot
  shows an empty state rather than a broken chat window.

### US-6: Demo or judge the system with no setup
**As a** hackathon judge, **I want to** see the whole flow work
**so that** I don't need API keys or a live backend to evaluate it.

- **AC1** — Given the configured backend is unreachable, the frontend
  detects this and switches to an offline mode rather than showing a
  blank or broken page.
- **AC2** — Given offline mode, uploading a sample invoice still
  produces a full pipeline run, a risk score, a recommendation, and a
  populated Approval Queue and History.

## 6. Non-functional requirements

| Requirement | Target / current behavior |
|---|---|
| Traceability | Every automated decision must be attributable to a named skill and, for the risk score, a named factor — never an unexplained LLM output. |
| Explainability | The recommendation must state which rule(s) drove it, not just the outcome. |
| Resilience | LLM provider failure must fail over automatically (US-1/AC3) rather than fail the whole request. |
| Demoability | The app must be fully operable with zero backend and zero API keys (offline mode), so a broken deployment doesn't block evaluation. |
| Auditability | The audit log is append-style per run and independent of outcome (US-4/AC2). |
| File size | Uploads capped at 25 MB per file. |

## 7. Success metrics (how we'd know this works, beyond the demo)

- **Extraction accuracy**: % of required fields (vendor, invoice #,
  date, total) correctly extracted on a sample of real invoices,
  measured against manual entry.
- **False-auto-approve rate**: % of `AUTO_APPROVE` invoices that a
  human reviewer, on spot-check, would have flagged — target as
  close to 0% as possible, since this is the metric that matters most
  for trust.
- **Time to process**: end-to-end time from upload to
  recommendation, per invoice.
- **Reviewer load reduction**: % of processed invoices that never
  need to enter the Approval Queue (i.e., correctly auto-approved).

## 8. Known limitations (see also `ARCHITECTURE.md` §"Known gaps")

- No persistent storage — history, vendor records, and duplicate
  fingerprints reset when the backend restarts.
- Policy rules and all thresholds (₹50,000 PO threshold, risk score
  weights, risk level bands) are hardcoded, not configurable per
  organization.
- No authentication — approval actions are not tied to a verified
  identity, only a freely-typed reviewer name.
- Extraction quality depends on the underlying LLM provider and has
  not been benchmarked at scale against messy real-world scans.

## 9. Open questions for a v2

- Should policy thresholds move to a config file / admin UI instead
  of Python constants?
- Should the approval queue require a second reviewer for
  CRITICAL-risk invoices (maker-checker), rather than any single
  reviewer?
- What's the retention/persistence story once this moves off
  in-memory storage — a database, and if so, what audit-log
  immutability guarantees does it need?
