import sys, json, importlib; sys.path.insert(0, '/tmp/claude-0/outils')
from commun import *
from PIL import Image
import problemes_data; importlib.reload(problemes_data)
P = problemes_data.P
REF = json.load(open(f'{DON}/references.json'))
def refs(q):
    return [r for r in REF if str(r['question']).startswith(f'{q}.')]
def taille(f):
    im = Image.open(f'{D}/images/{f}')
    return im.width if f.startswith('e14') else im.width // 2
out = []; w = out.append
w('<h1>Problèmes et recos</h1><p class="chapo">23 problèmes, du plus gênant au plus petit. Chacun : le symptôme, sa preuve, sa cause dans le code, qui le voit et combien de fois, deux ou trois options, le choix et pourquoi, la règle ou la convention qui le fonde, la spécification prête à coder et des critères d’acceptation vérifiables. Les captures sont affichées à leur taille CSS réelle.</p>')
w(table([dict(n=f'<a href="#p{p["id"]}">P{p["id"]}</a>', problème=e(p['titre']), gravité=f'<span class="pastille {"gene" if p["grav"] == "gêne" else "detail"}">{p["grav"]}</span>', effort=e(p['effort']), axe=e(p['axes']), **{'choix tranché': '⚠' if p['tranche'] and ('Gildas' in p['tranche'] or 'Va contre' in p['tranche']) else ''}) for p in P],
          ['n', 'problème', 'gravité', 'effort', 'axe', 'choix tranché'], raw=('n', 'problème', 'gravité')))
w('<p class="petit">« Gêne » : un visiteur ne peut pas faire ou lire quelque chose, ou une règle d’accessibilité échoue. « Détail » : se voit, ne bloque rien. ⚠ : la reco touche une décision de Gildas ou un texte ; elle attend son avis.</p>')
for p in P:
    h = f'<section class="probleme" id="p{p["id"]}"><h2>P{p["id"]} · {e(p["titre"])}</h2>'
    h += f'<div class="meta-p"><span class="pastille {"gene" if p["grav"] == "gêne" else "detail"}">{p["grav"]}</span><span class="pastille">effort : {e(p["effort"])}</span><span class="pastille">{e(p["axes"])}</span>'
    if p['proto']: h += f'<a class="pastille" href="prototypes/apres/{p["proto"].split("#")[0].split("?")[0]}.html{"?" + p["proto"].split("?")[1] if "?" in p["proto"] else ""}{"#" + p["proto"].split("#")[1] if "#" in p["proto"] else ""}">voir le prototype →</a>'
    h += '</div>'
    h += f'<h3>Symptôme</h3><p>{p["symptome"]}</p>'
    h += '<h3>Preuve</h3>'
    if p['preuves']:
        h += ''.join(f'<figure><a href="images/{f}"><img src="images/{f}" width="{taille(f)}" alt="{e(c)}" loading="lazy"></a><figcaption>{c}</figcaption></figure>' for f, c in p['preuves'])
    h += f'<p>{p["mesure"]}</p>'
    h += f'<h3>Cause dans le code</h3><p>{p["cause"]}</p>'
    h += f'<h3>Impact</h3><p>{p["impact"]}</p>'
    h += '<h3>Options</h3><div class="options">'
    for i, (n, pour, contre) in enumerate(p['options']):
        h += f'<div class="option{" choisie" if i == p["choix"] else ""}"><b>{e(n)}{" · retenue" if i == p["choix"] else ""}</b><ul><li>Pour : {pour}</li><li>Contre : {contre}</li></ul></div>'
    h += f'</div><h3>Choix</h3><p>{p["argument"]}</p>'
    h += '<h3>Règles et conventions</h3><ul>' + ''.join(f'<li>{r}</li>' for r in p['regles'])
    for q in p['refq']:
        for r in refs(q):
            cap = f' <a href="images/references/{e(r["capture"])}">capture</a>' if r.get('capture') else ''
            h += f'<li><b>{e(r["site"])}</b> ({e(r["largeur"])} px) : {e(r["observation"])}{cap}</li>'
    h += '</ul>'
    if p['tranche']: h += f'<h3>Ce qui a été tranché</h3><p>{p["tranche"]}</p>'
    def enc(x): return e(x).replace('&amp;amp;', '&amp;').replace('&amp;lt;', '&lt;').replace('&amp;gt;', '&gt;').replace('&amp;#', '&amp;#').replace('&lt;br&gt;', '<br>')
    def cod(x): return '—' if x == '—' else f'<code>{enc(x)}</code>'
    h += '<h3>Spécification</h3>' + table([dict(lieu=enc(a_), avant=cod(b_), après=cod(c_)) for a_, b_, c_ in p['spec']], ['lieu', 'avant', 'après'], raw=('lieu', 'avant', 'après'))
    h += '<h3>Critères d’acceptation</h3><ul class="criteres">' + ''.join(f'<li>{c}</li>' for c in p['criteres']) + '</ul>'
    h += '</section>'
    w(h)
w('<h2>Sources des conventions</h2><p>Observations faites le 8 novembre 2026 sur 13 sites (brew.sh, rustup.rs, tailscale.com, apple.com/fr, support.apple.com/fr-fr, raycast.com, linear.app, notion.com, culturedcode.com/things, obsidian.md…), avec Playwright : <a href="donnees/references.json">references.json</a> (50 observations, mesures comprises) et <a href="images/references/">images/references/</a>.</p>')
ecrire('problemes.html', page('problemes.html', 'Problèmes et recos', '23 problèmes du site de Callrecorder : preuve, cause, impact, options, choix, spécification et critères d’acceptation.', '\n'.join(out)))
