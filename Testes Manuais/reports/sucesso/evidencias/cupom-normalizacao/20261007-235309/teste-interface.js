const fs=require('fs');const path=require('path');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'/tmp/verzel-browser/node_modules/playwright');
const root=process.argv[2];if(!root)throw new Error('Informe o diretório da execução');
const now=()=>new Date().toLocaleString('sv-SE',{timeZone:'America/Fortaleza'})+' (America/Fortaleza)';
const normalize=s=>s.replace(/\s+/g,' ').trim();
(async()=>{
 const proxyUrl=process.env.HTTPS_PROXY||process.env.https_proxy;
 const proxy=proxyUrl?{server:new URL(proxyUrl).origin}:undefined;
 const browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,proxy});
 const results=[];
 try{
  for(const [slug,coupon] of [['minusculas','bemvindo10'],['maiusculas-e-minusculas','BeMvInDo10']]){
   const dir=path.join(root,slug,'interface');fs.mkdirSync(dir,{recursive:true});
   const result={data:now(),cupom_digitado:coupon,tls:'Verificação TLS ativa',etapas:[],verificacoes:[]};
   const context=await browser.newContext({viewport:{width:1280,height:1000},locale:'pt-BR'});
   const page=await context.newPage();
   try{
    await page.goto('https://verzel-store.qa-test-verzel-store.workers.dev/',{waitUntil:'networkidle'});
    result.etapas.push('Abrir loja em contexto novo, sem compartilhar carrinho com outro exemplo');
    const card=page.locator('article').filter({has:page.getByRole('heading',{name:'Mochila Urbana 20L',exact:true})});
    await card.getByRole('button',{name:'Adicionar ao carrinho',exact:true}).click();
    await page.getByRole('link',{name:/Carrinho/}).click();await page.waitForLoadState('networkidle');
    result.etapas.push('Adicionar 1 unidade de P005 e abrir carrinho');
    await page.getByLabel('Cupom de desconto',{exact:true}).fill(coupon);
    fs.writeFileSync(path.join(dir,'cupom-digitado.txt'),await page.getByLabel('Cupom de desconto',{exact:true}).inputValue());
    await page.screenshot({path:path.join(dir,'antes-de-aplicar.png'),fullPage:true});
    fs.writeFileSync(path.join(dir,'texto-antes.txt'),await page.locator('body').innerText());
    const responsePromise=page.waitForResponse(r=>r.url().endsWith('/api/carrinho/calcular')&&r.request().method()==='POST'&&typeof r.request().postDataJSON()?.cupom==='string');
    await page.getByRole('button',{name:'Aplicar cupom',exact:true}).click();
    const response=await responsePromise;
    const text=await response.text();const data=JSON.parse(text);
    fs.writeFileSync(path.join(dir,'corpo-enviado.json'),response.request().postData());
    fs.writeFileSync(path.join(dir,'corpo-recebido.json'),text);
    fs.writeFileSync(path.join(dir,'resposta-http.json'),JSON.stringify({url:response.url(),status:response.status(),headers:await response.allHeaders(),corpo:data},null,2)+'\n');
    result.etapas.push('Aplicar o cupom pelo formulário');
    if(data.cupom?.aplicado===true)await page.getByRole('button',{name:'Remover cupom',exact:true}).waitFor({state:'visible'});
    await page.waitForLoadState('networkidle');
    fs.writeFileSync(path.join(dir,'texto-depois.txt'),await page.locator('body').innerText());
    await page.screenshot({path:path.join(dir,'depois-de-aplicar.png'),fullPage:true});
    const add=(name,expected,actual,ok)=>result.verificacoes.push({verificacao:name,esperado:expected,encontrado:actual,resultado:ok?'Aprovado':'Falhou'});
    const label=await page.locator('.cupom-aplicado p').count()?normalize(await page.locator('.cupom-aplicado p').innerText()):'Cupom não aplicado';
    const remove=await page.getByRole('button',{name:'Remover cupom',exact:true}).isVisible();
    add('Cupom aplicado na tela','Cupom BEMVINDO10 aplicado.',label,label==='Cupom BEMVINDO10 aplicado.'&&remove);
    add('Código retornado pela API','BEMVINDO10',data.cupom?.codigo,data.cupom?.codigo==='BEMVINDO10'&&data.cupom?.aplicado===true);
    for(const [key,expected] of [['subtotal','R$ 100,00'],['desconto','- R$ 10,00'],['frete','R$ 19,90'],['total','R$ 109,90']]){
     const found=normalize(await page.locator('[data-valor="'+key+'"]').innerText());add(key,expected,found,found===expected);
    }
    result.resultado=result.verificacoes.every(c=>c.resultado==='Aprovado')?'Aprovado':'Falhou';
   }catch(e){result.resultado='Bloqueado';result.erro=e.message;fs.writeFileSync(path.join(dir,'erro-interface.txt'),e.stack);await page.screenshot({path:path.join(dir,'tela-no-erro.png'),fullPage:true}).catch(()=>{});}
   finally{fs.writeFileSync(path.join(dir,'validacao-interface.json'),JSON.stringify(result,null,2)+'\n');await context.close();results.push(result);}
  }
 }finally{await browser.close();fs.writeFileSync(path.join(root,'resumo-interface.json'),JSON.stringify(results,null,2)+'\n');}
 console.log(JSON.stringify(results,null,2));
})().catch(e=>{console.error(e.message);process.exitCode=1});
