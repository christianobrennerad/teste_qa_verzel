import { test, expect } from '../suporte/fixtures';
import { enviarPost } from '../suporte/http';

// BDD: features/quantidades_e_itens.feature — Aceitar os limites válidos de quantidade.
const exemplos = [
  { operacao: 'calcular', endpoint: '/api/carrinho/calcular', quantidade: 1, status: 200, subtotal: 50 },
  { operacao: 'calcular', endpoint: '/api/carrinho/calcular', quantidade: 5, status: 200, subtotal: 250 },
  { operacao: 'confirmar', endpoint: '/api/pedidos', quantidade: 1, status: 201, subtotal: 50 },
  { operacao: 'confirmar', endpoint: '/api/pedidos', quantidade: 5, status: 201, subtotal: 250 },
];

for (const exemplo of exemplos) {
  test(`Aceitar ${exemplo.quantidade} unidade(s) de P008 ao ${exemplo.operacao}`, {
    tag: ['@api', '@CA10'],
  }, async ({ request }, testInfo) => {
    // Dado um cliente fictício válido e a quantidade indicada no exemplo.
    const corpo = {
      cliente: { nome: 'Cliente Teste', email: 'qa@example.com', cep: '01310-100' },
      itens: [{ produtoId: 'P008', quantidade: exemplo.quantidade }],
    };

    // Quando envio a requisição para a operação correspondente.
    const resposta = await enviarPost(request, testInfo, exemplo.endpoint, corpo);

    // Então verifico os valores esperados deste exemplo.
    expect(resposta.status()).toBe(exemplo.status);
    expect(resposta.headers()['content-type']).toContain('application/json');
    const dados = await resposta.json();
    expect(dados.subtotal).toBe(exemplo.subtotal);
    expect(dados.itens).toHaveLength(1);
    expect(dados.itens[0]).toMatchObject({
      produtoId: 'P008',
      quantidade: exemplo.quantidade,
    });
  });
}
