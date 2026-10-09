import { test } from '../suporte/fixtures';
import { executarCaso } from '../suporte/conferencia';

for (const operacao of ['calculo', 'pedido']) {
  test(`Produto duplicado: ${operacao}`, { tag: ['@api', '@CA10'] }, async ({ request }, info) => {
    await executarCaso(info, 'produto-duplicado-api', operacao, async s => {
      const corpo = {
        itens: [{ produtoId: 'P001', quantidade: 3 }, { produtoId: 'P001', quantidade: 3 }],
        ...(operacao === 'pedido' ? { cliente: { nome: 'Cliente Teste', email: 'qa@example.com', cep: '01310-100' } } : {}),
      };
      const resposta = await s.api(request, 'api', 'POST', operacao === 'pedido' ? '/api/pedidos' : '/api/carrinho/calcular', corpo);
      s.comparar('API', 'Requisição recusada', 422, resposta.status);
      s.comparar('API', 'Código de duplicidade', 'ITEM_DUPLICADO', resposta.dados.erro?.codigo);
      s.comparar('API', 'Sem confirmação de pedido', false, Object.hasOwn(resposta.dados, 'numero') || Object.hasOwn(resposta.dados, 'criadoEm'));
    });
  });
}
