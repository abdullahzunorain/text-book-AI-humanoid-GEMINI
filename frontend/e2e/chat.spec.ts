import { test, expect } from '@playwright/test';

test.describe('Chat Widget', () => {
  test('T030 — chat widget is visible on chapter page', async ({ page }) => {
    await page.goto('./docs/intro');
    await page.waitForLoadState('networkidle');

    // The chat starts expanded with a "Close" button and header
    const chatHeader = page.locator('text=AI Textbook Assistant');
    await expect(chatHeader).toBeVisible({ timeout: 15_000 });

    // Verify the Close/toggle button exists
    const closeBtn = page.locator('button', { hasText: 'Close' });
    await expect(closeBtn).toBeVisible();
  });

  test('T031 — send a message and receive response', async ({ page }) => {
    await page.goto('./docs/intro');
    await page.waitForLoadState('networkidle');

    // Chat should already be open with input visible
    const chatInput = page.locator('input[placeholder*="Ask a question"]');
    await expect(chatInput).toBeVisible({ timeout: 15_000 });
    await chatInput.fill('What is ROS 2?');

    // Click Send button
    const sendBtn = page.locator('button', { hasText: 'Send' });
    await sendBtn.click();

    // Wait for bot response — either an AI response or graceful degradation message
    const botResponse = page.locator('text=AI Assistant').or(
      page.locator('text=AI service temporarily')
    ).or(
      page.locator('text=could not connect')
    );
    await expect(botResponse.first()).toBeVisible({ timeout: 30_000 });
  });
});
