import { mkdir, writeFile } from 'node:fs/promises';
import { dirname } from 'node:path';
import { isDeepStrictEqual } from 'node:util';
import type { APIRequestContext, APIResponse, Page, Response, TestInfo } from '@playwright/test';
import { expect } from './fixtures';

type Conferencia = {
  etapa: string;
  verificacao: string;
  esperado: unknown;
  encontrado: unknown;
  resultado: 'Aprovado' | 'Falhou';
};

export class Sessao {
  readonly inicio = new Date().toISOString();
  readonly verificacoes: Conferencia[] = [];
  readonly observacoes: string[] = [];
  concluido = false;
  erroExecucao?: string;

  constructor(readonly info: TestInfo, readonly relatorio: string, readonly caso: string) {}

  async arquivo(nome: string, conteudo: string | Buffer, tipo: string) {
    const path = this.info.outputPath('evidencias', nome);
    await mkdir(dirname(path), { recursive: true });
    await writeFile(path, conteudo);
    await this.info.attach(nome, { path, contentType: tipo });
  }

  async json(nome: string, conteudo: unknown) {
    await this.arquivo(nome, JSON.stringify(conteudo, null, 2) + '\n', 'application/json');
  }

  comparar(etapa: string, verificacao: string, esperado: unknown, encontrado: unknown) {
    const atual = encontrado === undefined ? '<ausente>' : encontrado;
    this.verificacoes.push({
      etapa, verificacao, esperado, encontrado: atual,
      resultado: isDeepStrictEqual(encontrado, esperado) ? 'Aprovado' : 'Falhou',
    });
    expect.soft(encontrado, `${etapa}: ${verificacao}`).toEqual(esperado);
  }

  async capturarHTTP(prefixo: string, resposta: APIResponse | Response, corpoEnviado?: unknown, metodoEnviado?: string) {
    const request = 'request' in resposta ? resposta.request() : undefined;
    const metodo = request?.method() ?? metodoEnviado ?? 'POST';
    const body = await resposta.text();
    const headers = await resposta.headersArray();
    await this.json(`${prefixo}-requisicao.json`, {
      horario: new Date().toISOString(), metodo, url: resposta.url(),
      cabecalhos: { 'Content-Type': 'application/json' }, corpo: corpoEnviado,
    });
    await this.json(`${prefixo}-resposta-http.json`, {
      horario: new Date().toISOString(), url: resposta.url(), status: resposta.status(),
      statusText: resposta.statusText(), cabecalhos: headers, corpoRecebido: body,
    });
    await this.arquivo(`${prefixo}-corpo-recebido.json`, body, 'application/json');
    const quote = (v: string) => "'" + v.replaceAll("'", "'\\''") + "'";
    const data = corpoEnviado === undefined ? '' : ' --data-binary ' + quote(JSON.stringify(corpoEnviado));
    await this.arquivo(`${prefixo}-comando.txt`,
      `curl -i -X ${metodo} ${quote(resposta.url())} -H 'Content-Type: application/json'${data} --max-time 30 --silent --show-error\n`,
      'text/plain');
    return { status: resposta.status(), headers, dados: JSON.parse(body) as Record<string, any> };
  }

  async api(request: APIRequestContext, prefixo: string, metodo: string, endpoint: string, corpo?: unknown) {
    const inicio = new Date().toISOString();
    await this.json(`${prefixo}-inicio.json`, { inicio, metodo, endpoint, corpo });
    const resposta = await request.fetch(endpoint, { method: metodo, data: corpo });
    const recebido = await this.capturarHTTP(prefixo, resposta, corpo, metodo);
    return recebido;
  }

  async tela(page: Page, prefixo: string) {
    const normalizar = (s: string) => s.replaceAll('\u00a0', ' ').trim();
    const valores: Record<string, string> = {};
    for (const campo of ['subtotal', 'desconto', 'frete', 'total']) {
      valores[campo] = normalizar(await page.locator(`[data-valor="${campo}"]`).innerText());
    }
    const aviso = page.locator('.aviso-frete');
    const cupons = page.locator('.cupom-aplicado');
    const estado = {
      horario: new Date().toISOString(), url: page.url(), valores,
      avisoFrete: await aviso.count() ? normalizar(await aviso.innerText()) : null,
      quantidadeCupons: await cupons.count(),
      cupom: await cupons.count() ? normalizar(await cupons.innerText()) : null,
      textoTela: normalizar(await page.locator('body').innerText()),
    };
    await this.json(`${prefixo}-estado-interface.json`, estado);
    await this.arquivo(`${prefixo}-texto-tela.txt`, estado.textoTela, 'text/plain');
    await this.arquivo(`${prefixo}-tela.png`, await page.screenshot({ fullPage: true }), 'image/png');
    return estado;
  }

  async finalizar() {
    await this.json('validacao.json', {
      relatorio: this.relatorio, caso: this.caso, tituloTeste: this.info.title,
      arquivoTeste: this.info.file, projeto: this.info.project.name,
      inicio: this.inicio, fim: new Date().toISOString(), timezone: 'America/Fortaleza',
      concluido: this.concluido, erroExecucao: this.erroExecucao,
      resultado: !this.concluido ? 'Bloqueado'
        : this.verificacoes.some(v => v.resultado === 'Falhou') ? 'Falhou' : 'Aprovado',
      observacoes: this.observacoes, verificacoes: this.verificacoes,
    });
  }
}

export async function executarCaso(info: TestInfo, relatorio: string, caso: string, executar: (sessao: Sessao) => Promise<void>) {
  const sessao = new Sessao(info, relatorio, caso);
  try {
    await executar(sessao);
    sessao.concluido = true;
  } catch (erro) {
    sessao.erroExecucao = erro instanceof Error ? erro.message : String(erro);
    throw erro;
  } finally {
    await sessao.finalizar();
  }
}
