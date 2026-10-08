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
NAME = 'Garrafa Térmica 750ml'
TZ = ZoneInfo('America/Fortaleza')
def now():
    return datetime.now(TZ).isoformat(timespec='seconds')

root = Path('reports/evidencias/limite-cinco-unidades') / datetime.now(TZ).strftime('%Y%m%d-%H%M%S')
root.mkdir(parents=True)
Path('/tmp/verzel-limite-cinco-unidades-run.txt').write_text(str(root.resolve()))
shutil.copyfile(__file__, root / 'teste-interface.py')
def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

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

def action(description):
    result['acoes'].append({'data': now(), 'acao': description})

def check(label, wanted, actual, ok):
    checks.append({'verificacao': label, 'esperado': wanted, 'encontrado': actual, 'resultado': 'Aprovado' if ok else 'Falhou'})

def snapshot(slug):
    folder = root / slug
    folder.mkdir()
    state = js('''const inc=document.querySelector('button[aria-label="Aumentar quantidade de Garrafa Térmica 750ml"]');
return {url:location.href,titulo:document.title,texto:document.body.innerText,
produtoCatalogo:document.querySelector('#nome-P008')?.textContent.trim()||null,
precoCatalogo:document.querySelector('article[aria-labelledby="nome-P008"] .produto-preco')?.textContent.trim()||null,
precoNoCarrinho:document.querySelector('.item-unitario')?.textContent.trim()||null,
itens:JSON.parse(sessionStorage.getItem('verzel-store:itens')||'[]'),cupom:JSON.parse(sessionStorage.getItem('verzel-store:cupom')||'null'),
quantidade:document.querySelector('output[aria-label="Quantidade de Garrafa Térmica 750ml"]')?.textContent.trim()||null,
valores:Object.fromEntries([...document.querySelectorAll('[data-valor]')].map(e=>[e.dataset.valor,e.textContent.trim()])),
aumentarQuantidade:inc?{disabled:inc.disabled,ariaLabel:inc.getAttribute('aria-label'),texto:inc.innerText}:null,
avisoLimite:document.querySelector('.item-limite')?.textContent.trim()||null,
calculosCapturados:window.__qaRede.length};''')
    state['data'] = now()
    save(folder / 'estado.json', state)
    (folder / 'texto-tela.txt').write_text(state['texto'] + '\n')
    (folder / 'pagina.html').write_text(browser.page_source)
    (folder / 'tela.png').write_bytes(base64.b64decode(browser.screenshot(format='base64', full=True)))
    return state

save(root / 'criterios.json', {'produtoId': 'P008', 'nome': NAME, 'precoUnitario': 50, 'quantidadeInicial': 4, 'quantidadeAposAdicionar': 5, 'subtotal': 250, 'quantidadeAposTentarSexta': 5, 'subtotalAposTentarSexta': 250})
try:
    profile = tempfile.mkdtemp(prefix='verzel-firefox-limite-')
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
    wait("document.querySelector('#nome-P008')!==null")
    js('''window.__qaRede=[];window.__qaErros=[];window.addEventListener('error',e=>window.__qaErros.push({tipo:'error',mensagem:e.message}));window.addEventListener('unhandledrejection',e=>window.__qaErros.push({tipo:'unhandledrejection',mensagem:String(e.reason)}));const originalFetch=window.fetch.bind(window);window.fetch=async(...args)=>{const inicio=new Date().toISOString();const response=await originalFetch(...args);const body=await response.clone().text();if(response.url.includes('/api/'))window.__qaRede.push({inicio,fim:new Date().toISOString(),url:response.url,metodo:args[1]?.method||'GET',cabecalhosEnviados:Object.fromEntries(new Headers(args[1]?.headers).entries()),corpoEnviado:args[1]?.body||null,status:response.status,cabecalhosRecebidos:Object.fromEntries(response.headers.entries()),corpoRecebido:body});return response;};''')
    product = snapshot('01-produto')
    check('Produto e preço no catálogo', 'P008 — Garrafa Térmica 750ml, R$ 50,00', {'nome': product['produtoCatalogo'], 'preco': product['precoCatalogo']}, product['produtoCatalogo'] == NAME and bool(re.fullmatch(r'R\$\s*50,00', product['precoCatalogo'] or '')))
    for quantity in range(1, 5):
        browser.find_element(By.CSS_SELECTOR, 'article[aria-labelledby="nome-P008"] button').click()
        action('Clicou em Adicionar ao carrinho de P008, preparando ' + str(quantity) + ' unidade(s).')
        wait("window.__qaRede.some(r=>r.corpoEnviado&&JSON.parse(r.corpoEnviado).itens?.some(i=>i.produtoId==='P008'&&i.quantidade===" + str(quantity) + '))')
    browser.find_element(By.CSS_SELECTOR, 'a[href="/carrinho"]').click()
    wait("location.pathname==='/carrinho'&&document.querySelector('output[aria-label=\"Quantidade de Garrafa Térmica 750ml\"]')?.textContent.trim()==='4'&&document.querySelector('[data-valor=\"subtotal\"]')!==null")
    four = snapshot('02-quatro-unidades')
    check('Pré-condição de quatro unidades', 'Quatro unidades de P008', {'itens': four['itens'], 'quantidadeVisivel': four['quantidade']}, four['itens'] == [{'produtoId': 'P008', 'quantidade': 4}] and four['quantidade'] == '4')
    check('Subtotal inicial', 'R$ 200,00', four['valores'].get('subtotal'), bool(re.fullmatch(r'R\$\s*200,00', four['valores'].get('subtotal', ''))))
    inc_selector = 'button[aria-label="Aumentar quantidade de Garrafa Térmica 750ml"]'
    browser.find_element(By.CSS_SELECTOR, inc_selector).click()
    action('Clicou no botão + do carrinho para adicionar a quinta unidade.')
    wait("window.__qaRede.some(r=>r.corpoEnviado&&JSON.parse(r.corpoEnviado).itens?.some(i=>i.produtoId==='P008'&&i.quantidade===5))&&document.querySelector('[data-valor=\"subtotal\"]')?.textContent.includes('250,00')")
    five = snapshot('03-cinco-unidades')
    check('Quinta unidade adicionada', 'Cinco unidades de P008', {'itens': five['itens'], 'quantidadeVisivel': five['quantidade']}, five['itens'] == [{'produtoId': 'P008', 'quantidade': 5}] and five['quantidade'] == '5')
    check('Subtotal com cinco unidades', 'R$ 250,00', five['valores'].get('subtotal'), bool(re.fullmatch(r'R\$\s*250,00', five['valores'].get('subtotal', ''))))
    inc = browser.find_element(By.CSS_SELECTOR, inc_selector)
    attempt = {'inicio': now(), 'botaoHabilitadoAntes': inc.is_enabled(), 'acao': 'Tentativa de clique no mesmo botão + via interação nativa WebDriver, sem alterar disabled ou o DOM.'}
    try:
        inc.click()
        attempt['retornoClique'] = 'Comando concluído.'
    except Exception as error:
        attempt['retornoClique'] = 'A ferramenta recusou o clique: ' + str(error)
        attempt['tipoErro'] = type(error).__name__
    action('Tentou clicar no botão + novamente, sem remover o bloqueio do limite.')
    time.sleep(1)
    after = snapshot('04-apos-tentar-sexta')
    attempt.update({'fim': now(), 'botaoHabilitadoDepois': browser.find_element(By.CSS_SELECTOR, inc_selector).is_enabled(), 'calculosAntes': five['calculosCapturados'], 'calculosDepois': after['calculosCapturados'], 'intervaloObservacaoSegundos': 1})
    save(root / 'tentativa-sexta-unidade.json', attempt)
    check('Quantidade após tentar sexta unidade', 'Continuar com cinco unidades de P008', {'itens': after['itens'], 'quantidadeVisivel': after['quantidade']}, after['itens'] == [{'produtoId': 'P008', 'quantidade': 5}] and after['quantidade'] == '5')
    check('Subtotal após tentar sexta unidade', 'Continuar em R$ 250,00', after['valores'].get('subtotal'), bool(re.fullmatch(r'R\$\s*250,00', after['valores'].get('subtotal', ''))))
    check('Botão de aumento bloqueado no limite', True, after['aumentarQuantidade'], attempt['botaoHabilitadoAntes'] is False and after['aumentarQuantidade']['disabled'] is True)
    check('Aviso do limite exibido', 'Limite de 5 unidades por produto.', after['avisoLimite'], after['avisoLimite'] == 'Limite de 5 unidades por produto.')
    network = js('return window.__qaRede')
    save(root / 'rede-navegador.json', network)
    save(root / 'erros-pagina.json', js('return window.__qaErros'))
    calcs = [r for r in network if r['url'].endswith('/api/carrinho/calcular')]
    for q, slug in [(4, 'calculo-quatro-unidades'), (5, 'calculo-cinco-unidades')]:
        captured = next(r for r in reversed(calcs) if any(i['produtoId'] == 'P008' and i['quantidade'] == q for i in json.loads(r['corpoEnviado'])['itens']))
        folder = root / slug
        folder.mkdir()
        save(folder / 'resposta-http.json', captured)
        (folder / 'corpo-enviado.json').write_text(captured['corpoEnviado'] + '\n')
        (folder / 'corpo-recebido.json').write_text(captured['corpoRecebido'] + '\n')
        if q == 5:
            check('Cálculo da quinta unidade aceito pela loja', 200, captured['status'], captured['status'] == 200)
            data = json.loads(captured['corpoRecebido'])
            check('Subtotal da quinta unidade retornado à interface', 250, data.get('subtotal'), type(data.get('subtotal')) in (int, float) and data['subtotal'] == 250)
    requests_for_six = [r for r in calcs if any(i['produtoId'] == 'P008' and i['quantidade'] > 5 for i in json.loads(r['corpoEnviado'])['itens'])]
    check('Tentativa bloqueada sem enviar sexta unidade', 'Nenhuma chamada com quantidade acima de cinco e nenhuma chamada adicional após a tentativa', {'chamadasAcimaDoLimite': len(requests_for_six), 'antes': five['calculosCapturados'], 'depois': after['calculosCapturados']}, not requests_for_six and five['calculosCapturados'] == after['calculosCapturados'])
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
    print(json.dumps({'evidencias': str(root), 'resultado': result['resultado'], 'inicio': result['inicio'], 'fim': result['fim'], 'erro': result.get('erro'), 'falhas': [c for c in checks if c['resultado'] != 'Aprovado']}, ensure_ascii=False), flush=True)
    if browser:
        try:
            browser.delete_session()
        finally:
            browser.cleanup()
sys.exit(0 if result['resultado'] == 'Aprovado' else 1)
