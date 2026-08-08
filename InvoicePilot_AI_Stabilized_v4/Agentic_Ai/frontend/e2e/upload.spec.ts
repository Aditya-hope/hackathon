import path from "node:path";
import { fileURLToPath } from "node:url";
import { test, expect } from "./fixtures";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

test.describe("Upload & Process", () => {
  test("processes an invoice with sample data end to end", async ({ page }) => {
    await page.goto("/");
    await page.locator("nav").getByText("Upload & Process", { exact: true }).click();

    // Nothing queued yet — the primary action is disabled.
    await expect(page.getByRole("button", { name: /^Run the agent/ })).toBeDisabled();

    const fixture = path.join(__dirname, "fixtures", "sample-invoice.txt");
    await page.locator('input[type="file"]').setInputFiles(fixture);

    await expect(page.getByText("sample-invoice.txt")).toBeVisible();
    await expect(page.getByRole("button", { name: /^Run the agent/ })).toBeEnabled();

    // Backend is offline (see fixtures.ts), so the sample-data path
    // is what's available — it runs entirely client-side.
    await page.getByRole("button", { name: "Try with sample data" }).click();

    // Pipeline trace animates through the nine skills, then the
    // batch-summary card appears.
    await expect(page.getByText(/1 of 1 processed successfully\./)).toBeVisible({ timeout: 15_000 });

    await page.getByRole("button", { name: "View latest result" }).click();

    // Results page: recommendation/risk badges and extracted fields.
    await expect(page.getByRole("button", { name: "New invoice" })).toBeVisible();
    await expect(page.getByRole("button", { name: "Ask AI Copilot" })).toBeVisible();
    await expect(page.getByText("Provider used")).toBeVisible();
    await expect(page.getByText("Validation status")).toBeVisible();
  });

  test("shows a per-invoice error when running against an unreachable backend", async ({ page }) => {
    await page.goto("/");
    await page.locator("nav").getByText("Upload & Process", { exact: true }).click();

    const fixture = path.join(__dirname, "fixtures", "sample-invoice.txt");
    await page.locator('input[type="file"]').setInputFiles(fixture);

    // "Run the agent" (as opposed to the sample-data button) makes a
    // real network call, which fixtures.ts aborts — the app should
    // surface that as a clear per-item failure rather than hanging
    // or crashing.
    await page.getByRole("button", { name: /^Run the agent/ }).click();

    await expect(page.getByText(/need attention/)).toBeVisible({ timeout: 15_000 });
    await expect(page.getByText(/processed successfully\./)).toBeVisible();
  });

  test("rejects an unsupported file type before it's queued", async ({ page }) => {
    await page.goto("/");
    await page.locator("nav").getByText("Upload & Process", { exact: true }).click();

    // Build a throwaway .json file on the fly — not in SUPPORTED_TYPES.
    await page.setInputFiles('input[type="file"]', {
      name: "not-an-invoice.json",
      mimeType: "application/json",
      buffer: Buffer.from("{}"),
    });

    // The filename is expected to appear alongside the error message
    // itself (e.g. "not-an-invoice.json: Unsupported file type ...") —
    // what matters is that the file was never queued for processing.
    await expect(page.getByText(/Unsupported file type/)).toBeVisible();
    await expect(page.getByRole("button", { name: /^Run the agent/ })).toBeDisabled();
  });

  test("supports pasted invoice text as an alternative to a file", async ({ page }) => {
    await page.goto("/");
    await page.locator("nav").getByText("Upload & Process", { exact: true }).click();

    await page.getByRole("button", { name: "Paste / type text" }).click();
    await page.getByRole("button", { name: "Add an invoice text block" }).click();

    await page.locator("textarea").fill(
      "Vendor: Northwind Logistics\nInvoice Number: INV-77012\nTotal: 12,400.00 USD"
    );

    await page.getByRole("button", { name: "Try with sample data" }).click();
    await expect(page.getByText(/1 of 1 processed successfully\./)).toBeVisible({ timeout: 15_000 });
  });
});
