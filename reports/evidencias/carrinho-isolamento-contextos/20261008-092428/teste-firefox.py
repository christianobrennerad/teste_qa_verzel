from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from urllib.parse import urlparse
import os,json,subprocess,tempfile,time,base64,shutil,sys,traceback
from marionette_driver.marionette import Marionette
from marionette_driver.by import By

ROOT=Path(sys.argv[1]);BASE='https://verzel-store.qa-test-verzel-store.workers.dev';TZ=ZoneInfo('America/Fortaleza')
def now():return datetime.now(TZ).isoformat(timespec='seconds')
def save(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def js(m,code):return m.execute_script(code,sandbox=None)
def wait(m,condition):
    until=time.monotonic()+25
    while time.monotonic()<until:
        if js(m,'return '+condition):return
        time.sleep(.2)
    raise TimeoutError('A interface não atingiu o estado esperado: '+condition)
def snapshot(m,folder):
    folder.mkdir(parents=True,exist_ok=True)
    state=js(m,'''const visible=e=>!!e&&!!(e.offsetWidth||e.offsetHeight||e.getClientRects().length);
const empty=[...document.querySelectorAll('h1')].find(e=>e.textContent.trim()==='Seu carrinho está vazio');
const qty=document.querySelector('output[aria-label="Quantidade de Mochila Urbana 20L"]');
return {url:location.href,titulo:document.title,itens:JSON.parse(sessionStorage.getItem('verzel-store:itens')||'[]'),cupom:JSON.parse(sessionStorage.getItem('verzel-store:cupom')||'null'),temOpener:window.opener!==null,carrinhoVazioVisivel:visible(empty),quantidadeP005:qty?qty.textContent.trim():null,nomesExibidos:[...document.querySelectorAll('.item-carrinho h3')].map(e=>e.textContent.trim()),texto:document.body.innerText};''')
    state['data']=now();save(folder/'estado.json',state);(folder/'texto-tela.txt').write_text(state['texto']);(folder/'tela.png').write_bytes(base64.b64decode(m.screenshot(format='base64',full=True)));return state
def launch_firefox(folder):
    profile=tempfile.mkdtemp(prefix='verzel-firefox-isolamento-')
    subprocess.run(['certutil','-N','--empty-password','-d','sql:'+profile],check=True,capture_output=True)
    subprocess.run(['certutil','-A','-n','Proxy oficial do ambiente','-t','C,,','-i','/usr/local/share/ca-certificates/environment-proxy-ca.crt','-d','sql:'+profile],check=True,capture_output=True)
    prefs={'browser.privatebrowsing.autostart':False};p=urlparse(os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy') or '')
    if p.hostname:prefs.update({'network.proxy.type':1,'network.proxy.http':p.hostname,'network.proxy.http_port':p.port or 80,'network.proxy.ssl':p.hostname,'network.proxy.ssl_port':p.port or 80,'network.proxy.no_proxies_on':'localhost,127.0.0.1'})
    m=Marionette(bin='/tmp/verzel-firefox-debian/usr/lib/firefox-esr/firefox-esr',profile=profile,headless=True,port=0,prefs=prefs,gecko_log=str(folder/'firefox-gecko.log'))
    caps=m.start_session({'acceptInsecureCerts':False});m.set_window_rect(width=1280,height=1000)
    return m,{'nome':caps['browserName'],'versao':caps['browserVersion'],'acceptInsecureCerts':caps['acceptInsecureCerts']}
result={'inicio':now(),'navegadorOriginal':'Firefox','tls':'Verificação TLS ativa; certificado oficial do proxy em perfis temporários','casos':[]}
for slug,name in [('01-outra-aba','outra aba'),('02-outro-navegador','outro navegador'),('03-janela-anonima','janela anônima')]:
    folder=ROOT/slug;folder.mkdir(parents=True);r={'contexto':name,'inicio':now(),'verificacoes':[]};m=None;child=None
    def check(label,want,found,ok):r['verificacoes'].append({'verificacao':label,'esperado':want,'encontrado':found,'resultado':'Aprovado' if ok else 'Falhou'})
    try:
        m,caps=launch_firefox(folder);r['navegadorOriginal']=caps;original=m.current_window_handle
        m.navigate(BASE+'/');wait(m,"[...document.querySelectorAll('article')].some(e=>e.textContent.includes('Mochila Urbana 20L'))")
        js(m,'''window.__qaCalculos=[];const originalFetch=window.fetch.bind(window);window.fetch=async(...args)=>{const response=await originalFetch(...args);if(String(args[0]).endsWith('/api/carrinho/calcular')){window.__qaCalculos.push({url:response.url,metodo:args[1]?.method||'GET',corpoEnviado:args[1]?.body,status:response.status,cabecalhos:Object.fromEntries(response.headers.entries()),corpoRecebido:await response.clone().text()});}return response;};''')
        card=next(x for x in m.find_elements(By.CSS_SELECTOR,'article') if 'Mochila Urbana 20L' in x.text)
        card.find_element(By.CSS_SELECTOR,'button').click()
        wait(m,"window.__qaCalculos?.length>0&&JSON.parse(sessionStorage.getItem('verzel-store:itens')||'[]').some(x=>x.produtoId==='P005'&&x.quantidade===1)")
        network=js(m,'return window.__qaCalculos[window.__qaCalculos.length-1]')
        (folder/'corpo-enviado.json').write_text(network['corpoEnviado']);(folder/'corpo-recebido.json').write_text(network['corpoRecebido']);save(folder/'resposta-http.json',network)
        m.find_element(By.CSS_SELECTOR,'a[href="/carrinho"]').click();wait(m,"document.querySelector('output[aria-label=\"Quantidade de Mochila Urbana 20L\"]')?.textContent.trim()==='1'&&document.querySelector('[data-valor=\"total\"]')?.textContent.includes('119,90')")
        before=snapshot(m,folder/'original-antes');check('Original preparada com P005','Uma unidade de P005',before['itens'],before['itens']==[{'produtoId':'P005','quantidade':1}] and before['quantidadeP005']=='1' and 'Mochila Urbana 20L' in before['nomesExibidos'])
        check('Status do cálculo da preparação',200,network['status'],network['status']==200)
        if name=='outro navegador':
            child=subprocess.Popen(['node','/tmp/verzel-isolamento-chromium-novo.js',str(folder/'novo-contexto')],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=(folder/'chromium-stderr.txt').open('w'),text=True)
            ready=json.loads(child.stdout.readline());assert ready.get('pronto'),ready
            fresh=ready['estado'];r['metodo']='Firefox original e processo separado de Chromium mantidos abertos simultaneamente'
            r['novoNavegador']=fresh['navegador']
        else:
            options={'type':'tab','focus':True} if name=='outra aba' else {'type':'window','focus':True,'private':True}
            opened=m.open(**options);save(folder/'contexto-aberto.json',{'solicitado':options,'aberto':opened,'distintoDaOriginal':opened['handle']!=original})
            m.switch_to_window(opened['handle']);m.navigate(BASE+'/');wait(m,"document.querySelector('a[href=\"/carrinho\"]')!==null")
            m.find_element(By.CSS_SELECTOR,'a[href="/carrinho"]').click();wait(m,"location.pathname==='/carrinho'&&document.querySelector('h1')!==null")
            fresh=snapshot(m,folder/'novo-contexto');r['metodo']='Nova aba do mesmo perfil do Firefox, sem duplicação' if name=='outra aba' else 'Nova janela privada do Firefox, criada com private=true'
            check('Contexto distinto da aba original',True,opened['handle']!=original,opened['handle']!=original)
        check('Novo contexto começa vazio','Aviso visível de carrinho vazio, sem itens',{'avisoVisivel':fresh['carrinhoVazioVisivel'],'itens':fresh['itens'],'quantidadeP005':fresh['quantidadeP005']},fresh['carrinhoVazioVisivel'] and fresh['itens']==[] and fresh['quantidadeP005'] is None)
        m.switch_to_window(original);after=snapshot(m,folder/'original-depois')
        check('Original mantém P005 após abrir novo contexto','Uma unidade de P005',after['itens'],after['itens']==[{'produtoId':'P005','quantidade':1}] and after['quantidadeP005']=='1' and 'Mochila Urbana 20L' in after['nomesExibidos'])
        r['resultado']='Aprovado' if all(x['resultado']=='Aprovado' for x in r['verificacoes']) else 'Falhou'
    except Exception as e:
        r['resultado']='Bloqueado';r['erro']=str(e);(folder/'erro-interface.txt').write_text(traceback.format_exc())
        if m:
            try:snapshot(m,folder/'estado-no-erro')
            except Exception:pass
    finally:
        if child:
            if child.poll() is None:child.communicate('concluir\n',timeout=30)
        if m:
            try:m.delete_session()
            finally:m.cleanup()
        r['fim']=now();save(folder/'validacao-interface.json',r);result['casos'].append(r)
        print(json.dumps({'contexto':name,'resultado':r['resultado'],'erro':r.get('erro'),'falhas':[x for x in r['verificacoes'] if x['resultado']=='Falhou']},ensure_ascii=False),flush=True)
result['fim']=now();result['resultado']='Falhou' if any(r['resultado']=='Falhou' for r in result['casos']) else 'Bloqueado' if any(r['resultado']=='Bloqueado' for r in result['casos']) else 'Aprovado'
save(ROOT/'resumo-interface.json',result)
sys.exit(0 if result['resultado']=='Aprovado' else 1)
