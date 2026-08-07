import { test, expect } from "./fixtures";

test.describe("Dashboard", () => {
  test("loads with the sidebar, an offline indicator, and an empty state", async ({ page }) => {
    await page.goto("/");

    await expect(page.getByRole("heading", { name: "Dashboard" })).toBeVisible();

    // Primary navigation.
    const nav = page.locator("nav");
    for (const label of ["Dashboard", "Upload & Process", "AI Copilot", "Approval Queue", "History"]) {
      await expect(nav.getByText(label, { exact: true })).toBeVisible();
    }

    // The backend call to the live Render service is aborted (see
    // fixtures.ts), so the app should settle into its offline state.
    await expect(page.getByText("Backend offline")).toBeVisible();
    await expect(page.getByText("Backend not reachable.")).toBeVisible();

    // Nothing processed yet this session.
    await expect(page.getByText("No invoices processed yet")).toBeVisible();
    await expect(page.getByText("Processed this session")).toBeVisible();
  });

  test("\"Process an invoice\" navigates to the Upload page", async ({ page }) => {
    await page.goto("/");
    await page.getByRole("button", { name: "Process an invoice" }).click();
    await expect(page.getByRole("heading", { name: "Upload & process" })).toBeVisible();
  });

  test("sidebar links switch pages", async ({ page }) => {
    await page.goto("/");
    const nav = page.locator("nav");

    await nav.getByText("Approval Queue", { exact: true }).click();
    await expect(page.getByRole("heading", { name: "Approval queue" })).toBeVisible();

    await nav.getByText("History", { exact: true }).click();
    await expect(page.getByRole("heading", { name: "History" })).toBeVisible();

    await nav.getByText("Dashboard", { exact: true }).click();
    await expect(page.getByRole("heading", { name: "Dashboard" })).toBeVisible();
  });
});
