const fs=require('fs');const path=require('path');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'/tmp/verzel-browser/node_modules/playwright');
const root=process.argv[2];if(!root)throw new Error('Informe o diretório de evidências');
const now=()=>new Date().toLocaleString('sv-SE',{timeZone:'America/Fortaleza'})+' (America/Fortaleza)';
const norm=s=>s.replace(/\s+/g,' ').trim();const money=n=>'R$ '+n.toFixed(2).replace('.',',');
const stages=[
 {slug:'01-cupom-quantidade-1',quantidade:1,esperado:{subtotal:100,desconto:10,frete:19.9,total:109.9}},
 {slug:'02-aumentar-para-2',quantidade:2,esperado:{subtotal:200,desconto:20,frete:0,total:180}},
 {slug:'03-diminuir-para-1',quantidade:1,esperado:{subtotal:100,desconto:10,frete:19.9,total:109.9},aviso:'Faltam R$ 100,00 para o frete grátis.'}
];
(async()=>{
 const proxyUrl=process.env.HTTPS_PROXY||process.env.https_proxy;
 const proxy=proxyUrl?{server:new URL(proxyUrl).origin}:undefined;
 const browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,proxy});
 const context=await browser.newContext({viewport:{width:1280,height:1000},locale:'pt-BR'});
 const page=await context.newPage();const result={inicio:now(),tls:'Verificação TLS ativa',sessao:'Mesma sessão de navegador nas três etapas',etapas:[]};
 let stageDir=root;
 try{
  await page.goto('https://verzel-store.qa-test-verzel-store.workers.dev/',{waitUntil:'networkidle'});
  const card=page.locator('article').filter({has:page.getByRole('heading',{name:'Mochila Urbana 20L',exact:true})});
  await card.getByRole('button',{name:'Adicionar ao carrinho',exact:true}).click();await page.waitForLoadState('networkidle');
  await page.getByRole('link',{name:/Carrinho/}).click();await page.waitForLoadState('networkidle');
  for(const [index,stage] of stages.entries()){
   stageDir=path.join(root,'interface',stage.slug);fs.mkdirSync(stageDir,{recursive:true});
   const r={etapa:stage.slug,inicio:now(),quantidadeEsperada:stage.quantidade,verificacoes:[]};
   const check=(label,want,found,ok)=>r.verificacoes.push({verificacao:label,esperado:want,encontrado:found,resultado:ok?'Aprovado':'Falhou'});
   const responsePromise=page.waitForResponse(resp=>{
    if(!resp.url().endsWith('/api/carrinho/calcular')||resp.request().method()!=='POST')return false;
    const b=resp.request().postDataJSON();return b?.cupom==='BEMVINDO10'&&b.itens?.length===1&&b.itens[0].produtoId==='P005'&&b.itens[0].quantidade===stage.quantidade;
   });
   if(index===0){await page.getByLabel('Cupom de desconto',{exact:true}).fill('BEMVINDO10');await page.getByRole('button',{name:'Aplicar cupom',exact:true}).click();}
   else if(index===1)await page.getByRole('button',{name:'Aumentar quantidade de Mochila Urbana 20L',exact:true}).click();
   else await page.getByRole('button',{name:'Diminuir quantidade de Mochila Urbana 20L',exact:true}).click();
   const response=await responsePromise;const raw=await response.text();const data=JSON.parse(raw);
   await page.waitForLoadState('networkidle');await page.getByRole('button',{name:'Remover cupom',exact:true}).waitFor({state:'visible'});
   const values={};for(const k of ['subtotal','desconto','frete','total'])values[k]=norm(await page.locator('[data-valor="'+k+'"]').innerText());
   const quantity=norm(await page.locator('output[aria-label="Quantidade de Mochila Urbana 20L"]').innerText());
   const coupons=page.locator('.cupom-aplicado');const couponCount=await coupons.count();const couponText=couponCount?norm(await coupons.innerText()):null;
   const notice=page.locator('.aviso-frete');const noticeText=await notice.count()?norm(await notice.innerText()):null;
   const state={data:now(),url:page.url(),quantidade:quantity,valores:values,cupom:couponText,quantidadeCupons:couponCount,avisoFrete:noticeText};
   fs.writeFileSync(path.join(stageDir,'corpo-enviado.json'),response.request().postData());
   fs.writeFileSync(path.join(stageDir,'corpo-recebido.json'),raw);
   fs.writeFileSync(path.join(stageDir,'resposta-http.json'),JSON.stringify({data:now(),status:response.status(),url:response.url(),headers:await response.allHeaders(),corpo:data},null,2)+'\n');
   fs.writeFileSync(path.join(stageDir,'estado.json'),JSON.stringify(state,null,2)+'\n');
   fs.writeFileSync(path.join(stageDir,'texto-tela.txt'),await page.locator('body').innerText());
   await page.screenshot({path:path.join(stageDir,'tela.png'),fullPage:true});
   check('Quantidade exibida',String(stage.quantidade),quantity,quantity===String(stage.quantidade));
   check('BEMVINDO10 permanece aplicado','Um cupom BEMVINDO10 aplicado',{quantidade:couponCount,texto:couponText,cupomRecebido:data.cupom},couponCount===1&&couponText.includes('BEMVINDO10')&&data.cupom?.codigo==='BEMVINDO10'&&data.cupom?.aplicado===true);
   check('Status do cálculo',200,response.status(),response.status()===200);
   for(const [k,v] of Object.entries(stage.esperado)){
    const want=(k==='desconto'?'- ':'')+money(v);
    check('Tela: '+k,want,values[k],values[k]===want||(k==='frete'&&v===0&&values[k]==='Grátis'));
    check('Cálculo recebido: '+k,v,data[k],data[k]===v);
   }
   if(stage.aviso)check('Aviso visível de quanto falta',stage.aviso,noticeText,noticeText===stage.aviso&&await notice.isVisible());
   r.fim=now();r.resultado=r.verificacoes.every(x=>x.resultado==='Aprovado')?'Aprovado':'Falhou';
   fs.writeFileSync(path.join(stageDir,'validacao-interface.json'),JSON.stringify(r,null,2)+'\n');result.etapas.push(r);
  }
  result.resultado=result.etapas.every(x=>x.resultado==='Aprovado')?'Aprovado':'Falhou';
 }catch(e){result.resultado=result.etapas.some(x=>x.resultado==='Falhou')?'Falhou':'Bloqueado';result.bloqueio=e.message;fs.writeFileSync(path.join(stageDir,'erro-interface.txt'),e.stack);await page.screenshot({path:path.join(stageDir,'tela-no-erro.png'),fullPage:true}).catch(()=>{});}
 finally{result.fim=now();fs.writeFileSync(path.join(root,'resumo-interface.json'),JSON.stringify(result,null,2)+'\n');await browser.close();}
 console.log(JSON.stringify({inicio:result.inicio,fim:result.fim,resultado:result.resultado,bloqueio:result.bloqueio,etapas:result.etapas.map(x=>({etapa:x.etapa,resultado:x.resultado,falhas:x.verificacoes.filter(y=>y.resultado==='Falhou')}))},null,2));
 if(result.resultado!=='Aprovado')process.exitCode=1;
})().catch(e=>{console.error(e.message);process.exitCode=1});
