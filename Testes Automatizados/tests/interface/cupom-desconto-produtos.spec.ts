import { test } from '../suporte/fixtures';
import { executarCaso } from '../suporte/conferencia';
import { aplicarCupom, conferirResumo, prepararCarrinho, valorDaTela } from '../suporte/carrinho';

test('Aplicar desconto apenas aos produtos e exibir a mensagem do BDD', { tag: ['@interface', '@CA01', '@CA09'] }, async ({ page, request, browser }, info) => {
  await executarCaso(info, 'cupom-desconto-produtos', 'bemvindo10-P005-1', async s => {
    s.observacoes.push(`Navegador: Chromium ${browser.version()}; mensagem comparada literalmente com o BDD.`);
    const corpo = { itens: [{ produtoId: 'P005', quantidade: 1 }], cupom: 'BEMVINDO10' };
    const esperado = { subtotal: 100, desconto: 10, frete: 19.9, total: 109.9 };
    const mensagem = 'Cupom aplicado: 10% de desconto nos produtos.';
    const api = await s.api(request, 'api-independente', 'POST', '/api/carrinho/calcular', corpo);
    s.comparar('API independente', 'Status', 200, api.status);
    conferirResumo(s, 'API independente', esperado, api.dados);
    s.comparar('API independente', 'Mensagem do cupom', mensagem, api.dados.cupom?.mensagem);
    await prepararCarrinho(page, corpo.itens);
    await s.tela(page, 'antes-do-cupom');
    const resposta = await aplicarCupom(page);
    const usado = await s.capturarHTTP('api-interface', resposta, resposta.request().postDataJSON());
    conferirResumo(s, 'API usada pela interface', esperado, usado.dados);
    const estado = await s.tela(page, 'depois-do-cupom');
    for (const [campo, valor] of Object.entries(esperado)) s.comparar('Interface', campo, valor, valorDaTela(estado.valores[campo]));
    const mensagens = await page.locator('[role="status"], [role="alert"]').allTextContents();
    await s.json('mensagens-interface.json', mensagens);
    s.comparar('Interface', 'Mensagem exigida pelo BDD exibida na tela', true, estado.textoTela.includes(mensagem));
    s.comparar('Interface', 'Um cupom aplicado', 1, estado.quantidadeCupons);
  });
});
