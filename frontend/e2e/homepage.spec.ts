import { test, expect } from '@playwright/test';

test.describe('Homepage & Navigation', () => {
  test('T028 — homepage loads with correct title and module links', async ({ page }) => {
    await page.goto('./');
    await page.waitForLoadState('networkidle');

    await expect(page).toHaveTitle(/Physical AI|Humanoid|AI Humanoid/i);

    // Module links use the full base path: /text-book-AI-humanoid/docs/module-*
    const moduleLinks = page.locator('a[href*="/docs/module-"]');
    await expect(moduleLinks.first()).toBeVisible({ timeout: 15_000 });
    const count = await moduleLinks.count();
    expect(count).toBeGreaterThanOrEqual(4);
  });

  test('T029 — clicking a module link loads chapter content', async ({ page }) => {
    await page.goto('./');
    await page.waitForLoadState('networkidle');

    const firstModuleLink = page.locator('a[href*="/docs/module-"]').first();
    await expect(firstModuleLink).toBeVisible({ timeout: 15_000 });
    await firstModuleLink.click();

    // Verify chapter page loaded with content
    await page.waitForLoadState('networkidle');
    const article = page.locator('article, .theme-doc-markdown, main');
    await expect(article.first()).toBeVisible({ timeout: 15_000 });
  });
});
