const fs=require('fs');const path=require('path');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'/tmp/verzel-browser/node_modules/playwright');
const root=process.argv[2];if(!root)throw new Error('Informe o diretório de evidências');
const dir=path.join(root,'01-p003','interface');fs.mkdirSync(dir,{recursive:true});
const normalize=s=>s.replace(/\s+/g,' ').trim();
const now=()=>new Date().toLocaleString('sv-SE',{timeZone:'America/Fortaleza'})+' (America/Fortaleza)';
(async()=>{
 const proxyUrl=process.env.HTTPS_PROXY||process.env.https_proxy;
 const proxy=proxyUrl?{server:new URL(proxyUrl).origin}:undefined;
 const browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,proxy});
 const context=await browser.newContext({viewport:{width:1280,height:1000},locale:'pt-BR'});
 const page=await context.newPage();const result={inicio:now(),tls:'Verificação TLS ativa',verificacoes:[]};
 const check=(name,expected,found,ok)=>result.verificacoes.push({verificacao:name,esperado:expected,encontrado:found,resultado:ok?'Aprovado':'Falhou'});
 try{
  await page.goto('https://verzel-store.qa-test-verzel-store.workers.dev/',{waitUntil:'networkidle'});
  const card=page.locator('article').filter({has:page.getByRole('heading',{name:'Tênis Casual Urbano',exact:true})});
  fs.writeFileSync(path.join(dir,'produto-texto.txt'),await card.innerText());
  const responsePromise=page.waitForResponse(r=>{
   if(!r.url().endsWith('/api/carrinho/calcular')||r.request().method()!=='POST')return false;
   const b=r.request().postDataJSON();return !b?.cupom&&b?.itens?.length===1&&b.itens[0].produtoId==='P003'&&b.itens[0].quantidade===1;
  });
  await card.getByRole('button',{name:'Adicionar ao carrinho',exact:true}).click();
  const response=await responsePromise;const raw=await response.text();const data=JSON.parse(raw);
  fs.writeFileSync(path.join(dir,'corpo-enviado.json'),response.request().postData());
  fs.writeFileSync(path.join(dir,'corpo-recebido.json'),raw);
  fs.writeFileSync(path.join(dir,'resposta-http.json'),JSON.stringify({data:now(),status:response.status(),url:response.url(),headers:await response.allHeaders(),corpo:data},null,2)+'\n');
  await page.getByRole('link',{name:/Carrinho/}).click();await page.waitForLoadState('networkidle');
  await page.locator('[data-valor="frete"]').waitFor({state:'visible'});
  const values={};for(const k of ['subtotal','desconto','frete','total'])values[k]=normalize(await page.locator('[data-valor="'+k+'"]').innerText());
  const notice=page.locator('.aviso-frete');const noticeVisible=await notice.isVisible();
  const noticeText=normalize(await notice.innerText());const text=await page.locator('body').innerText();
  const inputs=await page.locator('input').evaluateAll(xs=>xs.map(x=>({tipo:x.type,nome:x.name,valor:x.value,min:x.min,max:x.max})));
  const state={data:now(),url:page.url(),valores:values,avisoFrete:noticeText,avisoVisivel:noticeVisible,freteVisivel:await page.locator('[data-valor="frete"]').isVisible(),campos:inputs,cupomAtivo:await page.locator('.cupom-aplicado').count()>0};
  fs.writeFileSync(path.join(dir,'texto-tela.txt'),text);
  fs.writeFileSync(path.join(dir,'estado.json'),JSON.stringify(state,null,2)+'\n');
  await page.screenshot({path:path.join(dir,'tela.png'),fullPage:true});
  check('Carrinho com uma unidade de P003',[{produtoId:'P003',quantidade:1}],response.request().postDataJSON().itens,JSON.stringify(response.request().postDataJSON().itens)===JSON.stringify([{produtoId:'P003',quantidade:1}]));
  check('Subtotal do produto','R$ 189,90',values.subtotal,values.subtotal==='R$ 189,90');
  check('Frete visível na tela','R$ 19,90',values.frete,state.freteVisivel&&values.frete==='R$ 19,90');
  check('Aviso visível de valor faltante','Faltam R$ 10,10 para o frete grátis.',noticeText,noticeVisible&&noticeText==='Faltam R$ 10,10 para o frete grátis.');
  check('Sem cupom aplicado',false,state.cupomAtivo,state.cupomAtivo===false);
  check('Status do cálculo recebido pelo navegador',200,response.status(),response.status()===200);
  check('Frete retornado no cálculo',19.9,data.frete,data.frete===19.9);
  check('Faltante retornado no cálculo',10.1,data.valorFaltanteFreteGratis,data.valorFaltanteFreteGratis===10.1);
  result.resultado=result.verificacoes.every(x=>x.resultado==='Aprovado')?'Aprovado':'Falhou';
 }catch(e){result.resultado='Bloqueado';result.erro=e.message;fs.writeFileSync(path.join(dir,'erro-interface.txt'),e.stack);await page.screenshot({path:path.join(dir,'tela-no-erro.png'),fullPage:true}).catch(()=>{});}
 finally{result.fim=now();fs.writeFileSync(path.join(dir,'validacao-interface.json'),JSON.stringify(result,null,2)+'\n');await browser.close();}
 console.log(JSON.stringify(result,null,2));if(result.resultado!=='Aprovado')process.exitCode=1;
})().catch(e=>{console.error(e.message);process.exitCode=1});
