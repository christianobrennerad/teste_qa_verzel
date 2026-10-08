from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import subprocess,json,sys
root=Path(sys.argv[1])
for phase in ['01-cupom-aplicado','02-cupom-removido','03-cupom-expirado']:
 folder=root/'api'/phase;folder.mkdir(parents=True)
 body=(root/'interface'/phase/'corpo-enviado.json').read_text();(folder/'corpo-enviado.json').write_text(body)
 cmd=['curl','-i','-X','POST','https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular','-H','Content-Type: application/json','--data-binary',body,'--max-time','30','--silent','--show-error','--write-out','\nCURL_HTTP_STATUS:%{http_code}\n']
 start=datetime.now(ZoneInfo('America/Fortaleza')).isoformat(timespec='seconds');r=subprocess.run(cmd,capture_output=True)
 (folder/'resposta-http.txt').write_bytes(r.stdout);(folder/'curl-stderr.txt').write_bytes(r.stderr)
 response,sep,status=r.stdout.decode(errors='replace').rpartition('\nCURL_HTTP_STATUS:');received=response.replace('\r\n','\n').rsplit('\n\n',1)[-1].strip() if sep else ''
 (folder/'corpo.json').write_text(received+'\n')
 try:data=json.loads(received)
 except ValueError:data={}
 expected=json.loads((root/'interface'/phase/'corpo-recebido.json').read_text())
 ok=r.returncode==0 and status.strip()=='200' and data==expected
 meta={'data':start,'comando':cmd,'curl_exit_code':r.returncode,'status':status.strip(),'resultado':'Aprovado' if ok else ('Bloqueado' if r.returncode else 'Falhou'),'verificacao':'Resposta coincide com os dados recebidos durante esta etapa da interface','encontrado':data}
 (folder/'validacao-api.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
 print(phase,meta['resultado'],status.strip())
