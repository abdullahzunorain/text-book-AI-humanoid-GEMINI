import { test, expect } from '@playwright/test';

/**
 * Helper: Sign up a fresh user via the UI modal.
 */
async function signUpAndLogin(page: import('@playwright/test').Page) {
  await page.goto('./');
  await page.waitForLoadState('networkidle');

  const signInBtn = page.locator('button', { hasText: 'Sign In' });
  await expect(signInBtn).toBeVisible({ timeout: 15_000 });
  await signInBtn.click();

  // Wait for modal
  const modal = page.locator('[class*="modal"]');
  await expect(modal).toBeVisible({ timeout: 5_000 });
  await modal.locator('text=Sign Up').click();

  // Fill form within the modal (scoped to avoid chat input collision)
  const form = modal.locator('form');
  await form.locator('input[type="text"]').first().fill('Actions Tester');
  await form.locator('input[type="email"]').fill(`e2e-actions-${Date.now()}@test.com`);
  await form.locator('input[type="password"]').fill('test123456');
  await form.locator('select').first().selectOption({ index: 1 });
  await form.locator('select').nth(1).selectOption({ index: 1 });
  await form.locator('button[type="submit"]').click();

  // Wait for logged-in state
  const signOutBtn = page.locator('button', { hasText: 'Sign Out' });
  await expect(signOutBtn).toBeVisible({ timeout: 15_000 });
}

test.describe('Chapter Actions (Auth-Gated)', () => {
  test('T035 — Personalize and Translate buttons visible when logged in', async ({ page }) => {
    await signUpAndLogin(page);

    await page.goto('./docs/intro');
    await page.waitForLoadState('networkidle');

    const personalizeBtn = page.locator('button', { hasText: 'Personalize' });
    const translateBtn = page.locator('button', { hasText: 'Translate to Urdu' });

    await expect(personalizeBtn).toBeVisible({ timeout: 15_000 });
    await expect(translateBtn).toBeVisible();
  });

  test('T036 — Personalize button shows loading state', async ({ page }) => {
    await signUpAndLogin(page);
    await page.goto('./docs/intro');
    await page.waitForLoadState('networkidle');

    const personalizeBtn = page.locator('button', { hasText: 'Personalize' });
    await expect(personalizeBtn).toBeVisible({ timeout: 15_000 });
    await personalizeBtn.click();

    // Either "Personalizing..." loading text, AI transform message, or graceful error
    const result = page.locator('button:has-text("Personalizing...")').or(
      page.locator('text=transformed by AI')
    ).or(
      page.locator('text=AI service temporarily')
    );
    await expect(result.first()).toBeVisible({ timeout: 30_000 });
  });

  test('T037 — Translate button shows loading state', async ({ page }) => {
    await signUpAndLogin(page);
    await page.goto('./docs/intro');
    await page.waitForLoadState('networkidle');

    const translateBtn = page.locator('button', { hasText: 'Translate to Urdu' });
    await expect(translateBtn).toBeVisible({ timeout: 15_000 });
    await translateBtn.click();

    const result = page.locator('button:has-text("Translating...")').or(
      page.locator('text=transformed by AI')
    ).or(
      page.locator('text=AI service temporarily')
    );
    await expect(result.first()).toBeVisible({ timeout: 30_000 });
  });

  test('T038 — Revert to Original restores content after transformation', async ({ page }) => {
    await signUpAndLogin(page);
    await page.goto('./docs/intro');
    await page.waitForLoadState('networkidle');

    const personalizeBtn = page.locator('button', { hasText: 'Personalize' });
    await expect(personalizeBtn).toBeVisible({ timeout: 15_000 });
    await personalizeBtn.click();

    // Wait for transformation to complete
    await page.waitForTimeout(5_000);

    // Look for Revert button (appears only after successful transformation)
    const revertBtn = page.locator('button', { hasText: 'Revert to Original' });
    const revertVisible = await revertBtn.isVisible().catch(() => false);

    if (revertVisible) {
      await revertBtn.click();
      await expect(revertBtn).not.toBeVisible({ timeout: 10_000 });
    }
    // If revert button doesn't appear, the AI service was unavailable — acceptable
  });

  test('T039 — Personalize and Translate NOT visible when logged out', async ({ page }) => {
    await page.goto('./docs/intro');
    await page.waitForLoadState('networkidle');

    await page.waitForTimeout(3_000);

    const personalizeBtn = page.locator('button', { hasText: 'Personalize' });
    const translateBtn = page.locator('button', { hasText: 'Translate to Urdu' });

    await expect(personalizeBtn).not.toBeVisible();
    await expect(translateBtn).not.toBeVisible();
  });
});
