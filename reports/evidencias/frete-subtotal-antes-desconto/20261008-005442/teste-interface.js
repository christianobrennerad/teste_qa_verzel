const fs=require('fs');const path=require('path');const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'/tmp/verzel-browser/node_modules/playwright');
const root=process.argv[2];if(!root)throw new Error('Informe o diretório de evidências');const cases=JSON.parse(fs.readFileSync(path.join(root,'casos.json'),'utf8'));
const names={P001:'Camiseta Essencial',P002:'Calça Jeans Slim',P003:'Tênis Casual Urbano',P004:'Boné Aba Curva',P005:'Mochila Urbana 20L',P007:'Jaqueta Corta-Vento'};
const now=()=>new Date().toLocaleString('sv-SE',{timeZone:'America/Fortaleza'})+' (America/Fortaleza)';const normalize=s=>s.replace(/\s+/g,' ').trim();
const money=value=>'R$ '+value.toFixed(2).replace('.',',');const moneyRegex=/^R\$ [0-9]+,[0-9]{2}$/;
(async()=>{
 const proxyUrl=process.env.HTTPS_PROXY||process.env.https_proxy;const proxy=proxyUrl?{server:new URL(proxyUrl).origin}:undefined;
 const browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,proxy});const results=[];
 try{
  for(const c of cases){
   const dir=path.join(root,c.slug,'interface');fs.mkdirSync(dir,{recursive:true});const result={caso:c.slug,data:now(),itens:c.itens,tls:'Verificação TLS ativa',verificacoes:[]};
   const context=await browser.newContext({viewport:{width:1280,height:1000},locale:'pt-BR'});const page=await context.newPage();
   const check=(name,expected,found,ok)=>result.verificacoes.push({verificacao:name,esperado:expected,encontrado:found,resultado:ok?'Aprovado':'Falhou'});
   try{
    await page.goto('https://verzel-store.qa-test-verzel-store.workers.dev/',{waitUntil:'networkidle'});
    const responsePromise=page.waitForResponse(r=>{
     if(!r.url().endsWith('/api/carrinho/calcular')||r.request().method()!=='POST')return false;
     const body=r.request().postDataJSON();return body?.cupom==='BEMVINDO10'&&Array.isArray(body?.itens)&&body.itens.length===c.itens.length&&c.itens.every(w=>body.itens.some(i=>i.produtoId===w.produtoId&&i.quantidade===w.quantidade));
    });
    for(const item of c.itens){const card=page.locator('article').filter({has:page.getByRole('heading',{name:names[item.produtoId],exact:true})});for(let i=0;i<item.quantidade;i++){await card.getByRole('button',{name:'Adicionar ao carrinho',exact:true}).click();await page.waitForLoadState('networkidle');}}
    await page.getByRole('link',{name:/Carrinho/}).click();await page.waitForLoadState('networkidle');
    await page.getByLabel('Cupom de desconto',{exact:true}).fill('BEMVINDO10');
    await page.screenshot({path:path.join(dir,'antes-do-cupom.png'),fullPage:true});
    await page.getByRole('button',{name:'Aplicar cupom',exact:true}).click();
    const response=await responsePromise;const body=await response.text();const data=JSON.parse(body);
    fs.writeFileSync(path.join(dir,'corpo-enviado.json'),response.request().postData());fs.writeFileSync(path.join(dir,'corpo-recebido.json'),body);fs.writeFileSync(path.join(dir,'resposta-http.json'),JSON.stringify({status:response.status(),url:response.url(),headers:await response.allHeaders(),corpo:data},null,2)+'\n');
    await page.getByRole('button',{name:'Remover cupom',exact:true}).waitFor({state:'visible'});await page.waitForLoadState('networkidle');await page.locator('[data-valor="total"]').waitFor({state:'visible'});
    const totals={};for(const key of ['subtotal','desconto','frete','total'])totals[key]=normalize(await page.locator('[data-valor="'+key+'"]').innerText());
    const notices=page.locator('.aviso-frete');const notice=await notices.count()?normalize(await notices.innerText()):null;
    fs.writeFileSync(path.join(dir,'texto-tela.txt'),await page.locator('body').innerText());fs.writeFileSync(path.join(dir,'estado.json'),JSON.stringify({data:now(),valores:totals,avisoFrete:notice,cupomAtivo:await page.locator('.cupom-aplicado').count()>0},null,2)+'\n');await page.screenshot({path:path.join(dir,'tela.png'),fullPage:true});
    check('Status do cálculo na interface',200,response.status(),response.status()===200);
    for(const [key,value] of Object.entries(c.esperado))check('API durante interação: '+key,value,data[key],data[key]===value);
    check('Cupom único aplicado',1,await page.locator('.cupom-aplicado').count(),await page.locator('.cupom-aplicado').count()===1&&data.cupom?.codigo==='BEMVINDO10'&&data.cupom?.aplicado===true);
    for(const key of ['subtotal','desconto','frete','total']){
     const expected=(key==='desconto'&&c.esperado[key]>0?'- ':'')+money(c.esperado[key]);const found=totals[key];const equivalent=found===expected||(key==='frete'&&c.esperado.frete===0&&found==='Grátis');
     check('Valor na tela: '+key,expected,found,equivalent);

    }
    check('Indicação de frete grátis',c.esperado.freteGratis,totals.frete==='Grátis'||totals.frete==='R$ 0,00',(totals.frete==='Grátis'||totals.frete==='R$ 0,00')===c.esperado.freteGratis);
    const expectedNotice=c.esperado.freteGratis?null:'Faltam '+money(c.esperado.valorFaltanteFreteGratis)+' para o frete grátis.';
    check('Aviso de valor faltante',expectedNotice,notice,notice===expectedNotice);
    result.resultado=result.verificacoes.every(c=>c.resultado==='Aprovado')?'Aprovado':'Falhou';
   }catch(e){result.resultado='Bloqueado';result.erro=e.message;fs.writeFileSync(path.join(dir,'erro-interface.txt'),e.stack);await page.screenshot({path:path.join(dir,'tela-no-erro.png'),fullPage:true}).catch(()=>{});}
   finally{fs.writeFileSync(path.join(dir,'validacao-interface.json'),JSON.stringify(result,null,2)+'\n');await context.close();results.push(result);}
  }
 }finally{await browser.close();fs.writeFileSync(path.join(root,'resumo-interface.json'),JSON.stringify(results,null,2)+'\n')}
 console.log(JSON.stringify(results.map(r=>({caso:r.caso,data:r.data,resultado:r.resultado,falhas:r.verificacoes.filter(c=>c.resultado!=='Aprovado'),erro:r.erro})),null,2));
})().catch(e=>{console.error(e.message);process.exitCode=1});
