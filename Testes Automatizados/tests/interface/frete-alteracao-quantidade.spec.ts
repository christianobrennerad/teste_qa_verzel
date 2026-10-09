import { test } from '../suporte/fixtures';
import { executarCaso } from '../suporte/conferencia';
import { aplicarCupom, conferirResumo, prepararCarrinho, valorDaTela } from '../suporte/carrinho';

test('Frete após alterar quantidade com cupom: 1 para 2 e volta para 1', { tag: ['@interface', '@CA06', '@CA07', '@CA08'] }, async ({ page, browser }, info) => {
  await executarCaso(info, 'frete-alteracao-quantidade', 'quantidade-1-2-1', async s => {
    s.observacoes.push(`Navegador: Chromium ${browser.version()}; alteração pelos controles da tela, sem modificar o armazenamento.`);
    await prepararCarrinho(page, [{ produtoId: 'P005', quantidade: 1 }]);
    const primeira = await aplicarCupom(page);
    for (const [index, quantidade] of [1, 2, 1].entries()) {
      const etapa = `${index + 1}-quantidade-${quantidade}`;
      let resposta = primeira;
      if (index > 0) {
        const recebido = page.waitForResponse(r => r.url().endsWith('/api/carrinho/calcular') && r.request().postDataJSON()?.cupom === 'BEMVINDO10' && r.request().postDataJSON()?.itens?.[0]?.quantidade === quantidade);
        await page.getByRole('button', { name: `${index === 1 ? 'Aumentar' : 'Diminuir'} quantidade de Mochila Urbana 20L`, exact: true }).click();
        resposta = await recebido;
        await page.waitForLoadState('networkidle');
      }
      const recebido = await s.capturarHTTP(`${etapa}-api`, resposta, resposta.request().postDataJSON());
      const estado = await s.tela(page, etapa);
      const esperado = quantidade === 2 ? { subtotal: 200, desconto: 20, frete: 0, total: 180 } : { subtotal: 100, desconto: 10, frete: 19.9, total: 109.9 };
      conferirResumo(s, `API ${etapa}`, esperado, recebido.dados);
      const qtd = (await page.locator('output[aria-label="Quantidade de Mochila Urbana 20L"]').innerText()).trim();
      s.comparar(`Interface ${etapa}`, 'Quantidade de P005', String(quantidade), qtd);
      s.comparar(`Interface ${etapa}`, 'Um único cupom BEMVINDO10', true, estado.quantidadeCupons === 1 && Boolean(estado.cupom?.includes('BEMVINDO10')));
      for (const [campo, valor] of Object.entries(esperado)) s.comparar(`Interface ${etapa}`, campo, valor, valorDaTela(estado.valores[campo]));
      if (index === 2) s.comparar('Interface ao voltar para uma unidade', 'Aviso de frete', 'Faltam R$ 100,00 para o frete grátis.', estado.avisoFrete);
    }
  });
});
