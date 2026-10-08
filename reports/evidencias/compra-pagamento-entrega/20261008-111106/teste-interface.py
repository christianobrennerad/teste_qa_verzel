from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
from zoneinfo import ZoneInfo
import base64
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
import traceback
import sys
from marionette_driver.marionette import Marionette
from marionette_driver.by import By

BASE = 'https://verzel-store.qa-test-verzel-store.workers.dev'
TZ = ZoneInfo('America/Fortaleza')
def now():
    return datetime.now(TZ).isoformat(timespec='seconds')

start = now()
root = Path('reports/evidencias/compra-pagamento-entrega') / datetime.now(TZ).strftime('%Y%m%d-%H%M%S')
root.mkdir(parents=True)
Path('/tmp/verzel-compra-pagamento-entrega-run.txt').write_text(str(root.resolve()))
shutil.copyfile(__file__, root / 'teste-interface.py')
def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def js(code):
    return browser.execute_script(code, sandbox=None)

def wait(condition):
    until = time.monotonic() + 25
    while time.monotonic() < until:
        if js('return ' + condition):
            return
        time.sleep(0.2)
    raise TimeoutError('A interface não atingiu o estado esperado: ' + condition)

def button(text):
    return next(b for b in browser.find_elements(By.CSS_SELECTOR, 'button') if b.text.strip() == text)

def snapshot(slug):
    folder = root / slug
    folder.mkdir()
    state = js('''const visible=e=>!!e&&!!(e.offsetWidth||e.offsetHeight||e.getClientRects().length);
return {url:location.href,caminho:location.pathname,titulo:document.title,texto:document.body.innerText,
valores:Object.fromEntries([...document.querySelectorAll('[data-valor]')].map(e=>[e.dataset.valor,e.textContent.trim()])),
numeroPedido:document.querySelector('.numero-pedido')?.textContent.trim()||null,
cupomVisivel:document.querySelector('.cupom-aplicado')?.innerText||null,
pagamento:document.querySelector('.pagamento-info')?.innerText||null,
camposVisiveis:[...document.querySelectorAll('input,select,textarea')].filter(visible).map(e=>({id:e.id,nome:e.name,tipo:e.type||e.tagName,valor:e.value,autocomplete:e.autocomplete})),
botoesVisiveis:[...document.querySelectorAll('button')].filter(visible).map(e=>e.innerText.trim()),
iframesVisiveis:[...document.querySelectorAll('iframe')].filter(visible).map(e=>({src:e.src,title:e.title})),
itensCarrinho:JSON.parse(sessionStorage.getItem('verzel-store:itens')||'[]'),
cupomCarrinho:JSON.parse(sessionStorage.getItem('verzel-store:cupom')||'null'),
quantidadeP005:document.querySelector('output[aria-label="Quantidade de Mochila Urbana 20L"]')?.innerText.trim()||null};''')
    state['data'] = now()
    save(folder / 'estado.json', state)
    (folder / 'texto-tela.txt').write_text(state['texto'] + '\n')
    (folder / 'pagina.html').write_text(browser.page_source)
    (folder / 'tela.png').write_bytes(base64.b64decode(browser.screenshot(format='base64', full=True)))
    return state

checks = []
def check(label, expected, actual, ok):
    checks.append({'verificacao': label, 'esperado': expected, 'encontrado': actual, 'resultado': 'Aprovado' if ok else 'Falhou'})

save(root / 'criterios.json', {'produto': 'P005', 'quantidade': 1, 'precoUnitario': 100, 'cupom': 'BEMVINDO10', 'cliente': {'nome': 'Maria Silva', 'email': 'maria@exemplo.com', 'cep': '01310-100'}, 'numeroPedidoRegex': '^VZ-[0-9]{6}$', 'total': 109.9, 'pagamento': 'Na entrega', 'etapaPagamentoOnline': False})
browser = None
result = {'inicio': start, 'timezone': 'America/Fortaleza', 'verificacoes': checks, 'acoes': []}
def action(description):
    result['acoes'].append({'data': now(), 'acao': description})

try:
    profile = tempfile.mkdtemp(prefix='verzel-firefox-compra-')
    subprocess.run(['certutil', '-N', '--empty-password', '-d', 'sql:' + profile], check=True, capture_output=True)
    subprocess.run(['certutil', '-A', '-n', 'Proxy oficial do ambiente', '-t', 'C,,', '-i', '/usr/local/share/ca-certificates/environment-proxy-ca.crt', '-d', 'sql:' + profile], check=True, capture_output=True)
    prefs = {}
    proxy = urlparse(os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy') or '')
    if proxy.hostname:
        prefs = {'network.proxy.type': 1, 'network.proxy.http': proxy.hostname, 'network.proxy.http_port': proxy.port or 80, 'network.proxy.ssl': proxy.hostname, 'network.proxy.ssl_port': proxy.port or 80, 'network.proxy.no_proxies_on': 'localhost,127.0.0.1'}
    browser = Marionette(bin='/tmp/verzel-firefox-debian/usr/lib/firefox-esr/firefox-esr', profile=profile, headless=True, port=0, prefs=prefs, gecko_log=str(root / 'firefox-gecko.log'))
    caps = browser.start_session({'acceptInsecureCerts': False})
    browser.set_window_rect(width=1280, height=1000)
    result['navegador'] = {'nome': caps['browserName'], 'versao': caps['browserVersion'], 'acceptInsecureCerts': caps['acceptInsecureCerts'], 'viewport': '1280 x 1000'}
    result['tls'] = 'Verificação ativa; certificado oficial do proxy importado somente no perfil temporário do teste.'
    browser.navigate(BASE + '/')
    wait("document.querySelector('#nome-P005')!==null")
    js('''window.__qaRede=[];window.__qaRotas=[{data:new Date().toISOString(),caminho:location.pathname}];window.__qaErros=[];
window.addEventListener('error',e=>window.__qaErros.push({tipo:'error',mensagem:e.message}));
window.addEventListener('unhandledrejection',e=>window.__qaErros.push({tipo:'unhandledrejection',mensagem:String(e.reason)}));
const originalFetch=window.fetch.bind(window);window.fetch=async(...args)=>{const inicio=new Date().toISOString();const response=await originalFetch(...args);const body=await response.clone().text();window.__qaRede.push({inicio,fim:new Date().toISOString(),url:response.url,metodo:args[1]?.method||'GET',cabecalhosEnviados:Object.fromEntries(new Headers(args[1]?.headers).entries()),corpoEnviado:args[1]?.body||null,status:response.status,cabecalhosRecebidos:Object.fromEntries(response.headers.entries()),corpoRecebido:body});return response;};
const originalPush=history.pushState.bind(history);history.pushState=(...args)=>{const r=originalPush(...args);window.__qaRotas.push({data:new Date().toISOString(),caminho:location.pathname});return r;};
window.addEventListener('popstate',()=>window.__qaRotas.push({data:new Date().toISOString(),caminho:location.pathname}));''')
    catalog = snapshot('01-produto')
    card = next(x for x in browser.find_elements(By.CSS_SELECTOR, 'article') if 'Mochila Urbana 20L' in x.text)
    product_text = card.text
    check('Produto no catálogo', 'P005 — Mochila Urbana 20L, R$ 100,00', product_text, 'Mochila Urbana 20L' in product_text and re.search(r'R\$\s*100,00', product_text) is not None)
    card.find_element(By.CSS_SELECTOR, 'button').click()
    action('Clicou em Adicionar ao carrinho no produto Mochila Urbana 20L (P005).')
    wait("window.__qaRede.some(r=>r.url.endsWith('/api/carrinho/calcular'))")
    browser.find_element(By.CSS_SELECTOR, 'a[href="/carrinho"]').click()
    wait("location.pathname==='/carrinho'&&document.querySelector('#campo-cupom')!==null")
    before = snapshot('02-carrinho-sem-cupom')
    check('Carrinho preparado', 'Uma unidade de P005', before['itensCarrinho'], before['itensCarrinho'] == [{'produtoId': 'P005', 'quantidade': 1}] and before['quantidadeP005'] == '1')
    browser.find_element(By.ID, 'campo-cupom').send_keys('BEMVINDO10')
    button('Aplicar cupom').click()
    action('Digitou BEMVINDO10 e clicou em Aplicar cupom.')
    wait("document.querySelector('.cupom-aplicado')!==null&&window.__qaRede.some(r=>r.corpoEnviado&&JSON.parse(r.corpoEnviado).cupom==='BEMVINDO10')")
    cart = snapshot('03-carrinho-com-cupom')
    check('Cupom aplicado na interface', 'BEMVINDO10 aplicado', cart['cupomVisivel'], bool(cart['cupomVisivel']) and 'BEMVINDO10' in cart['cupomVisivel'] and cart['cupomCarrinho'] == 'BEMVINDO10')
    browser.find_element(By.CSS_SELECTOR, 'a[href="/checkout"]').click()
    action('Clicou em Finalizar compra.')
    wait("location.pathname==='/checkout'&&document.querySelector('#campo-nome')!==null")
    for field, value in {'nome': 'Maria Silva', 'email': 'maria@exemplo.com', 'cep': '01310-100'}.items():
        browser.find_element(By.ID, 'campo-' + field).send_keys(value)
    action('Preencheu nome Maria Silva, e-mail maria@exemplo.com e CEP 01310-100.')
    checkout = snapshot('04-dados-para-entrega')
    check('Dados preenchidos na interface', {'nome': 'Maria Silva', 'email': 'maria@exemplo.com', 'cep': '01310-100'}, {e['nome']: e['valor'] for e in checkout['camposVisiveis']}, {e['nome']: e['valor'] for e in checkout['camposVisiveis']} == {'nome': 'Maria Silva', 'email': 'maria@exemplo.com', 'cep': '01310-100'})
    button('Confirmar pedido').click()
    action('Clicou em Confirmar pedido uma vez.')
    wait("location.pathname==='/pedido-confirmado'&&document.querySelector('.numero-pedido')!==null&&window.__qaRede.some(r=>r.url.endsWith('/api/pedidos'))")
    confirmed = snapshot('05-pedido-confirmado')
    network = js('return window.__qaRede')
    routes = js('return window.__qaRotas')
    errors = js('return window.__qaErros')
    save(root / 'rede-navegador.json', network)
    save(root / 'rotas-percorridas.json', routes)
    save(root / 'erros-pagina.json', errors)
    orders = [e for e in network if e['url'].endswith('/api/pedidos')]
    save(root / 'resposta-pedido-http.json', orders[-1])
    (root / 'pedido-corpo-enviado.json').write_text(orders[-1]['corpoEnviado'] + '\n')
    (root / 'pedido-corpo-recebido.json').write_text(orders[-1]['corpoRecebido'] + '\n')
    order_request = json.loads(orders[-1]['corpoEnviado'])
    order = json.loads(orders[-1]['corpoRecebido'])
    check('Uma confirmação enviada pela interface', 1, len(orders), len(orders) == 1)
    check('Conteúdo do pedido enviado pela interface', {'cliente': {'nome': 'Maria Silva', 'email': 'maria@exemplo.com', 'cep': '01310-100'}, 'itens': [{'produtoId': 'P005', 'quantidade': 1}], 'cupom': 'BEMVINDO10'}, order_request, order_request == {'cliente': {'nome': 'Maria Silva', 'email': 'maria@exemplo.com', 'cep': '01310-100'}, 'itens': [{'produtoId': 'P005', 'quantidade': 1}], 'cupom': 'BEMVINDO10'})
    check('Pedido aceito pela API durante a compra', 201, orders[-1]['status'], orders[-1]['status'] == 201)
    check('Número de confirmação exibido', 'VZ- seguido por seis dígitos', confirmed['numeroPedido'], bool(re.fullmatch(r'VZ-[0-9]{6}', confirmed['numeroPedido'] or '')) and confirmed['numeroPedido'] == order.get('numero'))
    check('Total confirmado na interface', 'R$ 109,90', confirmed['valores'].get('total'), bool(re.fullmatch(r'R\$\s*109,90', confirmed['valores'].get('total', ''))))
    check('Total retornado na confirmação', 109.9, order.get('total'), type(order.get('total')) in (int, float) and order.get('total') == 109.9)
    check('Pagamento na entrega antes da confirmação', 'O pagamento é feito na entrega.', checkout['pagamento'], checkout['pagamento'] == 'O pagamento é feito na entrega.')
    check('Pagamento na entrega após a confirmação', 'Mensagem visível informando pagamento na entrega', confirmed['texto'], 'o pagamento será feito na entrega.' in confirmed['texto'])
    paths = [r['caminho'] for r in routes]
    permitted = ['/', '/carrinho', '/checkout', '/pedido-confirmado']
    check('Fluxo sem etapa de pagamento online', 'Produtos → carrinho → dados de entrega → confirmação; sem campos de pagamento ou iframe visível', {'rotas': paths, 'camposCheckout': [e['nome'] for e in checkout['camposVisiveis']], 'camposConfirmacao': confirmed['camposVisiveis'], 'iframesCheckout': checkout['iframesVisiveis'], 'iframesConfirmacao': confirmed['iframesVisiveis']}, paths == permitted and [e['nome'] for e in checkout['camposVisiveis']] == ['nome', 'email', 'cep'] and not confirmed['camposVisiveis'] and not checkout['iframesVisiveis'] and not confirmed['iframesVisiveis'])
    result['resultado'] = 'Aprovado' if all(c['resultado'] == 'Aprovado' for c in checks) else 'Falhou'
    result['numeroPedido'] = confirmed['numeroPedido']
except Exception as error:
    result['resultado'] = 'Bloqueado'
    result['erro'] = str(error)
    (root / 'erro-execucao.txt').write_text(traceback.format_exc())
    if browser:
        try:
            snapshot('estado-no-erro')
            save(root / 'rede-navegador.json', js('return window.__qaRede||[]'))
            save(root / 'rotas-percorridas.json', js('return window.__qaRotas||[]'))
        except Exception:
            pass
finally:
    result['fim'] = now()
    save(root / 'validacao-interface.json', result)
    print(json.dumps({'evidencias': str(root), 'resultado': result['resultado'], 'inicio': result['inicio'], 'fim': result['fim'], 'numeroPedido': result.get('numeroPedido'), 'erro': result.get('erro'), 'falhas': [c for c in checks if c['resultado'] != 'Aprovado']}, ensure_ascii=False), flush=True)
    if browser:
        try:
            browser.delete_session()
        finally:
            browser.cleanup()
sys.exit(0 if result['resultado'] == 'Aprovado' else 1)
