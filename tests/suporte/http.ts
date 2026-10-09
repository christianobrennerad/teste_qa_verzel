import type { APIRequestContext, TestInfo } from '@playwright/test';

// Registra os dados antes das comparações para preservar evidências de falhas.
export async function enviarPost(
  request: APIRequestContext,
  testInfo: TestInfo,
  endpoint: string,
  corpo: Record<string, unknown>,
) {
  const inicio = new Date().toISOString();
  await testInfo.attach('requisicao.json', {
    body: JSON.stringify(
      { inicio, metodo: 'POST', endpoint, corpo },
      null,
      2,
    ),
    contentType: 'application/json',
  });

  const resposta = await request.post(endpoint, { data: corpo });
  const corpoRecebido = await resposta.text();

  await testInfo.attach('resposta-http.json', {
    body: JSON.stringify(
      {
        inicio,
        fim: new Date().toISOString(),
        url: resposta.url(),
        status: resposta.status(),
        statusText: resposta.statusText(),
        cabecalhos: resposta.headersArray(),
        corpoRecebido,
      },
      null,
      2,
    ),
    contentType: 'application/json',
  });
  await testInfo.attach('corpo-recebido.json', {
    body: corpoRecebido,
    contentType: 'application/json',
  });

  return resposta;
}
