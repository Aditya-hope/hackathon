# AGENTS.md — Rules for AI coding agents working in this repo

This is the constitution referenced by the hackathon's non-negotiable
checklist. Any AI coding agent (Cline, Roo Code, Claude, Copilot,
etc.) working in this repository must follow these rules. They exist
so an agent stays effective and predictable as the project grows,
instead of re-deriving conventions — and re-burning context/quota —
on every task.

## 1. Project identity

InvoicePilot AI is an agent-driven invoice processing system
(Track A: Business Process Automation). See `ARCHITECTURE.md` for the
full pipeline and data model before making any structural change.
See `AGENTS_AND_SKILLS.md` for what the custom agent and skills are
and where they live.

## 2. Human in the loop, always

- Never wire a code path that lets the system pay, approve, or send
  something externally without a human decision recorded in the
  Approval Queue (`app/approval`). The `recommendation` skill may
  only ever produce `AUTO_APPROVE` / `NEEDS_REVIEW` / `REJECT` — it
  must never itself execute an action.
- Do not silently swallow an exception in a **required** pipeline
  step. Optional steps may be skipped with a recorded warning
  (`context.add_warning(...)`); required steps must propagate the
  failure so the run is marked `FAILED`, not `COMPLETED`.
- Every skill must record an `AgentEvent` via `context.add_event(...)`
  for both success and failure. If a change adds a new step to the
  pipeline, it must emit events like every existing skill does — the
  audit trail is not optional instrumentation, it's the point of the
  product.

## 3. Architecture boundaries — keep layers separate

- `app/skills/*` are thin adapters only. They call into a business
  engine (`app/validators`, `app/policies`, `app/risk`,
  `app/recommendations`, `app/duplicates`, `app/vendors`, `app/audit`)
  and record the result on `AgentContext`. Business logic goes in the
  engine, not the skill.
- Business engines must stay LLM-free and synchronous. If a rule
  needs a model call, that belongs in `app/services/llm` behind the
  existing `LLMService`/`LLMRouter` interface, not a new ad hoc client
  inside a skill.
- A new skill must be:
  1. implemented under `app/skills/`,
  2. registered in `app/bootstrap.py`'s `Application.__init__`,
  3. added to the ordered list in `app/agent/planner.py`'s
     `create_plan`, with the exact same string used for both
     registration name and plan step name (this exact mismatch was a
     real, previously-fixed bug in this codebase — see the "Notes on
     this stabilization pass" section of `README.md`),
  4. documented in `AGENTS_AND_SKILLS.md`.

## 4. LLM provider rules

- Never hardcode a provider API key, model name literal, or endpoint
  URL inside a skill or business engine. Read from `app/core/config.py`
  (`Settings`) only.
- Never commit a real API key. `.env` is gitignored; only
  `.env.example` (with empty values) is tracked.
- A missing provider key must never crash the app at startup or at
  request time for endpoints that don't need it — `configured_providers()`
  exists precisely so the app degrades gracefully. Preserve that.
- When adding a provider, follow the existing `app/services/llm/*_provider.py`
  pattern and register it in `LLMRouter`'s failover order — don't add
  a second, parallel way of calling a model.

## 5. Testing expectations

- Every new business-logic function (validator rule, policy rule,
  risk factor, duplicate-match condition) needs a corresponding
  pytest test in `InvoicePilot_AI_Stabilized_v4/Agentic_Ai/tests/`.
  These must not require network access or a real API key — test the
  pure logic, not the LLM call.
- Do not merge a change that turns `backend-ci.yml` or
  `e2e-tests.yml` red. If a test needs updating because behavior
  intentionally changed, update the test in the same commit, not in
  a follow-up.
- Playwright specs under `frontend/e2e/` intercept and abort calls to
  the live backend origin (see `e2e/fixtures.ts`) so the suite is
  deterministic in CI with zero secrets. Keep new specs following
  that pattern — don't add a spec that depends on a live deployed
  backend being reachable.

## 6. Commit hygiene

- Commit continuously in small, reviewable steps as you go — a single
  end-of-day dump is explicitly penalized by the judges. Each commit
  message should say what changed and why in one line.
- Never commit `node_modules/`, `dist/`, `test-results/`,
  `playwright-report/`, `__pycache__/`, or `.env`. `.gitignore`
  already excludes these — if a change needs to add a new generated
  directory, extend `.gitignore` in the same commit, don't commit the
  artifact.
- Human-in-the-loop applies to the agent's own commits too: review a
  diff before committing it. Blind, unreviewed auto-generation is
  explicitly called out as scoring poorly.

## 7. Code style

- Match the existing style in the file you're editing (this codebase
  intentionally uses one argument/statement per line in many places —
  don't reformat unrelated code while making a small change).
- Prefer extending an existing module over adding a new one with
  overlapping responsibility. Check `ARCHITECTURE.md`'s module layout
  before deciding where new code belongs.
- Keep `README.md` accurate. If a change adds an endpoint, a skill, or
  changes setup steps, update `README.md` and `ARCHITECTURE.md` in
  the same commit.
