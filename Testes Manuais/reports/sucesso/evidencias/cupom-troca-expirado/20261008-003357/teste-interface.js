const fs=require('fs');const path=require('path');const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'/tmp/verzel-browser/node_modules/playwright');
const root=process.argv[2];if(!root)throw new Error('Informe o diretório de evidências');
const now=()=>new Date().toLocaleString('sv-SE',{timeZone:'America/Fortaleza'})+' (America/Fortaleza)';const normalize=s=>s.replace(/\s+/g,' ').trim();
const result={data:now(),tls:'Verificação TLS ativa',etapas:[],verificacoes:[]};
(async()=>{
 const proxyUrl=process.env.HTTPS_PROXY||process.env.https_proxy;const proxy=proxyUrl?{server:new URL(proxyUrl).origin}:undefined;
 const browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,proxy});const context=await browser.newContext({viewport:{width:1280,height:1000},locale:'pt-BR'});const page=await context.newPage();
 function check(phase,name,expected,actual,ok){result.verificacoes.push({etapa:phase,verificacao:name,esperado:expected,encontrado:actual,resultado:ok?'Aprovado':'Falhou'})}
 async function capture(phase,response,expectedCoupon,expectedDiscount,expectedTotal){
  const dir=path.join(root,'interface',phase);fs.mkdirSync(dir,{recursive:true});
  const raw=await response.text();const data=JSON.parse(raw);
  fs.writeFileSync(path.join(dir,'corpo-enviado.json'),response.request().postData());fs.writeFileSync(path.join(dir,'corpo-recebido.json'),raw);fs.writeFileSync(path.join(dir,'resposta-http.json'),JSON.stringify({url:response.url(),status:response.status(),headers:await response.allHeaders(),corpo:data},null,2)+'\n');
  await page.waitForLoadState('networkidle');
  const counts={cupom:await page.locator('.cupom-aplicado').count(),campo:await page.getByLabel('Cupom de desconto',{exact:true}).count(),remover:await page.getByRole('button',{name:'Remover cupom',exact:true}).count()};
  const totals={};for(const key of ['subtotal','desconto','frete','total'])totals[key]=normalize(await page.locator('[data-valor="'+key+'"]').innerText());
  const label=counts.cupom?normalize(await page.locator('.cupom-aplicado p').innerText()):null;
  const message=await page.locator('#mensagem-cupom').count()?await page.locator('#mensagem-cupom').innerText():null;
  const state={data:now(),cupomExibido:label,mensagem:message,controles:counts,valores:totals};
  fs.writeFileSync(path.join(dir,'estado.json'),JSON.stringify(state,null,2)+'\n');fs.writeFileSync(path.join(dir,'texto-tela.txt'),await page.locator('body').innerText());await page.screenshot({path:path.join(dir,'tela.png'),fullPage:true});
  check(phase,'Status da API',200,response.status(),response.status()===200);
  check(phase,'Quantidade de cupons na tela',expectedCoupon?1:0,counts.cupom,counts.cupom===(expectedCoupon?1:0));
  if(expectedCoupon){check(phase,'Cupom ativo','BEMVINDO10',data.cupom?.codigo,data.cupom?.codigo==='BEMVINDO10'&&data.cupom?.aplicado===true&&label==='Cupom BEMVINDO10 aplicado.');}
  else{check(phase,'Nenhum cupom aplicado na API','Nenhum aplicado',data.cupom,data.cupom?.aplicado!==true);check(phase,'Formulário disponível novamente',true,counts.campo===1&&counts.remover===0,counts.campo===1&&counts.remover===0);}
  for(const [key,expected] of [['subtotal','R$ 100,00'],['desconto',expectedDiscount],['frete','R$ 19,90'],['total',expectedTotal]])check(phase,key,expected,totals[key],totals[key]===expected);
  if(phase==='03-cupom-expirado'){
   check(phase,'Mensagem visível','Cupom expirado.',message,message==='Cupom expirado.'&&await page.locator('#mensagem-cupom').isVisible());
   check(phase,'Cupom expirado rejeitado',false,data.cupom?.aplicado,data.cupom?.aplicado===false);
   check(phase,'Mensagem retornada pela API','Cupom expirado.',data.cupom?.mensagem,data.cupom?.mensagem==='Cupom expirado.');
  }
  const numericDiscount=expectedCoupon?10:0,numericTotal=expectedCoupon?109.9:119.9;
  check(phase,'Valores da API', {desconto:numericDiscount,frete:19.9,total:numericTotal},{desconto:data.desconto,frete:data.frete,total:data.total},data.desconto===numericDiscount&&data.frete===19.9&&data.total===numericTotal);
 }
 const waitCalculation=applied=>page.waitForResponse(r=>r.url().endsWith('/api/carrinho/calcular')&&r.request().method()==='POST'&&(applied?r.request().postDataJSON()?.cupom==='BEMVINDO10':!r.request().postDataJSON()?.cupom));
 async function apply(phase){await page.getByLabel('Cupom de desconto',{exact:true}).fill('BEMVINDO10');const waiting=waitCalculation(true);await page.getByRole('button',{name:'Aplicar cupom',exact:true}).click();const response=await waiting;await page.getByRole('button',{name:'Remover cupom',exact:true}).waitFor({state:'visible'});result.etapas.push(phase);await capture(phase,response,true,'- R$ 10,00','R$ 109,90');}
 try{
  await page.goto('https://verzel-store.qa-test-verzel-store.workers.dev/',{waitUntil:'networkidle'});
  await page.locator('article').filter({has:page.getByRole('heading',{name:'Mochila Urbana 20L',exact:true})}).getByRole('button',{name:'Adicionar ao carrinho',exact:true}).click();await page.getByRole('link',{name:/Carrinho/}).click();await page.waitForLoadState('networkidle');result.etapas.push('Preparar 1 unidade de P005 em um novo contexto de navegador');
  await apply('01-cupom-aplicado');
  const waiting=waitCalculation(false);await page.getByRole('button',{name:'Remover cupom',exact:true}).click();const removedResponse=await waiting;await page.getByLabel('Cupom de desconto',{exact:true}).waitFor({state:'visible'});result.etapas.push('02-cupom-removido');await capture('02-cupom-removido',removedResponse,false,'R$ 0,00','R$ 119,90');
  await page.getByLabel('Cupom de desconto',{exact:true}).fill('VERAO2026');
  const expiredWaiting=page.waitForResponse(r=>r.url().endsWith('/api/carrinho/calcular')&&r.request().method()==='POST'&&r.request().postDataJSON()?.cupom==='VERAO2026');
  await page.getByRole('button',{name:'Aplicar cupom',exact:true}).click();const expiredResponse=await expiredWaiting;
  await page.waitForFunction(()=>document.querySelector('#mensagem-cupom')||document.querySelector('.cupom-aplicado'));
  result.etapas.push('03-cupom-expirado');await capture('03-cupom-expirado',expiredResponse,false,'R$ 0,00','R$ 119,90');
  result.resultado=result.verificacoes.every(c=>c.resultado==='Aprovado')?'Aprovado':'Falhou';
 }catch(e){result.resultado='Bloqueado';result.erro=e.message;fs.writeFileSync(path.join(root,'erro-interface.txt'),e.stack);await page.screenshot({path:path.join(root,'tela-no-erro.png'),fullPage:true}).catch(()=>{});}
 finally{fs.writeFileSync(path.join(root,'validacao-interface.json'),JSON.stringify(result,null,2)+'\n');await browser.close()}
 console.log(JSON.stringify(result,null,2));
})().catch(e=>{console.error(e.message);process.exitCode=1});
