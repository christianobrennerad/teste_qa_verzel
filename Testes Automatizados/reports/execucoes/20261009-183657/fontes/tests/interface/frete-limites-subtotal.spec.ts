import { test } from '../suporte/fixtures';
import { executarCaso } from '../suporte/conferencia';
import { conferirResumo, dinheiro, prepararCarrinho, valorDaTela } from '../suporte/carrinho';

const exemplos = [
  { caso: 'P003-1', itens: [{ produtoId: 'P003', quantidade: 1 }], resumo: { subtotal: 189.9, desconto: 0, frete: 19.9, freteGratis: false, valorFaltanteFreteGratis: 10.1, total: 209.8 } },
  { caso: 'P002-1-P001-1', itens: [{ produtoId: 'P002', quantidade: 1 }, { produtoId: 'P001', quantidade: 1 }], resumo: { subtotal: 199.8, desconto: 0, frete: 19.9, freteGratis: false, valorFaltanteFreteGratis: 0.2, total: 219.7 } },
  { caso: 'P005-2', itens: [{ produtoId: 'P005', quantidade: 2 }], resumo: { subtotal: 200, desconto: 0, frete: 0, freteGratis: true, valorFaltanteFreteGratis: 0, total: 200 } },
  { caso: 'P007-1', itens: [{ produtoId: 'P007', quantidade: 1 }], resumo: { subtotal: 229.9, desconto: 0, frete: 0, freteGratis: true, valorFaltanteFreteGratis: 0, total: 229.9 } },
];

for (const exemplo of exemplos) {
  test(`Frete nos limites: ${exemplo.caso}`, { tag: ['@api', '@interface', '@CA06', '@CA07', '@CA11'] }, async ({ page, request, browser }, info) => {
    await executarCaso(info, 'frete-limites-subtotal', exemplo.caso, async s => {
      s.observacoes.push(`Navegador: Chromium ${browser.version()}; certificados verificados.`);
      const independente = await s.api(request, 'api-independente', 'POST', '/api/carrinho/calcular', { itens: exemplo.itens });
      s.comparar('API independente', 'Status', 200, independente.status);
      conferirResumo(s, 'API independente', exemplo.resumo, independente.dados);
      for (const campo of ['subtotal', 'desconto', 'frete', 'valorFaltanteFreteGratis', 'total']) {
        const v = independente.dados[campo];
        s.comparar('API independente', `Até duas casas decimais: ${campo}`, true, typeof v === 'number' && Number.isFinite(v) && Math.abs(v * 100 - Math.round(v * 100)) < 1e-7);
      }
      let ultima: import('@playwright/test').Response | undefined;
      page.on('response', r => { if (r.url().endsWith('/api/carrinho/calcular') && r.request().method() === 'POST') ultima = r; });
      await prepararCarrinho(page, exemplo.itens);
      if (!ultima) throw new Error('A interface não enviou o cálculo do carrinho.');
      const usada = await s.capturarHTTP('api-interface', ultima, ultima.request().postDataJSON());
      s.comparar('API usada pela interface', 'Status', 200, usada.status);
      conferirResumo(s, 'API usada pela interface', exemplo.resumo, usada.dados);
      const estado = await s.tela(page, 'carrinho');
      s.comparar('Interface', 'Sem cupom aplicado', 0, estado.quantidadeCupons);
      for (const campo of ['subtotal', 'desconto', 'frete', 'total'] as const) {
        s.comparar('Interface', `${campo} exibido com duas casas`, dinheiro(exemplo.resumo[campo]), estado.valores[campo]);
        s.comparar('API e interface', `${campo} sem divergência`, usada.dados[campo], valorDaTela(estado.valores[campo]));
      }
      s.comparar('Interface', 'Frete grátis', exemplo.resumo.freteGratis, valorDaTela(estado.valores.frete) === 0);
      const aviso = exemplo.resumo.freteGratis ? null : `Faltam ${dinheiro(exemplo.resumo.valorFaltanteFreteGratis)} para o frete grátis.`;
      s.comparar('Interface', 'Informação de quanto falta para frete grátis', aviso, estado.avisoFrete);
    });
  });
}
