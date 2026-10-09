import { test, expect } from '../suporte/fixtures';
import { enviarPost } from '../suporte/http';

// BDD: features/quantidades_e_itens.feature — Identificar o campo da quantidade inválida.
test('Identificar o campo da quantidade inválida', { tag: '@api' }, async (
  { request },
  testInfo,
) => {
  // Dado o produto P001 com quantidade zero.
  const corpo = { itens: [{ produtoId: 'P001', quantidade: 0 }] };

  // Quando envio esse corpo para calcular o carrinho.
  const resposta = await enviarPost(
    request,
    testInfo,
    '/api/carrinho/calcular',
    corpo,
  );

  // Então verifico o status, o formato dos dados e os três campos do erro.
  expect(resposta.status()).toBe(422);
  expect(resposta.headers()['content-type']).toContain('application/json');
  const dados = await resposta.json();
  expect(dados.erro.codigo).toBe('QUANTIDADE_INVALIDA');
  expect(dados.erro.mensagem).toBe(
    'A quantidade deve ser um número inteiro maior ou igual a 1.',
  );
  expect(dados.erro.campo).toBe('itens[0].quantidade');
});
