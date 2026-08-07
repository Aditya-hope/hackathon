# Submission Checklist — Deploy or Die

Read this top to bottom before you touch anything. Steps are ordered
by what has the biggest effect on the gate first.

## 0. What changed in this package vs. what you had

- Added at repo root: `ARCHITECTURE.md`, `AGENTS.md`, `AGENTS_AND_SKILLS.md`.
- Added `.github/workflows/backend-ci.yml` and `.github/workflows/e2e-tests.yml`
  (your `deploy.yml` for the frontend is unchanged).
- Added `InvoicePilot_AI_Stabilized_v4/Agentic_Ai/tests/` — 7 pytest
  files covering the validator, policy engine, risk engine, duplicate
  detector, planner/skill-registry wiring, and an API smoke test.
  These require no API keys and no network access.
- Added `requirements-dev.txt` (test-only deps: pytest, httpx) and
  `pytest.ini`.
- Rewrote `.gitignore` to actually exclude `node_modules/`, `dist/`,
  `test-results/`, `playwright-report/` — none of these should ever
  be committed.
- Removed a stray empty `npm` file and build/test output that had
  been sitting in the frontend folder.
- **Your GitHub repo currently has a `.AGENTS.md` (with a leading
  dot) at root — that does not satisfy the checkpoint, which needs
  exactly `.clinerules`, `AGENTS.md`, or `constitution.md`. This
  package's `AGENTS.md` (no dot) replaces it. Delete the old
  `.AGENTS.md` when you push so you don't have both.**
- I could not read the current contents of your live repo's
  `ARCHITECTURE.md` / `AGENTS_AND_SKILLS.md` / `.AGENTS.md` (GitHub
  blocked the fetch), so I rebuilt all three from scratch against
  your actual code rather than guess at merging. If you'd already
  written something you like in those, this will overwrite it —
  check before you push if that matters to you.

## 1. Push this to GitHub (replaces what's there)

From the folder you unzipped this into:

```bash
cd hackathon-final
git init                                   # if starting fresh, otherwise skip
git remote add origin https://github.com/Aditya-hope/hackathon.git
# or: git remote set-url origin https://github.com/Aditya-hope/hackathon.git

git add -A
git commit -m "Add architecture/agent docs, backend tests, CI workflows; fix gitignore"
git push origin main --force
```

`--force` is only safe here because you're intentionally replacing
the repo content with this package. If you have teammates who've
pushed commits since this zip was made, coordinate with them first —
you don't want to blow away their work.

If you'd rather not force-push, do it as a normal commit on top of
your existing history instead — just delete the old `.AGENTS.md` in
the same commit (`git rm .AGENTS.md`) and copy these new files in.

## 2. Watch the Actions tab

Go to `https://github.com/Aditya-hope/hackathon/actions` right after
pushing. You want to see three workflows run:

- **Backend CI** — installs `requirements.txt` + `requirements-dev.txt`,
  byte-compiles everything, runs pytest. Should go green in under a
  minute; there's no LLM call in any of these tests.
- **E2E Tests (Playwright)** — builds the frontend, runs the existing
  Playwright suite against the app's offline demo mode. Takes a few
  minutes (installing Chromium is the slow part).
- **Deploy frontend to GitHub Pages** — your existing workflow,
  unchanged.

If any of them go red, open the run and read the first failed step —
paste me the error and I'll fix it live rather than guessing blind.

## 3. Verify the five non-negotiables yourself, like the checker will

- [ ] `ARCHITECTURE.md` present at repo root — describes stack, data
      model, high-level design. ✅ included here.
- [ ] Agent rules file present — `AGENTS.md` at repo root (delete the
      old `.AGENTS.md`). ✅ included here.
- [ ] Working code — the app builds and runs. Prove it locally:
      ```bash
      cd InvoicePilot_AI_Stabilized_v4/Agentic_Ai
      python -m venv .venv && source .venv/bin/activate
      pip install -r requirements.txt
      cp .env.example .env      # add at least one provider key if you have one
      uvicorn app.api.main:app --reload
      # in another terminal:
      cd frontend && npm ci && npm run dev
      ```
- [ ] At least one custom agent + one custom skill, documented in
      `AGENTS_AND_SKILLS.md`. ✅ included here — `InvoiceAgent` +
      9 skills, all real and already in your codebase.
- [ ] A green CI/CD pipeline — the most recent Actions run passes.
      Check this *after* step 2 above, right before you submit the
      link. A workflow that passed yesterday doesn't count if your
      latest push broke it.

## 4. Optional but scored: deploy the backend

The frontend already defaults to
`https://hackathon-xhw8.onrender.com` and falls back to offline demo
mode if that's unreachable, so the app is demoable either way. If you
want the real backend live for the demo:

1. render.com → New → Web Service → paste your public repo URL.
2. Root directory: `InvoicePilot_AI_Stabilized_v4/Agentic_Ai`
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app.api.main:app --host 0.0.0.0 --port $PORT`
5. Add at least one of `GEMINI_API_KEY` / `GROQ_API_KEY` /
   `NVIDIA_API_KEY` as an environment variable — never commit these.
6. Once it's live, update the default in
   `frontend/src/InvoicePilotAI.jsx` (search `apiBase`) and
   `frontend/e2e/fixtures.ts` (`BACKEND_ORIGIN`) if the URL changed,
   commit, and let CI re-run.

## 5. What to actually submit

Per the brief: your public repo link, confirmation that CI is green
and Playwright passes (a screenshot of the green Actions tab is
fine), and either a ~3 minute demo video or screenshots of the app
working.

## 6. If you're short on time before the deadline

Priority order if you have to cut something:
1. Get the gate-clearing five green (docs + working code + CI) — this
   is pass/fail, everything else is worth zero without it.
2. Green CI over a live Render deployment — CI green is part of the
   gate; a deployed backend is not (the offline demo mode covers you).
3. Everything else in Group 2 (PRD/user stories, lint config, tagged
   release) is scored but not gating — do these last.
