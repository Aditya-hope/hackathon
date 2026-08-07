import path from "node:path";
import { fileURLToPath } from "node:url";
import type { Page } from "@playwright/test";
import { expect } from "./fixtures";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

/**
 * Drives the "Upload & Process" page end to end using a real file
 * and the app's offline "Try with sample data" path, then returns
 * once the Results page for that invoice is showing.
 *
 * Several specs (History, Copilot) need at least one processed
 * invoice to exist before they can test anything, so this is
 * factored out rather than repeated in every spec.
 */
export async function processSampleInvoice(page: Page) {
  await page.goto("/");
  await page.locator("nav").getByText("Upload & Process", { exact: true }).click();
  await expect(page.getByRole("heading", { name: "Upload & process" })).toBeVisible();

  const fixture = path.join(__dirname, "fixtures", "sample-invoice.txt");
  // The dropzone's <input type="file"> is visually hidden but still
  // reachable via setInputFiles, which doesn't require it to be
  // visible.
  await page.locator('input[type="file"]').setInputFiles(fixture);

  await expect(page.getByText("sample-invoice.txt")).toBeVisible();

  await page.getByRole("button", { name: "Try with sample data" }).click();

  // Batch summary card appears once the (simulated) run finishes.
  await expect(page.getByText(/processed successfully\.?$/)).toBeVisible({ timeout: 15_000 });

  await page.getByRole("button", { name: "View latest result" }).click();
  await expect(page.getByRole("button", { name: "New invoice" })).toBeVisible();
}
