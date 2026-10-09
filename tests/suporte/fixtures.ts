import { test as base, expect } from '@playwright/test';

// A loja é pública. Proxy, quando necessário, vem somente do ambiente.
// As credenciais do proxy não são gravadas na configuração ou nos anexos.
export const test = base.extend({
  request: async ({ playwright, baseURL, extraHTTPHeaders }, use) => {
    const proxyAddress = process.env.HTTPS_PROXY ?? process.env.https_proxy;
    const proxyURL = proxyAddress ? new URL(proxyAddress) : undefined;
    const proxy = proxyURL
      ? {
          server: `${proxyURL.protocol}//${proxyURL.host}`,
          username: proxyURL.username
            ? decodeURIComponent(proxyURL.username)
            : undefined,
          password: proxyURL.password
            ? decodeURIComponent(proxyURL.password)
            : undefined,
        }
      : undefined;

    const context = await playwright.request.newContext({
      baseURL,
      extraHTTPHeaders,
      timeout: 20_000,
      proxy,
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
