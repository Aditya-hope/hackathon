import { test as base, expect } from "@playwright/test";

/**
 * The frontend's hardcoded default API base (see the `apiBase`
 * useState in InvoicePilotAI.jsx). Every backend call the app makes
 * — health checks, invoice processing, approvals, chat — goes to
 * this origin unless the user changes it in Settings.
 */
export const BACKEND_ORIGIN = "https://hackathon-xhw8.onrender.com";

/**
 * A `test` that always intercepts and aborts calls to the live
 * backend before the page loads.
 *
 * Why: the real backend is a separate deployment (Render) that may
 * be asleep, unreachable from a CI runner, or missing LLM provider
 * keys. Rather than depend on that, these tests exercise the app's
 * own first-class offline/demo path — sample-data invoice
 * processing, a mock approval queue, and mock Copilot answers —
 * which exists in the app specifically so the console is fully
 * demoable without a live backend. That makes the suite
 * deterministic and safe to run in CI with zero secrets.
 */
export const test = base.extend({
  page: async ({ page }, use) => {
    await page.route(`${BACKEND_ORIGIN}/**`, (route) => route.abort());
    await use(page);
  },
});

export { expect };
