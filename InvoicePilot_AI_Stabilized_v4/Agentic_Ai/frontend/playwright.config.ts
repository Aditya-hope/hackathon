import { defineConfig, devices } from "@playwright/test";

/**
 * Playwright config for the InvoicePilot AI console.
 *
 * The app is a static Vite/React SPA, so tests run against a
 * production build served by `vite preview`. Playwright starts
 * that server itself (see `webServer` below) and waits for it to
 * respond before running any test.
 *
 * These tests never depend on the live backend (the deployed
 * Render service): every test runs the UI through its built-in
 * offline/demo mode instead (see e2e/fixtures.ts). That keeps the
 * suite fast, deterministic, and safe to run in CI with no API
 * keys or network access to third-party services.
 */
export default defineConfig({
  testDir: "./e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  workers: process.env.CI ? 1 : undefined,

  // The HTML report is what gets uploaded as a CI artifact (see
  // .github/workflows/e2e-tests.yml). `open: never` keeps a local
  // `npx playwright test` run from popping a browser tab.
  reporter: [
    ["html", { outputFolder: "playwright-report", open: "never" }],
    ["list"],
  ],

  use: {
    baseURL: "http://localhost:4173",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
    video: "retain-on-failure",
  },

  webServer: {
    command: "npm run preview -- --port 4173 --strictPort",
    url: "http://localhost:4173",
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
  },

  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],
});
