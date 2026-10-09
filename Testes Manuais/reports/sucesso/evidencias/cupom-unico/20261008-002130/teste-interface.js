const fs=require('fs');const path=require('path');const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'/tmp/verzel-browser/node_modules/playwright');
const root=process.argv[2];if(!root)throw new Error('Informe o diretório de evidências');const dir=path.join(root,'interface');fs.mkdirSync(dir,{recursive:true});
const now=()=>new Date().toLocaleString('sv-SE',{timeZone:'America/Fortaleza'})+' (America/Fortaleza)';const normalize=s=>s.replace(/\s+/g,' ').trim();
const result={data:now(),tls:'Verificação TLS ativa',etapas:[],verificacoes:[]};
(async()=>{
 const proxyUrl=process.env.HTTPS_PROXY||process.env.https_proxy;const proxy=proxyUrl?{server:new URL(proxyUrl).origin}:undefined;
 const browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,proxy});const context=await browser.newContext({viewport:{width:1280,height:1000},locale:'pt-BR'});const page=await context.newPage();
 let requests=0;page.on('request',r=>{if(r.url().endsWith('/api/carrinho/calcular')&&r.method()==='POST')requests++});
 const check=(name,expected,actual,ok)=>result.verificacoes.push({verificacao:name,esperado:expected,encontrado:actual,resultado:ok?'Aprovado':'Falhou'});
 async function state(){
  const totals={};for(const key of ['subtotal','desconto','frete','total'])totals[key]=normalize(await page.locator('[data-valor="'+key+'"]').innerText());
  return {cupom:await page.locator('.cupom-aplicado p').count()?normalize(await page.locator('.cupom-aplicado p').innerText()):null,cupomAplicadoCount:await page.locator('.cupom-aplicado').count(),removerCount:await page.getByRole('button',{name:'Remover cupom',exact:true}).count(),campoCount:await page.getByLabel('Cupom de desconto',{exact:true}).count(),aplicarCount:await page.getByRole('button',{name:'Aplicar cupom',exact:true}).count(),requisicoesCalculo:requests,valores:totals};
 }
 try{
  await page.goto('https://verzel-store.qa-test-verzel-store.workers.dev/',{waitUntil:'networkidle'});result.etapas.push('Abrir loja em contexto novo');
  await page.locator('article').filter({has:page.getByRole('heading',{name:'Mochila Urbana 20L',exact:true})}).getByRole('button',{name:'Adicionar ao carrinho',exact:true}).click();
  await page.getByRole('link',{name:/Carrinho/}).click();await page.waitForLoadState('networkidle');result.etapas.push('Preparar 1 unidade de P005, sem cupom');
  await page.getByLabel('Cupom de desconto',{exact:true}).fill('BEMVINDO10');
  const responsePromise=page.waitForResponse(r=>r.url().endsWith('/api/carrinho/calcular')&&r.request().method()==='POST'&&r.request().postDataJSON()?.cupom==='BEMVINDO10');
  await page.getByRole('button',{name:'Aplicar cupom',exact:true}).click();const response=await responsePromise;
  fs.writeFileSync(path.join(dir,'corpo-enviado.json'),response.request().postData());fs.writeFileSync(path.join(dir,'corpo-recebido.json'),await response.text());fs.writeFileSync(path.join(dir,'resposta-http.json'),JSON.stringify({status:response.status(),url:response.url(),headers:await response.allHeaders()},null,2)+'\n');
  await page.getByRole('button',{name:'Remover cupom',exact:true}).waitFor({state:'visible'});await page.waitForLoadState('networkidle');result.etapas.push('Aplicar BEMVINDO10 pela primeira vez');
  const before=await state();fs.writeFileSync(path.join(dir,'estado-apos-primeira-aplicacao.json'),JSON.stringify(before,null,2)+'\n');await page.screenshot({path:path.join(dir,'cupom-aplicado.png'),fullPage:true});
  // Attempt only through the supported UI; never create missing controls or remove the current coupon.
  const input=page.getByLabel('Cupom de desconto',{exact:true}),button=page.getByRole('button',{name:'Aplicar cupom',exact:true});
  const canReapply=(await input.count())>0&&(await button.count())>0&&await input.isVisible()&&await input.isEnabled()&&await button.isVisible()&&await button.isEnabled();
  if(canReapply){await input.fill('BEMVINDO10');await button.click();await page.waitForLoadState('networkidle');result.tentativa='Segunda aplicação enviada pelo formulário';}
  else result.tentativa='Reaplicação impedida pelo fluxo da interface: não há campo nem botão Aplicar cupom após a primeira aplicação; cupom atual não foi removido';
  result.etapas.push(result.tentativa);
  const after=await state();fs.writeFileSync(path.join(dir,'estado-apos-tentativa.json'),JSON.stringify(after,null,2)+'\n');fs.writeFileSync(path.join(dir,'texto-depois.txt'),await page.locator('body').innerText());await page.screenshot({path:path.join(dir,'apos-tentativa.png'),fullPage:true});
  check('Estado inicial do cupom',1,before.cupomAplicadoCount,before.cupomAplicadoCount===1);
  check('Quantidade de cupons após tentativa',1,after.cupomAplicadoCount,after.cupomAplicadoCount===1);
  check('Cupom mantido','Cupom BEMVINDO10 aplicado.',after.cupom,after.cupom==='Cupom BEMVINDO10 aplicado.');
  check('Desconto inicial','- R$ 10,00',before.valores.desconto,before.valores.desconto==='- R$ 10,00');check('Total inicial','R$ 109,90',before.valores.total,before.valores.total==='R$ 109,90');
  check('Desconto após tentativa','- R$ 10,00',after.valores.desconto,after.valores.desconto==='- R$ 10,00');check('Total após tentativa','R$ 109,90',after.valores.total,after.valores.total==='R$ 109,90');
  check('Frete após tentativa','R$ 19,90',after.valores.frete,after.valores.frete==='R$ 19,90');
  if(!canReapply)check('Controles de reaplicação ausentes',{campo:0,botao:0},{campo:after.campoCount,botao:after.aplicarCount},after.campoCount===0&&after.aplicarCount===0);
  result.resultado=result.verificacoes.every(c=>c.resultado==='Aprovado')?'Aprovado':'Falhou';
 }catch(e){result.resultado='Bloqueado';result.erro=e.message;fs.writeFileSync(path.join(dir,'erro-interface.txt'),e.stack);await page.screenshot({path:path.join(dir,'tela-no-erro.png'),fullPage:true}).catch(()=>{});}
 finally{fs.writeFileSync(path.join(dir,'validacao-interface.json'),JSON.stringify(result,null,2)+'\n');await browser.close()}
 console.log(JSON.stringify(result,null,2));
})().catch(e=>{console.error(e.message);process.exitCode=1});
