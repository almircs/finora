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

# ---------- versão para iPad (app web instalável) ----------
import shutil, json
from PIL import Image
pwa = root / 'pwa'; pwa.mkdir(exist_ok=True)
head_extra = (
  '<link rel="manifest" href="manifest.webmanifest">\n'
  '<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">\n'
  '<meta name="apple-mobile-web-app-capable" content="yes">\n'
  '<meta name="mobile-web-app-capable" content="yes">\n'
  '<meta name="apple-mobile-web-app-title" content="Finora">\n'
  '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">\n'
  '<meta name="theme-color" content="#0F2A44">\n'
  '<script>window.FINORA_PWA=true;if("serviceWorker" in navigator)addEventListener("load",()=>navigator.serviceWorker.register("sw.js").catch(()=>{}));</script>')
(pwa / 'index.html').write_text(src.replace('<!--CSP-->', head_extra), encoding='utf-8')
sqljs = root / 'desktop' / 'node_modules' / 'sql.js' / 'dist' / 'sql-asm.js'
shutil.copy(sqljs, pwa / 'sql-asm.js')
(pwa / 'icons').mkdir(exist_ok=True)
full = Image.open(root / 'assets' / 'icon-full-1024.png').convert('RGBA')
def flat(sz, pad=0.0):
    bg = Image.new('RGBA', (sz, sz), (15, 42, 68, 255))
    inner = int(sz * (1 - 2 * pad)); im = full.resize((inner, inner), Image.LANCZOS)
    bg.alpha_composite(im, ((sz - inner) // 2, (sz - inner) // 2)); return bg.convert('RGB')
flat(180).save(pwa / 'icons' / 'apple-touch-icon.png')
flat(192).save(pwa / 'icons' / 'icon-192.png')
flat(512).save(pwa / 'icons' / 'icon-512.png')
flat(512, 0.1).save(pwa / 'icons' / 'maskable-512.png')
(pwa / 'manifest.webmanifest').write_text(json.dumps({
  'name': 'Finora', 'short_name': 'Finora', 'lang': 'pt-BR', 'start_url': './', 'scope': './',
  'display': 'standalone', 'orientation': 'any', 'background_color': '#EEF2F5', 'theme_color': '#0F2A44',
  'description': 'Controle de receitas e despesas, compatível com o Gastos Diários.',
  'icons': [{'src': 'icons/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
            {'src': 'icons/icon-512.png', 'sizes': '512x512', 'type': 'image/png'},
            {'src': 'icons/maskable-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'}]},
  ensure_ascii=False, indent=1), encoding='utf-8')
import hashlib
ver = hashlib.sha1((pwa / 'index.html').read_bytes()).hexdigest()[:10]
(pwa / 'sw.js').write_text(f"""const CACHE='finora-{ver}';
const FILES=['./','index.html','sql-asm.js','manifest.webmanifest','icons/apple-touch-icon.png','icons/icon-192.png','icons/icon-512.png'];
self.addEventListener('install',e=>{{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES)).then(()=>self.skipWaiting()));}});
self.addEventListener('activate',e=>{{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));}});
self.addEventListener('fetch',e=>{{const u=new URL(e.request.url);if(e.request.method!=='GET') return;
  if(u.origin!==location.origin){{e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request).then(res=>{{const cp=res.clone();caches.open(CACHE).then(c=>c.put(e.request,cp));return res;}}).catch(()=>r)));return;}}
  e.respondWith(fetch(e.request).then(res=>{{const cp=res.clone();caches.open(CACHE).then(c=>c.put(e.request,cp));return res;}}).catch(()=>caches.match(e.request,{{ignoreSearch:true}}).then(r=>r||caches.match('index.html'))));}});
""", encoding='utf-8')
print('pwa ok', ver)
