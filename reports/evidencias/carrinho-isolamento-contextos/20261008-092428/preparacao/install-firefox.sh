#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from pathlib import Path
import subprocess,os
root=Path('/tmp/verzel-firefox-apt')
for name in ['empty','lists/partial','archives/partial']:(root/name).mkdir(parents=True,exist_ok=True)
(root/'sources.list').write_text('deb [signed-by=/usr/share/keyrings/debian-archive-keyring.gpg] https://deb.debian.org/debian trixie main\ndeb [signed-by=/usr/share/keyrings/debian-archive-keyring.gpg] https://security.debian.org/debian-security trixie-security main\n')
(root/'apt.conf').write_text('Dir::Etc::parts "/tmp/verzel-firefox-apt/empty";\nDir::Etc::main "/dev/null";\nDir::Etc::sourcelist "/tmp/verzel-firefox-apt/sources.list";\nDir::Etc::sourceparts "-";\nDir::State::lists "/tmp/verzel-firefox-apt/lists";\nDir::Cache::archives "/tmp/verzel-firefox-apt/archives";\nDir::State::status "/var/lib/dpkg/status";\nDebug::NoLocking "true";\n')
env=os.environ.copy();env['APT_CONFIG']=str(root/'apt.conf')
if env.get('HTTPS_PROXY'):env['https_proxy']=env['HTTPS_PROXY']
for cmd in [['/usr/bin/apt-get','update'],['/usr/bin/apt-get','--download-only','--no-install-recommends','-y','install','firefox-esr']]:subprocess.run(cmd,env=env,check=True)
packages=list((root/'archives').glob('firefox-esr_*.deb'))
assert packages,'Pacote Firefox não encontrado'
# Atualiza apenas a extração local; os pacotes são autenticados pelo APT.
package=max(packages,key=lambda p:p.stat().st_mtime)
subprocess.run(['dpkg-deb','-x',str(package),'/tmp/verzel-firefox-debian'],check=True)
PY
python3 -m pip install --target /tmp/verzel-marionette --upgrade 'marionette_driver==3.7.1'
/tmp/verzel-firefox-debian/usr/lib/firefox-esr/firefox-esr --version
