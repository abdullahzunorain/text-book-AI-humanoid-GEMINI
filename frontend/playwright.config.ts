import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: false,
  workers: 1,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  reporter: 'html',
  timeout: 60_000,

  use: {
    baseURL: 'http://localhost:3000/text-book-AI-humanoid/',
    headless: false,
    screenshot: 'only-on-failure',
    trace: 'on-first-retry',
    launchOptions: {
      slowMo: 500,
    },
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],

  webServer: [
    {
      command: 'cd ../backend && uv run uvicorn src.main:app --host 0.0.0.0 --port 8000',
      url: 'http://localhost:8000/health',
      reuseExistingServer: true,
      timeout: 30_000,
    },
    {
      command: 'npm start -- --port 3000',
      url: 'http://localhost:3000/text-book-AI-humanoid/',
      reuseExistingServer: true,
      timeout: 60_000,
    },
  ],
});
