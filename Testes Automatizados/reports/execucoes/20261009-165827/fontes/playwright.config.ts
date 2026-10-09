import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  timeout: 60_000,
  expect: { timeout: 5_000 },
  workers: 1,
  retries: 0,
  forbidOnly: Boolean(process.env.CI),
  outputDir: process.env.PLAYWRIGHT_OUTPUT_DIR ?? 'test-results',
  reporter: [
    ['list'],
    ['html', { open: 'never', outputFolder: process.env.PLAYWRIGHT_REPORT_DIR ?? 'playwright-report' }],
    ['json', { outputFile: process.env.PLAYWRIGHT_RESULTS_FILE ?? 'test-results/resultados.json' }],
  ],
  use: {
    baseURL:
      process.env.BASE_URL ??
      'https://verzel-store.qa-test-verzel-store.workers.dev',
    extraHTTPHeaders: { 'Content-Type': 'application/json' },
    ignoreHTTPSErrors: false,
    locale: 'pt-BR',
    viewport: { width: 1280, height: 1000 },
  },
  projects: [
    { name: 'api', testMatch: '**/api/*.spec.ts' },
    { name: 'interface-chromium', testMatch: '**/interface/*.spec.ts', use: { browserName: 'chromium' } },
  ],
});
