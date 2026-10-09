import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  timeout: 30_000,
  expect: { timeout: 5_000 },
  workers: 1,
  retries: 0,
  forbidOnly: Boolean(process.env.CI),
  outputDir: 'test-results',
  reporter: [
    ['list'],
    ['html', { open: 'never', outputFolder: 'playwright-report' }],
    ['json', { outputFile: 'test-results/resultados.json' }],
  ],
  use: {
    baseURL:
      process.env.BASE_URL ??
      'https://verzel-store.qa-test-verzel-store.workers.dev',
    extraHTTPHeaders: { 'Content-Type': 'application/json' },
  },
  projects: [{ name: 'api', testMatch: '**/api/*.spec.ts' }],
});
