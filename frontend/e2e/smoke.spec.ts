import { expect, test } from "@playwright/test";

// Runs on both desktop and mobile projects — assumption 2 requires responsive design.
test("home page renders the title", async ({ page }) => {
  await page.goto("/");

  await expect(page.getByRole("heading", { name: /sports tournament/i })).toBeVisible();
});
