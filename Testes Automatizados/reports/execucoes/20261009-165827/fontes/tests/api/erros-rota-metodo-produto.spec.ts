import { test } from '../suporte/fixtures';
import { executarCaso } from '../suporte/conferencia';

const exemplos = [
  { metodo: 'GET', endpoint: '/api/produtos/INEXISTENTE', status: 404, codigo: 'PRODUTO_NAO_ENCONTRADO' },
  { metodo: 'GET', endpoint: '/api/rota-inexistente', status: 404, codigo: 'ROTA_NAO_ENCONTRADA' },
  { metodo: 'POST', endpoint: '/api/produtos', status: 405, codigo: 'METODO_NAO_PERMITIDO' },
  { metodo: 'GET', endpoint: '/api/carrinho/calcular', status: 405, codigo: 'METODO_NAO_PERMITIDO' },
  { metodo: 'GET', endpoint: '/api/pedidos', status: 405, codigo: 'METODO_NAO_PERMITIDO' },
];

for (const [index, exemplo] of exemplos.entries()) {
  test(`Erros de rota: ${exemplo.metodo} ${exemplo.endpoint}`, { tag: '@api' }, async ({ request }, info) => {
    await executarCaso(info, 'erros-rota-metodo-produto', `${index + 1}-${exemplo.codigo.toLowerCase()}`, async s => {
      const resposta = await s.api(request, 'api', exemplo.metodo, exemplo.endpoint);
      s.comparar('API', 'Status da resposta', exemplo.status, resposta.status);
      s.comparar('API', 'Resposta JSON', true, resposta.headers.some(h => h.name.toLowerCase() === 'content-type' && h.value.includes('application/json')));
      s.comparar('API', 'Código do erro', exemplo.codigo, resposta.dados.erro?.codigo);
      s.comparar('API', 'Mensagem do erro preenchida', true, typeof resposta.dados.erro?.mensagem === 'string' && resposta.dados.erro.mensagem.length > 0);
      s.comparar('API', 'Formato documentado inclui campo relacionado', true, Object.hasOwn(resposta.dados.erro ?? {}, 'campo'));
      s.observacoes.push('O relatório original exige campo no formato comum. A documentação não esclarece a omissão desse campo em erros de rota e método; manter essa dúvida para Produto.');
    });
  });
}
