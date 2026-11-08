"""Pièces communes du dossier : style, gabarit de page, lecture des données, calculs de contraste."""
import csv, json, html, os, collections

ROOT = '/home/user/callrecorder-app/design/recos/graphisme-android'
D = ROOT + '/donnees'

def esc(s): return html.escape(str(s), quote=True)

def rows(name):
    with open(f'{D}/{name}.csv', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def short(path):
    return path.replace('phone/android/app/src/main/java/fyi/gildas/callrecorder/', '').replace('phone/android/app/src/main/', '')

GH = 'https://github.com/gildasfremont/callrecorder-app/blob/main/'
def src(path, line=None):
    """Un lien vers fichier:ligne (le chemin court affiché, le lien vers main)."""
    full = path if path.startswith('phone/') else 'phone/android/app/src/main/java/fyi/gildas/callrecorder/' + path
    lab = short(full) + (f':{line}' if line else '')
    return f'<a class="src" href="{GH}{full}{"#L" + str(line) if line else ""}">{esc(lab)}</a>'

# --- couleurs et contrastes (mêmes formules que donnees/outils/mesures.py)
def parse(h):
    h = h.lstrip('#')
    if len(h) == 6: h = 'FF' + h
    return (int(h[2:4], 16), int(h[4:6], 16), int(h[6:8], 16), int(h[0:2], 16) / 255)

def over(fg, bg):
    r, g, b, a = fg; R, G, B, _ = bg
    return (r * a + R * (1 - a), g * a + G * (1 - a), b * a + B * (1 - a), 1.0)

def lum(c):
    def lin(v):
        v /= 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * lin(c[0]) + 0.7152 * lin(c[1]) + 0.0722 * lin(c[2])

def wcag(fg, bg):
    a, b = lum(fg), lum(bg)
    return (max(a, b) + 0.05) / (min(a, b) + 0.05)

def apca(txt, bg):
    def Y(c): return sum(((v / 255) ** 2.4) * k for v, k in zip(c[:3], (0.2126729, 0.7151522, 0.0721750)))
    yt, yb = Y(txt), Y(bg)
    if yt < 0.022: yt += (0.022 - yt) ** 1.414
    if yb < 0.022: yb += (0.022 - yb) ** 1.414
    if abs(yb - yt) < 0.0005: return 0.0
    if yb > yt:
        s = (yb ** 0.56 - yt ** 0.57) * 1.14
        return 0 if s < 0.1 else (s - 0.027) * 100
    s = (yb ** 0.65 - yt ** 0.62) * 1.14
    return 0 if s > -0.1 else (s + 0.027) * 100

def hexc(c): return '#%02X%02X%02X' % tuple(round(v) for v in c[:3])

def ratio(fg, bg, page):
    """fg, bg, page en #AARRGGBB ; renvoie (texte composé, fond composé, WCAG, |Lc|)."""
    b = over(parse(bg), parse(page)) if bg else parse(page)
    f = over(parse(fg), b)
    return hexc(f), hexc(b), wcag(f, b), abs(apca(f, b))

def fr(x, n=2):
    return f'{x:.{n}f}'.replace('.', ',')

CSS = r"""
:root{
  --bg:#f4f5f7; --card:#fff; --sunk:#eceef1; --text:#1b1d21; --muted:#5a616d; --faint:#8a909a; --line:rgba(0,0,0,.09);
  --accent:#0b5cc4; --gene:#9a4206; --gene-bg:#fbeee3; --ok:#1d7a3a; --ok-bg:#e5f4ea; --ko:#b3261e; --ko-bg:#fbe9e7;
  --mark:#fff2b3;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#131416; --card:#1d1f22; --sunk:#26292d; --text:#eceef1; --muted:#a6acb6; --faint:#7d838d; --line:rgba(255,255,255,.1);
    --accent:#6aa8ff; --gene:#ffb06a; --gene-bg:#3a2513; --ok:#6fd38a; --ok-bg:#16301f; --ko:#ff8a80; --ko-bg:#3b1715; --mark:#5a4a00;
  }
}
:root[data-theme="dark"]{
  --bg:#131416; --card:#1d1f22; --sunk:#26292d; --text:#eceef1; --muted:#a6acb6; --faint:#7d838d; --line:rgba(255,255,255,.1);
  --accent:#6aa8ff; --gene:#ffb06a; --gene-bg:#3a2513; --ok:#6fd38a; --ok-bg:#16301f; --ko:#ff8a80; --ko-bg:#3b1715; --mark:#5a4a00;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--text);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
a{color:var(--accent)} a.src{font:13px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace;white-space:nowrap}
.wrap{max-width:1120px;margin:0 auto;padding:24px 16px 80px}
nav.top{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--line)}
nav.top .in{max-width:1120px;margin:0 auto;padding:10px 16px;display:flex;gap:6px 16px;flex-wrap:wrap;align-items:baseline}
nav.top b{margin-right:8px}
nav.top a{text-decoration:none;font-size:15px;color:var(--muted)} nav.top a.on{color:var(--text);font-weight:600}
h1{font-size:32px;line-height:1.15;margin:12px 0 8px;font-weight:700;letter-spacing:-.01em}
h2{font-size:23px;line-height:1.25;margin:40px 0 10px;font-weight:650}
h3{font-size:18px;line-height:1.3;margin:24px 0 8px;font-weight:600}
p,li{max-width:76ch}
.lede{color:var(--muted);font-size:17px}
.card{background:var(--card);border-radius:14px;padding:18px 20px;margin:14px 0}
code{font:13px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace;background:var(--sunk);padding:1px 5px;border-radius:5px}
pre{font:12.5px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;background:var(--sunk);padding:12px 14px;border-radius:10px;overflow-x:auto;white-space:pre}
.tw{overflow-x:auto;margin:10px 0;border-radius:12px;background:var(--card)}
table{border-collapse:collapse;width:100%;font-size:14px}
th,td{text-align:left;padding:7px 10px;vertical-align:top}
th{font-weight:600;color:var(--muted);font-size:13px;background:var(--sunk);position:sticky;top:0}
tbody tr:nth-child(even){background:color-mix(in srgb,var(--sunk) 45%,transparent)}
td.n,th.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.ok{color:var(--ok);font-weight:600} .ko{color:var(--ko);font-weight:600}
.pill{display:inline-block;font-size:12.5px;padding:1px 8px;border-radius:999px;background:var(--sunk);color:var(--muted);white-space:nowrap}
.pill.gene{background:var(--gene-bg);color:var(--gene)} .pill.ko{background:var(--ko-bg);color:var(--ko)} .pill.ok{background:var(--ok-bg);color:var(--ok)}
.sw{display:inline-block;width:14px;height:14px;border-radius:4px;vertical-align:-2px;margin-right:6px;box-shadow:inset 0 0 0 1px rgba(127,127,127,.35)}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px} .grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.kpi{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:16px 0}
.kpi div{background:var(--card);border-radius:12px;padding:12px 14px} .kpi b{display:block;font-size:26px;font-variant-numeric:tabular-nums}
.kpi span{color:var(--muted);font-size:14px}
figure{margin:12px 0} figure img{max-width:100%;height:auto;border-radius:10px;display:block} figcaption{font-size:13px;color:var(--muted);margin-top:6px}
[id]{scroll-margin-top:60px}
.prob{background:var(--card);border-radius:16px;padding:20px 22px;margin:22px 0}
.prob h2{margin-top:0}
.prob dl{display:grid;grid-template-columns:170px 1fr;gap:8px 18px;margin:12px 0}
.prob dt{color:var(--muted);font-size:14px;padding-top:2px} .prob dd{margin:0;min-width:0}
td pre{white-space:pre-wrap;word-break:break-word;margin:0;padding:6px 8px;font-size:12px}
.opts{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px}
.opt{background:var(--sunk);border-radius:12px;padding:10px 12px;font-size:14.5px}
.opt.choisi{outline:2px solid var(--ok)}
.opt b{display:block;margin-bottom:4px}
.against{border-left:3px solid var(--gene);padding-left:10px}
.toc{columns:2;column-gap:28px} .toc li{break-inside:avoid;margin:2px 0}
details summary{cursor:pointer;color:var(--accent)}
.small{font-size:13.5px;color:var(--muted)}
@media (max-width:760px){
  .grid2,.grid3{grid-template-columns:1fr} .kpi{grid-template-columns:1fr 1fr} .toc{columns:1}
  .prob dl{grid-template-columns:1fr} .prob dt{padding-top:8px}
  h1{font-size:26px}
}
"""

PAGES = [('index.html', 'Synthèse'), ('inventaire.html', 'Inventaire'), ('mesures.html', 'Mesures'),
         ('problemes.html', 'Problèmes et recos'), ('prototypes.html', 'Prototypes'), ('systeme.html', 'Système et migration'),
         ('plan.html', 'Plan')]

def page(fname, title, body, extra_css=''):
    nav = ''.join(f'<a href="{f}"{" class=on" if f == fname else ""}>{t}</a>' for f, t in PAGES)
    doc = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<style>{CSS}{extra_css}</style>
</head>
<body>
<nav class="top"><div class="in"><b>Android · graphisme</b>{nav}</div></nav>
<div class="wrap">
{body}
</div>
</body>
</html>
"""
    open(f'{ROOT}/{fname}', 'w', encoding='utf-8').write(doc)

def table(headers, data, num=()):
    th = ''.join(f'<th{" class=n" if i in num else ""}>{h}</th>' for i, h in enumerate(headers))
    tr = ''.join('<tr>' + ''.join(f'<td{" class=n" if i in num else ""}>{c}</td>' for i, c in enumerate(r)) + '</tr>' for r in data)
    return f'<div class="tw"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'

def sw(hexcolor):
    return f'<span class="sw" style="background:{hexcolor}"></span>'
