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

root = Path('reports/evidencias/limites-independentes-produtos') / datetime.now(TZ).strftime('%Y%m%d-%H%M%S')
root.mkdir(parents=True)
Path('/tmp/verzel-limites-independentes-run.txt').write_text(str(root.resolve()))
shutil.copyfile(__file__, root / 'teste-interface.py')
def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

browser = None
checks = []
result = {'inicio': now(), 'timezone': 'America/Fortaleza', 'verificacoes': checks, 'acoes': []}
def js(code):
    return browser.execute_script(code, sandbox=None)

def wait(condition):
    until = time.monotonic() + 25
    while time.monotonic() < until:
        if js('return ' + condition):
            return
        time.sleep(0.2)
    raise TimeoutError('A interface não atingiu o estado esperado: ' + condition)

def action(text):
    result['acoes'].append({'data': now(), 'acao': text})

def check(label, wanted, found, ok):
    checks.append({'verificacao': label, 'esperado': wanted, 'encontrado': found, 'resultado': 'Aprovado' if ok else 'Falhou'})

def snapshot(slug):
    folder = root / slug
    folder.mkdir()
    state = js('''return {url:location.href,titulo:document.title,texto:document.body.innerText,
itens:JSON.parse(sessionStorage.getItem('verzel-store:itens')||'[]'),cupom:JSON.parse(sessionStorage.getItem('verzel-store:cupom')||'null'),
catalogo:Object.fromEntries(['P008','P005'].map(id=>{const c=document.querySelector('article[aria-labelledby="nome-'+id+'"]');return [id,c?{nome:c.querySelector('h3')?.innerText,preco:c.querySelector('.produto-preco')?.innerText,botaoDesabilitado:c.querySelector('button')?.disabled,aviso:c.querySelector('.produto-aviso')?.innerText}:null]})),
linhas:[...document.querySelectorAll('.item-carrinho')].map(e=>({nome:e.querySelector('h3')?.textContent.trim(),precoUnitario:e.querySelector('.item-unitario')?.textContent.trim(),quantidade:e.querySelector('output')?.textContent.trim(),total:e.querySelector('.item-total')?.textContent.trim(),aumentoDesabilitado:e.querySelector('button[aria-label^="Aumentar quantidade"]')?.disabled,aviso:e.querySelector('.item-limite')?.textContent.trim()||null})),
valores:Object.fromEntries([...document.querySelectorAll('[data-valor]')].map(e=>[e.dataset.valor,e.textContent.trim()])),calculosCapturados:window.__qaRede.length};''')
    state['data'] = now()
    save(folder / 'estado.json', state)
    (folder / 'texto-tela.txt').write_text(state['texto'] + '\n')
    (folder / 'pagina.html').write_text(browser.page_source)
    (folder / 'tela.png').write_bytes(base64.b64decode(browser.screenshot(format='base64', full=True)))
    return state

save(root / 'criterios.json', {'preparacao': [{'produtoId': 'P008', 'quantidade': 5}], 'precosUnitarios': {'P008': 50, 'P005': 100}, 'itensFinais': [{'produtoId': 'P008', 'quantidade': 5}, {'produtoId': 'P005', 'quantidade': 5}], 'subtotal': 750, 'cupom': None})
try:
    profile = tempfile.mkdtemp(prefix='verzel-firefox-independentes-')
    subprocess.run(['certutil', '-N', '--empty-password', '-d', 'sql:' + profile], check=True, capture_output=True)
    subprocess.run(['certutil', '-A', '-n', 'Proxy oficial do ambiente', '-t', 'C,,', '-i', '/usr/local/share/ca-certificates/environment-proxy-ca.crt', '-d', 'sql:' + profile], check=True, capture_output=True)
    proxy = urlparse(os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy') or '')
    prefs = {}
    if proxy.hostname:
        prefs = {'network.proxy.type': 1, 'network.proxy.http': proxy.hostname, 'network.proxy.http_port': proxy.port or 80, 'network.proxy.ssl': proxy.hostname, 'network.proxy.ssl_port': proxy.port or 80, 'network.proxy.no_proxies_on': 'localhost,127.0.0.1'}
    browser = Marionette(bin='/tmp/verzel-firefox-debian/usr/lib/firefox-esr/firefox-esr', profile=profile, headless=True, port=0, prefs=prefs, gecko_log=str(root / 'firefox-gecko.log'))
    caps = browser.start_session({'acceptInsecureCerts': False})
    browser.set_window_rect(width=1280, height=1000)
    result['navegador'] = {'nome': caps['browserName'], 'versao': caps['browserVersion'], 'acceptInsecureCerts': caps['acceptInsecureCerts'], 'janela': '1280 x 1000'}
    result['tls'] = 'Verificação ativa; certificado oficial do proxy somente no perfil temporário.'
    browser.navigate(BASE + '/')
    wait("document.querySelector('#nome-P008')!==null&&document.querySelector('#nome-P005')!==null")
    js('''window.__qaRede=[];window.__qaErros=[];window.addEventListener('error',e=>window.__qaErros.push({tipo:'error',mensagem:e.message}));window.addEventListener('unhandledrejection',e=>window.__qaErros.push({tipo:'unhandledrejection',mensagem:String(e.reason)}));const originalFetch=window.fetch.bind(window);window.fetch=async(...args)=>{const inicio=new Date().toISOString();const response=await originalFetch(...args);const body=await response.clone().text();if(response.url.includes('/api/'))window.__qaRede.push({inicio,fim:new Date().toISOString(),url:response.url,metodo:args[1]?.method||'GET',cabecalhosEnviados:Object.fromEntries(new Headers(args[1]?.headers).entries()),corpoEnviado:args[1]?.body||null,status:response.status,cabecalhosRecebidos:Object.fromEntries(response.headers.entries()),corpoRecebido:body});return response;};''')
    initial = snapshot('01-produtos')
    for pid, name, price in [('P008', 'Garrafa Térmica 750ml', '50,00'), ('P005', 'Mochila Urbana 20L', '100,00')]:
        card = initial['catalogo'][pid]
        check('Produto e preço de ' + pid, {'nome': name, 'preco': 'R$ ' + price}, card, card['nome'] == name and bool(re.fullmatch(r'R\$\s*' + price, card['preco'])))
    for q in range(1, 6):
        browser.find_element(By.CSS_SELECTOR, 'article[aria-labelledby="nome-P008"] button').click()
        action('Adicionou P008 pelo catálogo, preparando ' + str(q) + ' unidade(s).')
        wait("window.__qaRede.some(r=>r.corpoEnviado&&JSON.parse(r.corpoEnviado).itens?.some(i=>i.produtoId==='P008'&&i.quantidade===" + str(q) + '))')
    browser.find_element(By.CSS_SELECTOR, 'a[href="/carrinho"]').click()
    wait("location.pathname==='/carrinho'&&document.querySelector('output[aria-label=\"Quantidade de Garrafa Térmica 750ml\"]')!==null&&document.querySelector('[data-valor=\"subtotal\"]')!==null")
    prepared = snapshot('02-p008-no-limite')
    check('Preparação com P008 no limite', [{'produtoId': 'P008', 'quantidade': 5}], prepared['itens'], prepared['itens'] == [{'produtoId': 'P008', 'quantidade': 5}] and prepared['linhas'][0]['quantidade'] == '5')
    check('Subtotal da preparação', 'R$ 250,00', prepared['valores'].get('subtotal'), bool(re.fullmatch(r'R\$\s*250,00', prepared['valores'].get('subtotal', ''))))
    browser.find_element(By.CSS_SELECTOR, 'a[href="/"]').click()
    wait("location.pathname==='/'&&document.querySelector('#nome-P005')!==null")
    available = snapshot('03-p005-disponivel')
    check('P008 bloqueado no próprio limite', True, available['catalogo']['P008']['botaoDesabilitado'], available['catalogo']['P008']['botaoDesabilitado'] is True)
    check('P005 continua disponível com P008 no limite', False, available['catalogo']['P005']['botaoDesabilitado'], available['catalogo']['P005']['botaoDesabilitado'] is False)
    for q in range(1, 6):
        add = browser.find_element(By.CSS_SELECTOR, 'article[aria-labelledby="nome-P005"] button')
        if not add.is_enabled():
            check('Adição de P005 antes de atingir cinco', 'Botão habilitado para adicionar unidade ' + str(q), 'Botão desabilitado', False)
            break
        add.click()
        action('Adicionou P005 pelo catálogo, totalizando ' + str(q) + ' unidade(s), mantendo P008 no carrinho.')
        wait("window.__qaRede.some(r=>r.corpoEnviado&&JSON.parse(r.corpoEnviado).itens?.some(i=>i.produtoId==='P005'&&i.quantidade===" + str(q) + '))')
        state = js("return JSON.parse(sessionStorage.getItem('verzel-store:itens')||'[]')")
        wanted = {'P008': 5, 'P005': q}
        check('P008 preservado ao adicionar unidade ' + str(q) + ' de P005', wanted, state, {i['produtoId']: i['quantidade'] for i in state} == wanted and len(state) == 2)
    browser.find_element(By.CSS_SELECTOR, 'a[href="/carrinho"]').click()
    wait("location.pathname==='/carrinho'&&document.querySelector('[data-valor=\"subtotal\"]')!==null")
    final = snapshot('04-cinco-de-cada-produto')
    quantities = {i['produtoId']: i['quantidade'] for i in final['itens']}
    visible = {line['nome']: line['quantidade'] for line in final['linhas']}
    check('Cinco unidades de P008 no carrinho final', 5, {'armazenado': quantities.get('P008'), 'exibido': visible.get('Garrafa Térmica 750ml')}, quantities.get('P008') == 5 and visible.get('Garrafa Térmica 750ml') == '5')
    check('Cinco unidades de P005 no carrinho final', 5, {'armazenado': quantities.get('P005'), 'exibido': visible.get('Mochila Urbana 20L')}, quantities.get('P005') == 5 and visible.get('Mochila Urbana 20L') == '5')
    check('Subtotal exibido', 'R$ 750,00', final['valores'].get('subtotal'), bool(re.fullmatch(r'R\$\s*750,00', final['valores'].get('subtotal', ''))))
    network = js('return window.__qaRede')
    save(root / 'rede-navegador.json', network)
    save(root / 'erros-pagina.json', js('return window.__qaErros'))
    calculations = [r for r in network if r['url'].endswith('/api/carrinho/calcular')]
    final_network = calculations[-1]
    save(root / 'calculo-final-http.json', final_network)
    (root / 'calculo-final-corpo-enviado.json').write_text(final_network['corpoEnviado'] + '\n')
    (root / 'calculo-final-corpo-recebido.json').write_text(final_network['corpoRecebido'] + '\n')
    request = json.loads(final_network['corpoEnviado'])
    response = json.loads(final_network['corpoRecebido'])
    check('Cálculo final aceito pela loja', 200, final_network['status'], final_network['status'] == 200)
    check('Subtotal retornado à interface', 750, response.get('subtotal'), type(response.get('subtotal')) in (int, float) and response['subtotal'] == 750)
    check('Dois produtos no cálculo final', {'P008': 5, 'P005': 5}, response.get('itens'), {i['produtoId']: i['quantidade'] for i in response.get('itens', [])} == {'P008': 5, 'P005': 5} and len(response.get('itens', [])) == 2)
    check('Dois produtos enviados pela interface', {'P008': 5, 'P005': 5}, request.get('itens'), {i['produtoId']: i['quantidade'] for i in request.get('itens', [])} == {'P008': 5, 'P005': 5} and len(request.get('itens', [])) == 2)
    result['resultado'] = 'Aprovado' if all(c['resultado'] == 'Aprovado' for c in checks) else 'Falhou'
except Exception as error:
    result['resultado'] = 'Bloqueado'
    result['erro'] = str(error)
    (root / 'erro-execucao.txt').write_text(traceback.format_exc())
    if browser:
        try:
            snapshot('estado-no-erro')
            save(root / 'rede-navegador.json', js('return window.__qaRede||[]'))
        except Exception:
            pass
finally:
    result['fim'] = now()
    save(root / 'validacao-interface.json', result)
    print(json.dumps({'evidencias': str(root), 'resultado': result['resultado'], 'inicio': result['inicio'], 'fim': result['fim'], 'verificacoes': len(checks), 'erro': result.get('erro'), 'falhas': [c for c in checks if c['resultado'] != 'Aprovado']}, ensure_ascii=False), flush=True)
    if browser:
        try:
            browser.delete_session()
        finally:
            browser.cleanup()
sys.exit(0 if result['resultado'] == 'Aprovado' else 1)
