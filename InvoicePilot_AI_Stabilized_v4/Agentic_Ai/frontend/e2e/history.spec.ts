import { test, expect } from "./fixtures";
import { processSampleInvoice } from "./helpers";

test.describe("History", () => {
  test("processed invoices appear in History and reopen the matching result", async ({ page }) => {
    await processSampleInvoice(page);

    await page.locator("nav").getByText("History", { exact: true }).click();
    await expect(page.getByRole("heading", { name: "History" })).toBeVisible();

    const row = page.locator("table tbody tr").first();
    await expect(row).toBeVisible();
    const vendorCell = row.locator("td").first();
    const vendorName = (await vendorCell.textContent())?.trim();
    expect(vendorName).toBeTruthy();

    await row.click();

    // Results page header shows the same vendor name as the History row.
    await expect(page.getByRole("heading", { name: vendorName! })).toBeVisible();
  });

  test("search narrows the History table", async ({ page }) => {
    await processSampleInvoice(page);
    await page.locator("nav").getByText("History", { exact: true }).click();

    await expect(page.locator("table tbody tr")).toHaveCount(1);

    await page.getByPlaceholder("Search vendor or invoice number…").fill("zzz-no-such-vendor-zzz");
    await expect(page.getByText("No matches")).toBeVisible();

    await page.getByPlaceholder("Search vendor or invoice number…").fill("");
    await expect(page.locator("table tbody tr")).toHaveCount(1);
  });

  test("removing an invoice requires a confirm step", async ({ page }) => {
    await processSampleInvoice(page);
    await page.locator("nav").getByText("History", { exact: true }).click();

    const row = page.locator("table tbody tr").first();
    await row.getByTitle("Remove from history").click();

    // First click only arms the confirmation — the row must still
    // be there until the user confirms.
    const confirmBtn = row.getByTitle("Confirm removal");
    await expect(confirmBtn).toBeVisible();
    await expect(page.locator("table tbody tr")).toHaveCount(1);

    await confirmBtn.click();

    await expect(page.getByText("No history yet")).toBeVisible();
  });
});
