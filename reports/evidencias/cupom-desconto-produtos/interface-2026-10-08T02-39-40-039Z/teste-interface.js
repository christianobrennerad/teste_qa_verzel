const fs=require('fs');const path=require('path');const {chromium}=require('/tmp/verzel-browser/node_modules/playwright');
const base=process.argv[2]; if(!base) throw new Error('Informe o diretório base de evidências como primeiro argumento');
const stamp=new Date().toISOString().replace(/[:.]/g,'-');const root=path.join(base,'interface-'+stamp);fs.mkdirSync(root);

function localTime(){return new Date().toLocaleString('sv-SE',{timeZone:'America/Fortaleza'})+' (America/Fortaleza)'}
const result={data:localTime(),ferramenta:'Playwright com Chromium',tls:'Verificação de certificado ativa; CA oficial autorizada pelo usuário',etapas:[],verificacoes:[]};
const normalize=s=>s.replace(/\s+/g,' ').trim();
(async()=>{
 const proxy=new URL(process.env.HTTPS_PROXY||process.env.https_proxy);
 const browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,proxy:{server:proxy.protocol+'//'+proxy.host}});
 const context=await browser.newContext({viewport:{width:1280,height:1000},locale:'pt-BR'});
 const page=await context.newPage();
 try{
  await page.goto('https://verzel-store.qa-test-verzel-store.workers.dev/',{waitUntil:'networkidle'});result.etapas.push('Abrir loja em contexto novo com carrinho vazio');
  const card=page.locator('article').filter({has:page.getByRole('heading',{name:'Mochila Urbana 20L',exact:true})});
  await card.getByRole('button',{name:'Adicionar ao carrinho',exact:true}).click();result.etapas.push('Adicionar uma unidade de Mochila Urbana 20L');
  await page.getByRole('link',{name:/Carrinho/}).click();await page.waitForLoadState('networkidle');
  await page.screenshot({path:path.join(root,'carrinho-antes.png'),fullPage:true});
  fs.writeFileSync(path.join(root,'texto-antes.txt'),await page.locator('body').innerText());
  await page.getByLabel('Cupom de desconto',{exact:true}).fill('BEMVINDO10');
  const responsePromise=page.waitForResponse(r=>r.url().endsWith('/api/carrinho/calcular')&&r.request().method()==='POST'&&r.request().postDataJSON()?.cupom==='BEMVINDO10');
  await page.getByRole('button',{name:'Aplicar cupom',exact:true}).click();result.etapas.push('Aplicar BEMVINDO10 pelo formulário');
  const response=await responsePromise;
  fs.writeFileSync(path.join(root,'resposta-calculo-interface.json'),await response.text());
  fs.writeFileSync(path.join(root,'requisicao-calculo-interface.json'),response.request().postData());
  fs.writeFileSync(path.join(root,'status-calculo-interface.json'),JSON.stringify({status:response.status(),url:response.url(),data:localTime()},null,2));
  await page.getByRole('button',{name:'Remover cupom',exact:true}).waitFor({state:'visible'});
  await page.waitForLoadState('networkidle');
  await page.screenshot({path:path.join(root,'carrinho-com-cupom.png'),fullPage:true});
  fs.writeFileSync(path.join(root,'texto-depois.txt'),await page.locator('body').innerText());
  for(const [key,expected] of [['subtotal','R$ 100,00'],['desconto','- R$ 10,00'],['frete','R$ 19,90'],['total','R$ 109,90']]){
   const found=await page.locator('[data-valor="'+key+'"]').innerText();
   result.verificacoes.push({verificacao:key,esperado:expected,encontrado:found,resultado:normalize(found)===expected?'Aprovado':'Falhou'});
  }
  const message=await page.locator('.cupom-aplicado p').innerText();const expected='Cupom aplicado: 10% de desconto nos produtos.';
  result.verificacoes.push({verificacao:'Mensagem visível',esperado:expected,encontrado:message,resultado:(await page.getByText(expected,{exact:true}).count())>0?'Aprovado':'Falhou'});
  const text=await page.locator('body').innerText();result.verificacoes.push({verificacao:'Cupom aplicado na tela',esperado:'BEMVINDO10 aplicado',encontrado:text.includes('BEMVINDO10')&&await page.getByRole('button',{name:'Remover cupom',exact:true}).isVisible()?'BEMVINDO10 aplicado':'Não confirmado',resultado:text.includes('BEMVINDO10')&&await page.getByRole('button',{name:'Remover cupom',exact:true}).isVisible()?'Aprovado':'Falhou'});
  result.resultado=result.verificacoes.every(c=>c.resultado==='Aprovado')?'Aprovado':'Falhou';
 }catch(e){result.resultado='Bloqueado';result.erro=e.message;fs.writeFileSync(path.join(root,'erro-interface.txt'),e.stack);await page.screenshot({path:path.join(root,'tela-no-erro.png'),fullPage:true}).catch(()=>{});}
 finally{fs.writeFileSync(path.join(root,'validacao-interface.json'),JSON.stringify(result,null,2)+'\n');await browser.close()}
 console.log(JSON.stringify({root,result},null,2));
})().catch(e=>{console.error(e);process.exitCode=1});
