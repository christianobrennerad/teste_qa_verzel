const fs=require('fs');const path=require('path');const os=require('os');
const {chromium}=require('/tmp/verzel-browser/node_modules/playwright');
const root=process.argv[2];if(!root)throw new Error('Informe o diretório de evidências');
const now=()=>new Date().toLocaleString('sv-SE',{timeZone:'America/Fortaleza'})+' (America/Fortaleza)';
const norm=s=>s.replace(/\s+/g,' ').trim();
const cases=[{slug:'01-outra-aba',nome:'outra aba'},{slug:'02-outro-navegador',nome:'outro navegador'},{slug:'03-janela-anonima',nome:'janela anônima'}];
async function snapshot(page,dir){
 fs.mkdirSync(dir,{recursive:true});
 const body=await page.locator('body').innerText();
 const storage=await page.evaluate(()=>({itens:JSON.parse(sessionStorage.getItem('verzel-store:itens')||'[]'),cupom:JSON.parse(sessionStorage.getItem('verzel-store:cupom')||'null'),temOpener:window.opener!==null}));
 const state={data:now(),url:page.url(),titulo:await page.title(),texto:body,itens:storage.itens,cupom:storage.cupom,temOpener:storage.temOpener,quantidadeP005:await page.locator('output[aria-label="Quantidade de Mochila Urbana 20L"]').count()?norm(await page.locator('output[aria-label="Quantidade de Mochila Urbana 20L"]').innerText()):null,carrinhoVazioVisivel:await page.getByRole('heading',{name:'Seu carrinho está vazio',exact:true}).isVisible()};
 fs.writeFileSync(path.join(dir,'estado.json'),JSON.stringify(state,null,2)+'\n');
 fs.writeFileSync(path.join(dir,'texto-tela.txt'),body);await page.screenshot({path:path.join(dir,'tela.png'),fullPage:true});return state;
}
(async()=>{
 const proxyUrl=process.env.HTTPS_PROXY||process.env.https_proxy;const proxy=proxyUrl?{server:new URL(proxyUrl).origin}:undefined;
 const result={inicio:now(),tls:'Verificação TLS ativa',casos:[]};
 for(const c of cases){
  const dir=path.join(root,c.slug);fs.mkdirSync(dir,{recursive:true});
  const profile=fs.mkdtempSync(path.join(os.tmpdir(),'verzel-isolamento-chromium-'));
  const context=await chromium.launchPersistentContext(profile,{executablePath:'/usr/bin/chromium',headless:true,proxy,viewport:{width:1280,height:1000},locale:'pt-BR'});
  const page=context.pages()[0];let extraContext;const r={contexto:c.nome,inicio:now(),navegador:'Chromium '+context.browser().version(),verificacoes:[]};
  const check=(name,want,found,ok)=>r.verificacoes.push({verificacao:name,esperado:want,encontrado:found,resultado:ok?'Aprovado':'Falhou'});
  try{
   await page.goto('https://verzel-store.qa-test-verzel-store.workers.dev/',{waitUntil:'networkidle'});
   const responsePromise=page.waitForResponse(resp=>{if(!resp.url().endsWith('/api/carrinho/calcular')||resp.request().method()!=='POST')return false;const b=resp.request().postDataJSON();return b.itens?.length===1&&b.itens[0].produtoId==='P005'&&b.itens[0].quantidade===1;});
   const card=page.locator('article').filter({has:page.getByRole('heading',{name:'Mochila Urbana 20L',exact:true})});
   await card.getByRole('button',{name:'Adicionar ao carrinho',exact:true}).click();const resp=await responsePromise;const raw=await resp.text();
   fs.writeFileSync(path.join(dir,'corpo-enviado.json'),resp.request().postData());
   fs.writeFileSync(path.join(dir,'corpo-recebido.json'),raw);
   fs.writeFileSync(path.join(dir,'resposta-http.json'),JSON.stringify({data:now(),status:resp.status(),url:resp.url(),headers:await resp.allHeaders(),corpo:JSON.parse(raw)},null,2)+'\n');
   await page.getByRole('link',{name:/Carrinho/}).click();await page.waitForLoadState('networkidle');
   const before=await snapshot(page,path.join(dir,'original-antes'));
   check('Original preparada com P005','Uma unidade de P005',before.itens,before.quantidadeP005==='1'&&before.itens.length===1&&before.itens[0].produtoId==='P005'&&before.itens[0].quantidade===1);
   check('Status do cálculo da preparação',200,resp.status(),resp.status()===200);
   if(c.nome==='outro navegador'){
    r.bloqueio='Firefox não instalado: os downloads oficiais do Playwright e a fonte alternativa da Mozilla foram recusados pelo ambiente com HTTP 403.';
    r.verificacoes.push({verificacao:'Novo carrinho em outro navegador',esperado:'Carrinho vazio no Firefox',encontrado:'Navegador indisponível',resultado:'Bloqueado'});
   }else{
    let newPage;
    if(c.nome==='outra aba'){newPage=await context.newPage();r.metodo='Nova aba no mesmo perfil do Chromium, sem opener e sem duplicar a aba original';}
    else{extraContext=await context.browser().newContext({viewport:{width:1280,height:1000},locale:'pt-BR'});newPage=await extraContext.newPage();r.metodo='Contexto anônimo do Chromium, separado do perfil normal da aba original';}
    await newPage.goto('https://verzel-store.qa-test-verzel-store.workers.dev/',{waitUntil:'networkidle'});
    await newPage.getByRole('link',{name:/Carrinho/}).click();await newPage.waitForLoadState('networkidle');
    const fresh=await snapshot(newPage,path.join(dir,'novo-contexto'));
    check('Novo contexto com carrinho vazio','Aviso de carrinho vazio visível, sem produtos',{avisoVisivel:fresh.carrinhoVazioVisivel,itens:fresh.itens,quantidadeP005:fresh.quantidadeP005},fresh.carrinhoVazioVisivel&&fresh.itens.length===0&&fresh.quantidadeP005===null);
   }
   await page.bringToFront();const after=await snapshot(page,path.join(dir,'original-depois'));
   check('Aba original mantém P005','Uma unidade de P005',after.itens,after.quantidadeP005==='1'&&after.itens.length===1&&after.itens[0].produtoId==='P005'&&after.itens[0].quantidade===1);
   r.resultado=r.verificacoes.some(x=>x.resultado==='Falhou')?'Falhou':r.bloqueio?'Bloqueado':'Aprovado';
  }catch(e){r.resultado='Bloqueado';r.erro=e.message;fs.writeFileSync(path.join(dir,'erro-interface.txt'),e.stack);await page.screenshot({path:path.join(dir,'tela-no-erro.png'),fullPage:true}).catch(()=>{});}
  finally{r.fim=now();fs.writeFileSync(path.join(dir,'validacao-interface.json'),JSON.stringify(r,null,2)+'\n');if(extraContext)await extraContext.close();await context.close();result.casos.push(r);}
 }
 result.fim=now();result.resultado=result.casos.some(x=>x.resultado==='Falhou')?'Falhou':result.casos.some(x=>x.resultado==='Bloqueado')?'Bloqueado':'Aprovado';
 fs.writeFileSync(path.join(root,'resumo-interface.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result,null,2));if(result.resultado!=='Aprovado')process.exitCode=1;
})().catch(e=>{console.error(e.stack);process.exitCode=1});
