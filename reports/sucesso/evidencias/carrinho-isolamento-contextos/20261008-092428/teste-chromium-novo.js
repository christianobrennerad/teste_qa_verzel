const fs=require('fs');const path=require('path');const {chromium}=require('/tmp/verzel-browser/node_modules/playwright');
const dir=process.argv[2];fs.mkdirSync(dir,{recursive:true});
(async()=>{
 const proxyUrl=process.env.HTTPS_PROXY||process.env.https_proxy;const proxy=proxyUrl?{server:new URL(proxyUrl).origin}:undefined;
 const browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,proxy});
 try{
  const context=await browser.newContext({viewport:{width:1280,height:1000},locale:'pt-BR'});const page=await context.newPage();
  await page.goto('https://verzel-store.qa-test-verzel-store.workers.dev/',{waitUntil:'networkidle'});
  await page.getByRole('link',{name:/Carrinho/}).click();await page.waitForLoadState('networkidle');
  const state={data:new Date().toLocaleString('sv-SE',{timeZone:'America/Fortaleza'}),url:page.url(),navegador:'Chromium '+browser.version(),carrinhoVazioVisivel:await page.getByRole('heading',{name:'Seu carrinho está vazio',exact:true}).isVisible(),itens:await page.evaluate(()=>JSON.parse(sessionStorage.getItem('verzel-store:itens')||'[]')),quantidadeP005:await page.locator('output[aria-label="Quantidade de Mochila Urbana 20L"]').count()?await page.locator('output[aria-label="Quantidade de Mochila Urbana 20L"]').innerText():null};
  fs.writeFileSync(path.join(dir,'estado.json'),JSON.stringify(state,null,2)+'\n');fs.writeFileSync(path.join(dir,'texto-tela.txt'),await page.locator('body').innerText());await page.screenshot({path:path.join(dir,'tela.png'),fullPage:true});
  process.stdout.write(JSON.stringify({pronto:true,estado:state})+'\n');
  process.stdin.resume();await new Promise(resolve=>{process.stdin.once('data',resolve);process.stdin.once('end',resolve)});
 }catch(e){fs.writeFileSync(path.join(dir,'erro.txt'),e.stack);process.stdout.write(JSON.stringify({pronto:false,erro:e.message})+'\n');process.exitCode=1;}
 finally{await browser.close();}
})().catch(e=>{console.error(e.stack);process.exitCode=1});
