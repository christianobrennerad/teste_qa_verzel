import { test as base, expect } from '@playwright/test';

function proxyDoAmbiente() {
  const address = process.env.HTTPS_PROXY ?? process.env.https_proxy;
  if (!address) return undefined;
  const url = new URL(address);
  return {
    server: url.origin,
    username: url.username ? decodeURIComponent(url.username) : undefined,
    password: url.password ? decodeURIComponent(url.password) : undefined,
  };
}

// A loja é pública. Proxy, quando necessário, vem somente do ambiente.
// As credenciais do proxy não são gravadas na configuração ou nos anexos.
export const test = base.extend({
  browser: [async ({ playwright, browserName }, use) => {
    const browser = await playwright[browserName].launch({
      headless: true,
      executablePath: browserName === 'chromium'
        ? process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH
        : undefined,
      proxy: proxyDoAmbiente(),
    });
    try {
      await use(browser);
    } finally {
      await browser.close();
    }
  }, { scope: 'worker' }],
  request: async ({ playwright, baseURL, extraHTTPHeaders }, use) => {
    const context = await playwright.request.newContext({
      baseURL,
      extraHTTPHeaders,
      timeout: 20_000,
      proxy: proxyDoAmbiente(),
      ignoreHTTPSErrors: false,
    });

    try {
      await use(context);
    } finally {
      await context.dispose();
    }
  },
});

export { expect };
