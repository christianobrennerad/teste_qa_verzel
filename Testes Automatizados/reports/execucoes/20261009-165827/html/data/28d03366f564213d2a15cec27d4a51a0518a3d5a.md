# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: api/erros-rota-metodo-produto.spec.ts >> Erros de rota: GET /api/produtos/INEXISTENTE
- Location: tests/api/erros-rota-metodo-produto.spec.ts:13:7

# Error details

```
Error: API: Formato documentado inclui campo relacionado

expect(received).toEqual(expected) // deep equality

Expected: true
Received: false
```

# Test source

```ts
  1   | import { mkdir, writeFile } from 'node:fs/promises';
  2   | import { dirname } from 'node:path';
  3   | import { isDeepStrictEqual } from 'node:util';
  4   | import type { APIRequestContext, APIResponse, Page, Response, TestInfo } from '@playwright/test';
  5   | import { expect } from './fixtures';
  6   | 
  7   | type Conferencia = {
  8   |   etapa: string;
  9   |   verificacao: string;
  10  |   esperado: unknown;
  11  |   encontrado: unknown;
  12  |   resultado: 'Aprovado' | 'Falhou';
  13  | };
  14  | 
  15  | export class Sessao {
  16  |   readonly inicio = new Date().toISOString();
  17  |   readonly verificacoes: Conferencia[] = [];
  18  |   readonly observacoes: string[] = [];
  19  |   concluido = false;
  20  |   erroExecucao?: string;
  21  | 
  22  |   constructor(readonly info: TestInfo, readonly relatorio: string, readonly caso: string) {}
  23  | 
  24  |   async arquivo(nome: string, conteudo: string | Buffer, tipo: string) {
  25  |     const path = this.info.outputPath('evidencias', nome);
  26  |     await mkdir(dirname(path), { recursive: true });
  27  |     await writeFile(path, conteudo);
  28  |     await this.info.attach(nome, { path, contentType: tipo });
  29  |   }
  30  | 
  31  |   async json(nome: string, conteudo: unknown) {
  32  |     await this.arquivo(nome, JSON.stringify(conteudo, null, 2) + '\n', 'application/json');
  33  |   }
  34  | 
  35  |   comparar(etapa: string, verificacao: string, esperado: unknown, encontrado: unknown) {
  36  |     const atual = encontrado === undefined ? '<ausente>' : encontrado;
  37  |     this.verificacoes.push({
  38  |       etapa, verificacao, esperado, encontrado: atual,
  39  |       resultado: isDeepStrictEqual(encontrado, esperado) ? 'Aprovado' : 'Falhou',
  40  |     });
> 41  |     expect.soft(encontrado, `${etapa}: ${verificacao}`).toEqual(esperado);
      |                                                         ^ Error: API: Formato documentado inclui campo relacionado
  42  |   }
  43  | 
  44  |   async capturarHTTP(prefixo: string, resposta: APIResponse | Response, corpoEnviado?: unknown, metodoEnviado?: string) {
  45  |     const request = 'request' in resposta ? resposta.request() : undefined;
  46  |     const metodo = request?.method() ?? metodoEnviado ?? 'POST';
  47  |     const body = await resposta.text();
  48  |     const headers = await resposta.headersArray();
  49  |     await this.json(`${prefixo}-requisicao.json`, {
  50  |       horario: new Date().toISOString(), metodo, url: resposta.url(),
  51  |       cabecalhos: { 'Content-Type': 'application/json' }, corpo: corpoEnviado,
  52  |     });
  53  |     await this.json(`${prefixo}-resposta-http.json`, {
  54  |       horario: new Date().toISOString(), url: resposta.url(), status: resposta.status(),
  55  |       statusText: resposta.statusText(), cabecalhos: headers, corpoRecebido: body,
  56  |     });
  57  |     await this.arquivo(`${prefixo}-corpo-recebido.json`, body, 'application/json');
  58  |     const quote = (v: string) => "'" + v.replaceAll("'", "'\\''") + "'";
  59  |     const data = corpoEnviado === undefined ? '' : ' --data-binary ' + quote(JSON.stringify(corpoEnviado));
  60  |     await this.arquivo(`${prefixo}-comando.txt`,
  61  |       `curl -i -X ${metodo} ${quote(resposta.url())} -H 'Content-Type: application/json'${data} --max-time 30 --silent --show-error\n`,
  62  |       'text/plain');
  63  |     return { status: resposta.status(), headers, dados: JSON.parse(body) as Record<string, any> };
  64  |   }
  65  | 
  66  |   async api(request: APIRequestContext, prefixo: string, metodo: string, endpoint: string, corpo?: unknown) {
  67  |     const inicio = new Date().toISOString();
  68  |     await this.json(`${prefixo}-inicio.json`, { inicio, metodo, endpoint, corpo });
  69  |     const resposta = await request.fetch(endpoint, { method: metodo, data: corpo });
  70  |     const recebido = await this.capturarHTTP(prefixo, resposta, corpo, metodo);
  71  |     return recebido;
  72  |   }
  73  | 
  74  |   async tela(page: Page, prefixo: string) {
  75  |     const normalizar = (s: string) => s.replaceAll('\u00a0', ' ').trim();
  76  |     const valores: Record<string, string> = {};
  77  |     for (const campo of ['subtotal', 'desconto', 'frete', 'total']) {
  78  |       valores[campo] = normalizar(await page.locator(`[data-valor="${campo}"]`).innerText());
  79  |     }
  80  |     const aviso = page.locator('.aviso-frete');
  81  |     const cupons = page.locator('.cupom-aplicado');
  82  |     const estado = {
  83  |       horario: new Date().toISOString(), url: page.url(), valores,
  84  |       avisoFrete: await aviso.count() ? normalizar(await aviso.innerText()) : null,
  85  |       quantidadeCupons: await cupons.count(),
  86  |       cupom: await cupons.count() ? normalizar(await cupons.innerText()) : null,
  87  |       textoTela: normalizar(await page.locator('body').innerText()),
  88  |     };
  89  |     await this.json(`${prefixo}-estado-interface.json`, estado);
  90  |     await this.arquivo(`${prefixo}-texto-tela.txt`, estado.textoTela, 'text/plain');
  91  |     await this.arquivo(`${prefixo}-tela.png`, await page.screenshot({ fullPage: true }), 'image/png');
  92  |     return estado;
  93  |   }
  94  | 
  95  |   async finalizar() {
  96  |     await this.json('validacao.json', {
  97  |       relatorio: this.relatorio, caso: this.caso, tituloTeste: this.info.title,
  98  |       arquivoTeste: this.info.file, projeto: this.info.project.name,
  99  |       inicio: this.inicio, fim: new Date().toISOString(), timezone: 'America/Fortaleza',
  100 |       concluido: this.concluido, erroExecucao: this.erroExecucao,
  101 |       resultado: !this.concluido ? 'Bloqueado'
  102 |         : this.verificacoes.some(v => v.resultado === 'Falhou') ? 'Falhou' : 'Aprovado',
  103 |       observacoes: this.observacoes, verificacoes: this.verificacoes,
  104 |     });
  105 |   }
  106 | }
  107 | 
  108 | export async function executarCaso(info: TestInfo, relatorio: string, caso: string, executar: (sessao: Sessao) => Promise<void>) {
  109 |   const sessao = new Sessao(info, relatorio, caso);
  110 |   try {
  111 |     await executar(sessao);
  112 |     sessao.concluido = true;
  113 |   } catch (erro) {
  114 |     sessao.erroExecucao = erro instanceof Error ? erro.message : String(erro);
  115 |     throw erro;
  116 |   } finally {
  117 |     await sessao.finalizar();
  118 |   }
  119 | }
  120 | 
```