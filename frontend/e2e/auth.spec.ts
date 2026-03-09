import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
  test('T032 — Sign In button opens auth modal with two tabs', async ({ page }) => {
    await page.goto('./');
    await page.waitForLoadState('networkidle');

    const signInBtn = page.locator('button', { hasText: 'Sign In' });
    await expect(signInBtn).toBeVisible({ timeout: 15_000 });
    await signInBtn.click();

    // Modal should have Sign In and Sign Up tabs
    const modal = page.locator('[class*="modal"]');
    await expect(modal).toBeVisible({ timeout: 5_000 });

    const signUpTab = modal.locator('text=Sign Up');
    await expect(signUpTab).toBeVisible();
  });

  test('T033 — Sign Up creates new user and shows logged-in state', async ({ page }) => {
    await page.goto('./');
    await page.waitForLoadState('networkidle');

    const signInBtn = page.locator('button', { hasText: 'Sign In' });
    await expect(signInBtn).toBeVisible({ timeout: 15_000 });
    await signInBtn.click();

    // Wait for modal to appear
    const modal = page.locator('[class*="modal"]');
    await expect(modal).toBeVisible({ timeout: 5_000 });

    // Switch to Sign Up tab
    await modal.locator('text=Sign Up').click();

    // Fill form within the modal
    const form = modal.locator('form');
    await form.locator('input[type="text"]').first().fill('Playwright Tester');
    await form.locator('input[type="email"]').fill(`e2e-playwright-${Date.now()}@test.com`);
    await form.locator('input[type="password"]').fill('test123456');
    await form.locator('select').first().selectOption({ index: 1 });
    await form.locator('select').nth(1).selectOption({ index: 1 });

    // Submit
    await form.locator('button[type="submit"]').click();

    // Verify user is logged in — Sign Out button appears
    const signOutBtn = page.locator('button', { hasText: 'Sign Out' });
    await expect(signOutBtn).toBeVisible({ timeout: 15_000 });
  });

  test('T034 — Sign Out then Sign In works', async ({ page }) => {
    await page.goto('./');
    await page.waitForLoadState('networkidle');

    // Sign up first
    const signInBtn = page.locator('button', { hasText: 'Sign In' });
    await expect(signInBtn).toBeVisible({ timeout: 15_000 });
    await signInBtn.click();

    const modal = page.locator('[class*="modal"]');
    await expect(modal).toBeVisible({ timeout: 5_000 });
    await modal.locator('text=Sign Up').click();

    const uniqueEmail = `e2e-signout-${Date.now()}@test.com`;

    const form = modal.locator('form');
    await form.locator('input[type="text"]').first().fill('SignOut Tester');
    await form.locator('input[type="email"]').fill(uniqueEmail);
    await form.locator('input[type="password"]').fill('test123456');
    await form.locator('select').first().selectOption({ index: 1 });
    await form.locator('select').nth(1).selectOption({ index: 1 });
    await form.locator('button[type="submit"]').click();

    // Wait for logged-in state
    const signOutBtn = page.locator('button', { hasText: 'Sign Out' });
    await expect(signOutBtn).toBeVisible({ timeout: 15_000 });

    // Sign out
    await signOutBtn.click();

    // Verify Sign In button is back
    const signInBtnAfter = page.locator('button', { hasText: 'Sign In' });
    await expect(signInBtnAfter).toBeVisible({ timeout: 10_000 });

    // Sign in with the same email
    await signInBtnAfter.click();

    const modalSignIn = page.locator('[class*="modal"]');
    await expect(modalSignIn).toBeVisible({ timeout: 5_000 });

    // Ensure we're on the Sign In tab (not Sign Up)
    const signInTab = modalSignIn.locator('button', { hasText: 'Sign In' }).first();
    await signInTab.click();

    const signInForm = modalSignIn.locator('form');
    await signInForm.locator('input[type="email"]').fill(uniqueEmail);
    await signInForm.locator('input[type="password"]').fill('test123456');
    await signInForm.locator('button[type="submit"]').click();

    // Verify logged in again
    const signOutBtnAfter = page.locator('button', { hasText: 'Sign Out' });
    await expect(signOutBtnAfter).toBeVisible({ timeout: 15_000 });
  });
});
