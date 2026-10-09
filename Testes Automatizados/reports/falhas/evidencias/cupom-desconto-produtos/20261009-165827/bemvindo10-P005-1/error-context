# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: interface/cupom-desconto-produtos.spec.ts >> Aplicar desconto apenas aos produtos e exibir a mensagem do BDD
- Location: tests/interface/cupom-desconto-produtos.spec.ts:5:5

# Error details

```
Error: Interface: Mensagem exigida pelo BDD exibida na tela

expect(received).toEqual(expected) // deep equality

Expected: true
Received: false
```

# Page snapshot

```yaml
- generic [ref=e2]:
  - note [ref=e3]:
    - paragraph [ref=e4]:
      - text: Ambiente de teste técnico do processo seletivo de QA da Verzel.
      - link "Leia a documentação antes de começar." [ref=e5] [cursor=pointer]:
        - /url: /documentacao
  - banner [ref=e6]:
    - generic [ref=e7]:
      - link "Verzel Store, página inicial" [ref=e8] [cursor=pointer]:
        - /url: /
        - generic [ref=e9]:
          - generic [ref=e15]: verzel
          - generic [ref=e16]: store
      - navigation "Principal" [ref=e17]:
        - link "Produtos" [ref=e18] [cursor=pointer]:
          - /url: /
        - link "Documentação" [ref=e19] [cursor=pointer]:
          - /url: /documentacao
        - link "Carrinho 1 itens no carrinho" [ref=e20] [cursor=pointer]:
          - /url: /carrinho
          - text: Carrinho
          - generic "1 itens no carrinho" [ref=e21]: "1"
  - main [ref=e22]:
    - generic [ref=e23]:
      - generic [ref=e24]:
        - heading "Carrinho" [level=1] [ref=e25]
        - button "Esvaziar carrinho" [ref=e26] [cursor=pointer]
      - generic [ref=e27]:
        - generic [ref=e28]:
          - list [ref=e29]:
            - listitem [ref=e30]:
              - generic [ref=e38]:
                - heading "Mochila Urbana 20L" [level=3] [ref=e39]
                - paragraph [ref=e40]: R$ 100,00 cada
              - group "Quantidade de Mochila Urbana 20L" [ref=e41]:
                - button "Diminuir quantidade de Mochila Urbana 20L" [disabled] [ref=e42]: "-"
                - status "Quantidade de Mochila Urbana 20L" [ref=e43]: "1"
                - button "Aumentar quantidade de Mochila Urbana 20L" [ref=e44] [cursor=pointer]: +
              - paragraph [ref=e45]: R$ 100,00
              - button "Remover Mochila Urbana 20L do carrinho" [ref=e46] [cursor=pointer]: Remover
          - generic [ref=e47]:
            - paragraph [ref=e48]:
              - text: Cupom
              - strong [ref=e49]: BEMVINDO10
              - text: aplicado.
            - button "Remover cupom" [ref=e50] [cursor=pointer]
        - region [ref=e52]:
          - heading "Resumo do pedido" [level=2] [ref=e53]
          - generic [ref=e54]:
            - generic [ref=e55]:
              - term [ref=e56]: Subtotal
              - definition [ref=e57]: R$ 100,00
            - generic [ref=e58]:
              - term [ref=e59]: Desconto (BEMVINDO10)
              - definition [ref=e60]: "- R$ 10,00"
            - generic [ref=e61]:
              - term [ref=e62]: Frete
              - definition [ref=e63]: R$ 19,90
            - generic [ref=e64]:
              - term [ref=e65]: Total
              - definition [ref=e66]: R$ 109,90
          - paragraph [ref=e67]: Faltam R$ 100,00 para o frete grátis.
          - link "Finalizar compra" [ref=e68] [cursor=pointer]:
            - /url: /checkout
  - contentinfo [ref=e69]:
    - paragraph [ref=e71]: Verzel Store é um ambiente fictício criado para o teste técnico do processo seletivo de QA da Verzel. Nenhuma compra é real.
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
      |                                                         ^ Error: Interface: Mensagem exigida pelo BDD exibida na tela
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