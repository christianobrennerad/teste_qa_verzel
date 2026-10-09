import type { Page } from '@playwright/test';
import { expect } from './fixtures';
import type { Sessao } from './conferencia';

export type Item = { produtoId: string; quantidade: number };
export const nomes: Record<string, string> = {
  P001: 'Camiseta Essencial', P002: 'Calça Jeans Slim', P003: 'Tênis Casual Urbano',
  P004: 'Boné Aba Curva', P005: 'Mochila Urbana 20L', P007: 'Jaqueta Corta-Vento', P008: 'Garrafa Térmica 750ml',
};
export const dinheiro = (valor: number) => 'R$ ' + valor.toFixed(2).replace('.', ',');
// O sinal antes de R$ indica que o desconto é subtraído do total.
// O valor do desconto no contrato é a magnitude positiva dessa dedução.
export const valorDaTela = (texto: string) => texto === 'Grátis' ? 0
  : Number(texto.replace(/^\s*-\s*(?=R\$)/, '').replace('R$', '').replaceAll('.', '').replace(',', '.').trim());

export async function prepararCarrinho(page: Page, itens: Item[]) {
  await page.goto('/', { waitUntil: 'networkidle' });
  for (const item of itens) {
    const card = page.locator('article').filter({ has: page.getByRole('heading', { name: nomes[item.produtoId], exact: true }) });
    for (let q = 0; q < item.quantidade; q++) {
      const recebido = page.waitForResponse(r => r.url().endsWith('/api/carrinho/calcular') && r.request().method() === 'POST');
      await card.getByRole('button', { name: 'Adicionar ao carrinho', exact: true }).click();
      await recebido;
    }
  }
  await page.getByRole('link', { name: /Carrinho/ }).click();
  await expect(page.locator('[data-valor="total"]')).toBeVisible();
  await page.waitForLoadState('networkidle');
}

export async function aplicarCupom(page: Page) {
  const recebido = page.waitForResponse(r => r.url().endsWith('/api/carrinho/calcular')
    && r.request().method() === 'POST' && r.request().postDataJSON()?.cupom === 'BEMVINDO10');
  await page.getByLabel('Cupom de desconto', { exact: true }).fill('BEMVINDO10');
  await page.getByRole('button', { name: 'Aplicar cupom', exact: true }).click();
  const resposta = await recebido;
  await expect(page.getByRole('button', { name: 'Remover cupom', exact: true })).toBeVisible();
  await page.waitForLoadState('networkidle');
  return resposta;
}

export function conferirResumo(sessao: Sessao, etapa: string, esperado: Record<string, unknown>, dados: Record<string, any>) {
  for (const [campo, valor] of Object.entries(esperado)) sessao.comparar(etapa, campo, valor, dados[campo]);
}
