# Agents & Skills

This repo defines one custom agent and nine custom skills, all
committed under `InvoicePilot_AI_Stabilized_v4/Agentic_Ai/app/`. This
document is the non-negotiable "custom agent + custom skill,
documented" checkpoint.

## The custom agent — `InvoiceAgent`

**Where:** `app/agent/invoice_agent.py`, orchestrated with
`app/agent/planner.py` and `app/agent/context.py`.

**What it does:** `InvoiceAgent` is the workflow orchestrator for the
whole invoice pipeline. It is not a wrapper around a single LLM
prompt — it's a small planning/execution loop purpose-built for this
domain:

1. **Plans.** Asks `Planner.create_plan(context)` for an ordered list
   of `PlanStep`s (skill name, whether it's required, how many times
   to retry it). The plan is domain-specific to invoice processing —
   extract → look up vendor → validate → check duplicates → apply
   policy → assess risk → recommend → queue for approval → audit.
2. **Executes with per-step retry and required/optional handling.**
   For each step it looks the skill up in the `SkillRegistry`, runs
   it against the shared `AgentContext`, retries on failure up to
   `step.retry` times, and either raises (required step) or records a
   warning and continues (optional step).
3. **Short-circuits on validation failure.** If `validate_invoice`
   fails, the agent stops the workflow rather than running policy/risk
   checks against data it already knows is invalid.
4. **Times every step** (`context.add_skill_timing`) so the UI can
   show a real per-stage processing-time breakdown, not a fake
   progress bar.
5. **Records state transitions** (`PLANNING` → running each step →
   `COMPLETED`/`FAILED`) and persists the finished `AgentContext` to
   `execution_store` so the AI Copilot and the History tab can query
   it after the fact.
6. **Never lets an exception disappear.** The top-level `try/except`
   in `process()` marks the context failed, records the error as an
   `AgentEvent`, and still saves the execution — a crashed run is
   traceable in the UI, not just a 500 in a log somewhere.

This is what "steered your AI tooling" (the Agent Engineering scoring
criterion) means concretely here: the agent's planning and control
flow is hand-written and specific to this domain, not a generic
"call an LLM and hope" loop.

## The custom skills — `app/skills/`

Each skill is a thin adapter: it pulls what it needs off
`AgentContext`, calls a business engine, writes the result back onto
the context, and records an `AgentEvent`. Registered in
`app/bootstrap.py`, ordered in `app/agent/planner.py`.

| Skill (registered name) | File | Engine it drives | What it decides |
|---|---|---|---|
| `extract_invoice` | `extract_invoice.py` | `LLMService` / `LLMRouter` | Turns the raw document (PDF/image/text) into a structured `Invoice`. The only skill that calls an LLM. |
| `vendor_lookup` | `vendor_lookup.py` | `VendorRepository` | Matches the extracted vendor name against known vendors, creates a new record if unseen, flags first-time vendors as higher risk. |
| `validate_invoice` | `validate_invoice.py` | `InvoiceValidator` | Checks required fields (vendor, invoice number, date, positive total) — see `app/validators/invoice_validator.py`. Missing/invalid fields become blocking errors; missing currency/PO become warnings. |
| `duplicate_detection` | `duplicate_detection.py` | `DuplicateInvoiceDetector` | Flags **EXACT** duplicates (same vendor + same invoice number already processed) and **SUSPECTED** duplicates (same vendor + amount + date but a different invoice number — a common tampering pattern). |
| `policy_engine` | `policy_engine.py` | `InvoicePolicyEngine` | Business rules: PO required above ₹50,000; missing GST number → review; non-INR currency → review. |
| `risk_assessment` | `risk_assessment.py` | `InvoiceRiskEngine` | Rolls validation failures, policy review flags, error/warning counts, high-value invoices, duplicate matches, and new-vendor status into one 0–100 risk score and a `LOW`/`MEDIUM`/`HIGH`/`CRITICAL` level (see thresholds in `app/core/constants.py`). |
| `recommendation` | `recommendation.py` | `InvoiceRecommendationEngine` | Turns the risk level into an actionable outcome: `AUTO_APPROVE`, `NEEDS_REVIEW`, or `REJECT`. Never executes anything itself. |
| `approval_queue` | `approval_queue.py` | `ApprovalQueueService` | If the recommendation isn't a clean auto-approve, queues the invoice for a human decision with the reason attached. |
| `audit_logger` | `audit_logger.py` | `AuditService` + `AuditLogger` | Writes the permanent, append-only audit record for the run — the source of truth for "what happened and when." |

### Why these count as genuinely custom (not boilerplate)

- Every rule threshold (₹50,000 PO cutoff, risk score weights,
  duplicate-match conditions) is domain logic specific to invoice
  processing, defined once in `app/core/constants.py` and consumed by
  the engines above — not copy-pasted example code.
- The duplicate detector implements two distinct match strategies
  (exact vs. suspected) with different evidence and a different
  reason string for each, specifically to catch the "resubmitted
  with a tampered invoice number" fraud pattern described in the
  business-process-automation brief.
- The skill/engine split (`app/skills/*` thin, `app/validators`,
  `app/policies`, `app/risk`, `app/recommendations`, `app/duplicates`,
  `app/audit` doing the real work) means every rule is independently
  unit-testable without a running agent, an LLM key, or the API layer
  — see `InvoicePilot_AI_Stabilized_v4/Agentic_Ai/tests/`.

## Extending this

To add a new skill: implement it under `app/skills/`, register it in
`app/bootstrap.py`, add it to the plan in `app/agent/planner.py` using
the *exact same string* for both the registration name and the plan
step name, and add a row to the table above plus a pytest test. See
`AGENTS.md` §3 for the full rule.
