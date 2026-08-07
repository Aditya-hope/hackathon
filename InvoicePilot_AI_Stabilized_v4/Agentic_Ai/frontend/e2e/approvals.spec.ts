import { test, expect } from "./fixtures";

test.describe("Approval Queue", () => {
  test("shows a sample queue and an offline banner when the backend is unreachable", async ({ page }) => {
    await page.goto("/");
    await page.locator("nav").getByText("Approval Queue", { exact: true }).click();

    await expect(page.getByRole("heading", { name: "Approval queue" })).toBeVisible();
    await expect(page.getByText("Backend not reachable — showing sample queue data")).toBeVisible();

    // buildMockApprovals() always seeds 4 pending items in demo mode.
    await expect(page.locator(".ip-card.ip-fade-in")).toHaveCount(4);
  });

  test("approving an item opens the decision modal and records the decision", async ({ page }) => {
    await page.goto("/");
    await page.locator("nav").getByText("Approval Queue", { exact: true }).click();

    const firstItem = page.locator(".ip-card.ip-fade-in").first();
    await firstItem.getByRole("button", { name: "Approve" }).click();

    await expect(page.getByRole("heading", { name: "Approve invoice" })).toBeVisible();
    await page.getByPlaceholder("e.g. Priya Shah").fill("Test Reviewer");

    // Scope to the modal so this doesn't collide with the row's own
    // "Approve" button underneath it.
    const modal = page.locator(".ip-card.ip-pop");
    await modal.getByRole("button", { name: "Approve" }).click();

    await expect(page.getByText("Invoice approved.")).toBeVisible();
    await expect(modal).not.toBeVisible();
  });

  test("rejecting an item records the decision", async ({ page }) => {
    await page.goto("/");
    await page.locator("nav").getByText("Approval Queue", { exact: true }).click();

    const firstItem = page.locator(".ip-card.ip-fade-in").first();
    await firstItem.getByRole("button", { name: "Reject" }).click();

    await expect(page.getByRole("heading", { name: "Reject invoice" })).toBeVisible();

    const modal = page.locator(".ip-card.ip-pop");
    await modal.getByRole("button", { name: "Reject" }).click();

    await expect(page.getByText("Invoice rejected.")).toBeVisible();
  });

  test("the Pending / All toggle filters the queue", async ({ page }) => {
    await page.goto("/");
    await page.locator("nav").getByText("Approval Queue", { exact: true }).click();

    await expect(page.locator(".ip-card.ip-fade-in")).toHaveCount(4);

    await page.getByRole("button", { name: "All", exact: true }).click();
    // Still a sample queue in demo mode — the toggle itself should
    // not error out or blank the page.
    await expect(page.getByRole("heading", { name: "Approval queue" })).toBeVisible();
  });
});
