# Fabrique les prototypes : chaque page du site au commit 953f6d3 (avant), et la même corrigée (après).
# python3 prototypes.py <site> <dossier prototypes>
import re, sys, os, html
SITE, P = sys.argv[1], sys.argv[2]
LIVE = 'https://gildasfremont.github.io/callrecorder/'
PAGES = {'accueil': 'index.html', 'fonctionnalites': 'fonctionnalites/index.html', 'guides': 'guides/index.html', 'versions': 'versions/index.html', 'confidentialite': 'confidentialite/index.html'}

def links(h, page):
    pre = '' if page == 'accueil' else '../'
    # assets : les images restent celles du site en ligne
    h = re.sub(r'(src|href)="(?:\.\./)?(img/[^"]+)"', lambda m: f'{m.group(1)}="{LIVE}{m.group(2)}"', h)
    h = re.sub(r'<link rel="stylesheet" href="(?:\.\./)?style\.css[^"]*">', '<link rel="stylesheet" href="../css/site-953f6d3.css">', h)
    h = re.sub(r'<script src="(?:\.\./)?nav\.js[^"]*"></script>', '<script src="../js/nav.js"></script>', h)
    h = re.sub(r'<script src="(?:\.\./)?note\.js[^"]*"></script>', '<script src="../js/note.js"></script>', h)
    h = re.sub(r'<script src="(?:\.\./)?visite\.js[^"]*"></script>\n?', '', h)
    # liens entre pages : vers la page sœur du prototype
    def lk(m):
        u = m.group(1)
        base, _, frag = u.partition('#')
        base = base.replace('../', '').strip('./')
        target = {'': 'accueil', 'index.html': 'accueil'}.get(base, base.strip('/'))
        if target in PAGES: return f'href="{target}.html' + (('#' + frag) if frag else '') + '"'
        return m.group(0)
    h = re.sub(r'href="((?:\.\./|\./)?(?:fonctionnalites|guides|versions|confidentialite)?/?(?:#[^"]*)?)"', lambda m: lk(m) if not m.group(1).startswith('#') else m.group(0), h)
    h = h.replace('href="../"', 'href="accueil.html"').replace('href="./"', 'href="accueil.html"')
    return h

# ——— Transformations de l'après ———
TEXT_SKIP = ('script', 'style', 'code', 'kbd', 'pre', 'textarea')
def on_text(h, fn):
    out, i, skip = [], 0, []
    for m in re.finditer(r'<[^>]+>', h):
        t = h[i:m.start()]
        out.append(t if skip else fn(t))
        tag = m.group(0); out.append(tag)
        n = re.match(r'</?(\w+)', tag)
        if n and n.group(1).lower() in TEXT_SKIP:
            if tag.startswith('</'): skip and skip.pop()
            elif not tag.endswith('/>'): skip.append(1)
        i = m.end()
    t = h[i:]; out.append(t if skip else fn(t))
    return ''.join(out)

NB, FINE = '&nbsp;', '&#8239;'
def typo(t):  # P11
    t = re.sub(r"(?<=[A-Za-zÀ-ÿ])'(?=[A-Za-zÀ-ÿ])", '’', t)
    t = re.sub(r'(?<=\S) :(?=\s|$)', NB + ':', t)
    t = re.sub(r'(?<=\S) ([;?!])', NB + r'\1', t)  # U+00A0, comme Apple et Notion (references.json, question 9)
    t = re.sub(r'«(?: | )', '«' + NB, t); t = re.sub(r'(?: | )»', NB + '»', t)
    t = re.sub(r'(\d) (min|Go|Mo|ko|h|jours|s)\b', r'\1' + NB + r'\2', t)
    t = re.sub(r'(\d) %', r'\1' + FINE + '%', t)
    return t

PATHS = ['Réglages Système › Confidentialité et sécurité › Accessibilité', 'Réglages › Général › Dossier des appels › Changer…', 'Réglages › Outils et intégrations › Autres outils',
         'Réglages › Paramètres › Rechercher une mise à jour', 'Réglages › Paramètres › Reconnaître ma voix', 'Réglages › Intégrations › Base de données externe',
         'Réglages › Intégrations › Vocaux WhatsApp', 'Réglages › Enregistrements › Espace occupé', 'Réglages › Enregistrements › Récemment supprimés',
         'Réglages › Enregistrements › Vocaux WhatsApp', 'Réglages › Intégrations › Agents', 'Réglages › Téléphones › Ajouter un téléphone', 'Google Drive › Mon Drive › CallRecordings',
         'Fichier › Exporter la transcription', 'menu ⋯ › Ajouter un sous-titre', 'Paramètres › Apps et sites', 'Paramètres › Enregistrement', 'Intégrations › Agents',
         'Réglages › Paramètres', 'Réglages › Général', 'Réglages › Groupes', 'Réglages › Téléphones', 'Réglages › Intégrations']
def chemin_html(p):
    steps = p.split(' › ')
    return '<span class="chemin">' + ' '.join(f'<span>{s}{NB}›</span>' if i < len(steps) - 1 else f'<span>{s}</span>' for i, s in enumerate(steps)) + '</span>'
def chemins(t):  # P12
    t = t.replace('&nbsp;›&nbsp;', ' › ')
    for p in PATHS:
        t = re.sub(r'(?<![\w>])' + re.escape(p) + r'(?![\w])', lambda m: '\x00' + str(PATHS.index(p)) + '\x01', t)
    return re.sub(r'\x00(\d+)\x01', lambda m: chemin_html(PATHS[int(m.group(1))]), t)

from PIL import Image
def demi(h):
    # P1, P3 : chaque capture à sa taille réelle (la moitié de ses pixels), plafonnée par sa colonne.
    def one(m):
        tag = m.group(0); src = re.search(r'src="([^"]+)"', tag).group(1)
        path = src.replace(LIVE, SITE + '/').split('?')[0] if src.startswith(LIVE) else os.path.join(P, 'apres', src)
        path = os.path.normpath(path)
        if not os.path.exists(path) or 'gildas.webp' in src: return tag
        w = Image.open(path).width // 2
        tag = re.sub(r'\sstyle="[^"]*"', '', tag)
        return tag.replace('<img', f'<img style="--l:{w}px"', 1)
    return re.sub(r'<img[^>]+>', one, h)

def apres(h, page):
    h = h.replace('<link rel="stylesheet" href="../css/site-953f6d3.css">', '<link rel="stylesheet" href="../css/site-953f6d3.css">\n<link rel="stylesheet" href="../css/apres.css">')
    # P9 : un repère principal
    h = re.sub(r'(</nav>\n)', r'\1<main>\n', h, count=1)
    h = h.replace('\n  <footer>', '\n  </main>\n  <footer>', 1)
    if page == 'accueil':  # la section de l'installation se ferme avant le pied
        h = h.replace('\n  </main>\n  <footer>', '\n  </section>\n  </main>\n  <footer>', 1)
        # P21
        h = h.replace('<h1>Souvenez-vous de tout</h1>', '<h1>Souvenez<span class="union">-</span>vous de tout</h1>')
        # P2 : la ligne entière, une coupure permise après chaque « / »
        h = re.sub(r'(<code id="cmd">)(.*?)(</code>)', lambda m: m.group(1) + m.group(2).replace('/', '/<wbr>').replace('https:/<wbr>/<wbr>', 'https://').replace(' | ', NB + '|' + NB) + m.group(3), h)
        # P15 : la source sans point médian
        h = re.sub(r'<span class="sub">· ', '<span class="sub">', h)
        # P10 : la carte iPhone rejoint les cassettes ; l'ordinateur passe à droite pour garder l'alternance
        h = re.sub(r'\s*<li id="telephones" class="o-telephones">.*?</li>', '', h, flags=re.S)
        h = h.replace("et transcrit dès qu'il se termine.</p>", "et transcrit dès qu'il se termine. Rien à installer sur l'iPhone.</p>")
        h = h.replace('<li class="o-ordinateur">', '<li id="telephones" class="o-ordinateur text-right">')
        h = h.replace('<li class="o-telephone text-right">', '<li class="o-telephone">')
        # P5 : chaque icône se focalise et dit son nom au toucher
        h = h.replace('<span class="app tile', '<span tabindex="0" class="app tile').replace('<span class="app"', '<span tabindex="0" class="app"')
    if page == 'fonctionnalites':
        for src, w in [('appels-reunion', 590), ('appels-note', 650), ('calendrier', 360), ('transcription', 665)]:
            h = re.sub(r'<img([^>]*?) src="' + re.escape(LIVE) + r'img/' + src + r'\.webp[^"]*"([^>]*?)>',
                       lambda m: f'<img src="../img/{src}-extrait.webp" width="{w}" class="extrait-coupe"' + re.sub(r'\s(width|height|class)="[^"]*"', '', m.group(1) + m.group(2)) + '>', h)
        h = h.replace('<header class="page-head">', '<header class="page-head avec-sommaire">', 1)
        h = demi(h)
    if page == 'versions':
        crops = {'0.11.0': 1380, '0.13.0': 1140, '0.15.0': 1300, '0.19.0': 1390, '0.6.0': 1400, '0.7.0': 1400, '0.7.1': 1400, '0.4.0': 1400, '0.5.0': 1360, '0.5.5': 1400}
        nat = {'0.24.0': (600, 757), '0.23.0': (1360, 418), '0.22.0': (288, 80), '0.21.0': (1360, 288), '0.20.0': (1360, 322), '0.16.0': (990, 620), '0.14.2': (1373, 593), '0.14.0': (1360, 847), '0.12.0': (1370, 1194), '0.10.1': (1370, 235), '0.10.0': (1360, 591), '0.9.0': (915, 384), '0.8.0': (1360, 382)}
        def img(m):
            tag, v = m.group(0), m.group(1)
            if v in crops:
                tag = tag.replace(f'{LIVE}img/versions/{v}.webp', f'../img/versions/{v}-extrait.webp')
                w = crops[v] // 2
            elif v in nat: w = nat[v][0] // 2
            else: return tag
            tag = re.sub(r'\s(width|height)="[^"]*"', '', tag)
            return tag.replace('<img', f'<img width="{w}"', 1)
        h = re.sub(r'<img[^>]*img/versions/([\d.]+)\.webp[^>]*>', img, h)
        h = demi(h)
    if page == 'confidentialite':
        sec = h[h.index('<section class="legal">'):h.index('</section>', h.index('<section class="legal">'))]
        ps = re.findall(r'      <p>.*?</p>\n', sec, flags=re.S)
        groups = [('Ce qui reste sur votre Mac', [0, 1]), ('Ce qui en sort, si vous le décidez', [2, 3, 6]), ('Ce qui en sort d’office, et comment le couper', [4, 5, 7]), ('Ce site', [8, 9, 10])]
        body = ''.join(f'      <div class="masse"><h2>{t}</h2>\n' + ''.join(ps[i] for i in idx) + '      </div>\n' for t, idx in groups)
        body += ps[11].replace('<p>', '<p class="fin">', 1)
        h = h.replace(''.join(ps), body)
    h = on_text(h, lambda t: chemins(typo(t)))
    # le thème du prototype : ?theme=sombre (option)
    h = h.replace('</head>', '<script>if (/theme=sombre/.test(location.search)) document.documentElement.dataset.theme = "sombre";</script>\n</head>', 1)
    h = h.replace('<meta name="color-scheme" content="light only">', '<meta name="color-scheme" content="light dark">')
    return h

for page, f in PAGES.items():
    h = links(open(os.path.join(SITE, f), encoding='utf-8').read(), page)
    marque = '<!-- Prototype : copie du site gildasfremont/callrecorder au commit 953f6d3. -->\n'
    open(f'{P}/avant/{page}.html', 'w').write(h.replace('<!doctype html>', '<!doctype html>\n' + marque, 1))
    open(f'{P}/apres/{page}.html', 'w').write(apres(h, page).replace('<!doctype html>', '<!doctype html>\n' + marque.replace('Copie', 'Après').replace('copie', 'après, à partir'), 1))
    print(page, 'ok')
