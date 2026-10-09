import { test } from '../suporte/fixtures';
import { executarCaso } from '../suporte/conferencia';

for (const cep of ['01310-100', '01310100']) {
  test(`Pedido com CEP ${cep}`, { tag: '@api' }, async ({ request }, info) => {
    await executarCaso(info, 'pedido-cep-formatos', cep.includes('-') ? 'com-hifen' : 'sem-hifen', async s => {
      const corpo = { cliente: { nome: 'Maria Silva', email: 'maria@exemplo.com', cep }, itens: [{ produtoId: 'P005', quantidade: 1 }] };
      const resposta = await s.api(request, 'api', 'POST', '/api/pedidos', corpo);
      s.comparar('API', 'Pedido confirmado', 201, resposta.status);
      s.comparar('API', 'CEP normalizado, incluindo zero inicial', '01310100', resposta.dados.cliente?.cep);
      s.comparar('API', 'Produto e quantidade', [{ produtoId: 'P005', quantidade: 1 }], resposta.dados.itens?.map((i: any) => ({ produtoId: i.produtoId, quantidade: i.quantidade })));
    });
  });
}
