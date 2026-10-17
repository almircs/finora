"""Gera as duas versões do Finora a partir de finora.src.html:
- desktop/app/index.html  (programa Electron, com política de segurança e leitor SQLite local)
- web/finora.html         (página publicada no claude.ai, sem o envelope <html>/<head>/<body>)
"""
import re, pathlib

root = pathlib.Path(__file__).parent
src = (root / 'finora.src.html').read_text(encoding='utf-8')
import base64
logo = 'data:image/png;base64,' + base64.b64encode((root / 'assets' / 'logo.png').read_bytes()).decode()
src = src.replace('%%LOGO%%', logo)

csp = ('<meta http-equiv="Content-Security-Policy" content="default-src \'self\'; '
       'script-src \'self\' \'unsafe-inline\'; style-src \'self\' \'unsafe-inline\' https://fonts.googleapis.com; '
       'font-src \'self\' data: https://fonts.gstatic.com; img-src \'self\' data:; connect-src \'none\'">')
desktop = src.replace('<!--CSP-->', csp)
(root / 'desktop' / 'app').mkdir(parents=True, exist_ok=True)
(root / 'desktop' / 'app' / 'index.html').write_text(desktop, encoding='utf-8')

head = re.search(r'<head>(.*?)</head>', src, re.S).group(1)
body = re.search(r'<body>(.*?)</body>', src, re.S).group(1)
head = re.sub(r'<meta charset[^>]*>\s*|<meta name="viewport"[^>]*>\s*|<!--CSP-->\s*', '', head)
web = head.strip() + '\n' + body.strip() + '\n'
(root / 'web').mkdir(exist_ok=True)
(root / 'web' / 'finora.html').write_text(web, encoding='utf-8')
print('desktop', len(desktop), 'web', len(web))
