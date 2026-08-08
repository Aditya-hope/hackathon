import { test, expect } from "./fixtures";
import { processSampleInvoice } from "./helpers";

test.describe("AI Copilot", () => {
  test("shows an empty state until an invoice has been processed", async ({ page }) => {
    await page.goto("/");
    await page.locator("nav").getByText("AI Copilot", { exact: true }).click();

    await expect(page.getByText("Nothing to ask about yet")).toBeVisible();
  });

  test("answers a suggested question about the processed invoice in demo mode", async ({ page }) => {
    await processSampleInvoice(page);

    await page.getByRole("button", { name: "Ask AI Copilot" }).click();
    await expect(page.getByRole("heading", { name: "AI Copilot" })).toBeVisible();
    await expect(page.getByText("Demo mode")).toBeVisible();

    await page.getByRole("button", { name: "Summarize this invoice" }).click();

    // User turn renders first, then the assistant's mock answer.
    await expect(page.locator(".ip-chat-user").getByText("Summarize this invoice", { exact: true })).toBeVisible();
    await expect(page.getByText(/billed/)).toBeVisible({ timeout: 10_000 });
  });

  test("free-typed questions are answered too", async ({ page }) => {
    await processSampleInvoice(page);
    await page.locator("nav").getByText("AI Copilot", { exact: true }).click();

    const input = page.getByPlaceholder("Ask about this invoice…");
    await input.fill("Explain the risk score for this one");
    await input.press("Enter");

    await expect(page.getByText(/risk score of/)).toBeVisible({ timeout: 10_000 });
  });
});
