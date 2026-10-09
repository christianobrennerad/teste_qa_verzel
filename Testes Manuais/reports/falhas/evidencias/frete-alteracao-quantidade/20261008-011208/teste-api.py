from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import subprocess,json,sys

root=Path(sys.argv[1]);results=[]
for quantity,expected in [(1,{'subtotal':100,'desconto':10,'frete':19.9,'total':109.9,'freteGratis':False,'valorFaltanteFreteGratis':100}),(2,{'subtotal':200,'desconto':20,'frete':0,'total':180,'freteGratis':True,'valorFaltanteFreteGratis':0})]:
    folder=root/'api'/f'quantidade-{quantity}';folder.mkdir(parents=True)
    body=json.dumps({'itens':[{'produtoId':'P005','quantidade':quantity}],'cupom':'BEMVINDO10'},separators=(',',':'))
    (folder/'corpo-enviado.json').write_text(body)
    cmd=['curl','-i','-X','POST','https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular','-H','Content-Type: application/json','--data-binary',body,'--max-time','30','--silent','--show-error','--write-out','\nCURL_HTTP_STATUS:%{http_code}\n']
    start=datetime.now(ZoneInfo('America/Fortaleza')).isoformat(timespec='seconds');r=subprocess.run(cmd,capture_output=True)
    (folder/'resposta-http.txt').write_bytes(r.stdout);(folder/'curl-stderr.txt').write_bytes(r.stderr)
    response,sep,status=r.stdout.decode(errors='replace').rpartition('\nCURL_HTTP_STATUS:')
    raw=response.replace('\r\n','\n').rsplit('\n\n',1)[-1].strip() if sep else ''
    (folder/'corpo.json').write_text(raw+'\n')
    try:data=json.loads(raw)
    except ValueError:data={}
    checks=[]
    def check(name,want,found,ok):checks.append({'verificacao':name,'esperado':want,'encontrado':found,'resultado':'Aprovado' if ok else 'Falhou'})
    check('Status final da aplicação',200,status.strip(),r.returncode==0 and status.strip()=='200')
    for k,v in expected.items():check(k,v,data.get(k),type(data.get(k)) is type(v) and data.get(k)==v if isinstance(v,bool) else type(data.get(k)) in (int,float) and data.get(k)==v)
    coupon=data.get('cupom');check('Cupom aplicado','BEMVINDO10',coupon,isinstance(coupon,dict) and coupon.get('codigo')=='BEMVINDO10' and coupon.get('aplicado') is True)
    result={'data':start,'quantidade':quantity,'comando':cmd,'curl_exit_code':r.returncode,'resultado':'Bloqueado' if r.returncode else ('Aprovado' if all(c['resultado']=='Aprovado' for c in checks) else 'Falhou'),'verificacoes':checks}
    (folder/'validacao-api.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');results.append(result)
    print(json.dumps({'quantidade':quantity,'resultado':result['resultado'],'encontrado':data},ensure_ascii=False))
(root/'resumo-api.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
sys.exit(1 if any(r['resultado']!='Aprovado' for r in results) else 0)
