"""Pièces communes des pages du dossier : gabarit, navigation, tableaux tirés des CSV."""
import csv, html, json, os

DOSSIER = "design/recos/ux-android"
DONNEES = f"{DOSSIER}/donnees"

PAGES = [
    ("index.html", "Synthèse"),
    ("inventaire.html", "Inventaire"),
    ("mesures.html", "Mesures"),
    ("problemes.html", "Problèmes et recos"),
    ("prototypes.html", "Prototypes"),
    ("systeme.html", "Système et migration"),
    ("plan.html", "Plan"),
    ("references.html", "Références"),
]

def e(s): return html.escape(str(s), quote=True)

def lire(nom): return list(csv.DictReader(open(f"{DONNEES}/{nom}", encoding="utf-8")))
def json_(nom): return json.load(open(f"{DONNEES}/{nom}", encoding="utf-8"))

def tableau(entetes, rangs, classe="", brut=False, legende=None):
    """rangs : listes de cellules ; brut=True : cellules déjà en HTML."""
    out = [f'<div class="tw"><table class="{classe}">']
    if legende: out.append(f"<caption>{legende}</caption>")
    out.append("<thead><tr>" + "".join(f"<th>{e(h)}</th>" for h in entetes) + "</tr></thead><tbody>")
    for r in rangs:
        out.append("<tr>" + "".join(f"<td>{c if brut else e(c)}</td>" for c in r) + "</tr>")
    out.append("</tbody></table></div>")
    return "\n".join(out)

def code_lien(fichier, ligne):
    f = fichier.split("/")[-1]
    return f"<code>{e(f)}:{e(ligne)}</code>"

def page(nom, titre, corps, description=""):
    nav = "".join(f'<a href="{p}"{" aria-current=\"page\"" if p == nom else ""}>{e(t)}</a>' for p, t in PAGES)
    doc = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titre)}</title>
<meta name="description" content="{e(description)}">
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="haut"><div class="haut-in"><span class="marque">UX Android · Callrecorder</span><nav>{nav}</nav></div></header>
<main>
{corps}
</main>
<footer>Dossier de relecture UX de l'app Android, branche <code>recos-ux-android</code>, 8 novembre 2026. Aucun code de l'app modifié.
Données brutes dans <a href="donnees/">donnees/</a>, outils de mesure dans <a href="outils/">outils/</a>.</footer>
</body>
</html>
"""
    open(f"{DOSSIER}/{nom}", "w", encoding="utf-8").write(doc)

CSS = r"""
:root{
  --bg:#f4f4f2; --card:#ffffff; --text:#1d1d1f; --sec:#5b5b60; --ter:#7a7a80; --line:rgba(0,0,0,.12); --mass:rgba(0,0,0,.05); --chip:rgba(0,0,0,.07);
  --accent:#0064d2; --warn:#a0470a; --bad:#b3261e; --good:#146c2e; --hl:#fff3c4;
  --bad-bg:rgba(179,38,30,.10); --good-bg:rgba(20,108,46,.10); --warn-bg:rgba(160,71,10,.10);
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){
  --bg:#141414; --card:#1f1f20; --text:#f2f2f4; --sec:#b4b4ba; --ter:#8e8e94; --line:rgba(255,255,255,.14); --mass:rgba(255,255,255,.06); --chip:rgba(255,255,255,.09);
  --accent:#5aa9ff; --warn:#ffb35c; --bad:#ff8a80; --good:#7bd88f; --hl:#4a3f12;
  --bad-bg:rgba(255,138,128,.14); --good-bg:rgba(123,216,143,.13); --warn-bg:rgba(255,179,92,.13);
}}
:root[data-theme="dark"]{
  --bg:#141414; --card:#1f1f20; --text:#f2f2f4; --sec:#b4b4ba; --ter:#8e8e94; --line:rgba(255,255,255,.14); --mass:rgba(255,255,255,.06); --chip:rgba(255,255,255,.09);
  --accent:#5aa9ff; --warn:#ffb35c; --bad:#ff8a80; --good:#7bd88f; --hl:#4a3f12;
  --bad-bg:rgba(255,138,128,.14); --good-bg:rgba(123,216,143,.13); --warn-bg:rgba(255,179,92,.13);
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--text);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
a{color:var(--accent)}
.haut{position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.haut-in{max-width:1180px;margin:0 auto;padding:8px 16px;display:flex;flex-wrap:wrap;gap:6px 16px;align-items:center}
.marque{font-weight:600;font-size:14px}
nav{display:flex;flex-wrap:wrap;gap:2px}
nav a{font-size:14px;text-decoration:none;color:var(--sec);padding:4px 9px;border-radius:99px}
nav a[aria-current]{background:var(--chip);color:var(--text)}
main{max-width:1180px;margin:0 auto;padding:28px 16px 60px}
footer{max-width:1180px;margin:0 auto;padding:0 16px 40px;color:var(--sec);font-size:14px}
h1{font-size:30px;line-height:1.2;margin:0 0 14px;font-weight:650;letter-spacing:-.01em}
h2{font-size:22px;line-height:1.3;margin:36px 0 10px;font-weight:620}
h3{font-size:18px;line-height:1.35;margin:24px 0 8px;font-weight:600}
h4{font-size:15px;margin:16px 0 6px;font-weight:600}
p,ul,ol{margin:0 0 12px}
li{margin:2px 0}
.lead{font-size:18px;color:var(--sec);max-width:820px}
.card{background:var(--card);border-radius:12px;padding:18px 20px;margin:0 0 16px}
.grid{display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(210px,1fr))}
.chiffre{background:var(--card);border-radius:12px;padding:14px 16px}
.chiffre b{display:block;font-size:30px;line-height:1.1;font-weight:650;font-variant-numeric:tabular-nums}
.chiffre span{color:var(--sec);font-size:14px}
td:has(.sw){white-space:nowrap}
code{font:13px/1.4 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;background:var(--mass);padding:1px 5px;border-radius:5px;overflow-wrap:anywhere}
pre{font:12.5px/1.5 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;background:var(--mass);padding:12px 14px;border-radius:8px;overflow:auto;margin:0 0 12px}
pre .del{background:var(--bad-bg);display:block}
pre .add{background:var(--good-bg);display:block}
.tw{overflow-x:auto;margin:0 0 16px;border-radius:10px;background:var(--card)}
table{border-collapse:collapse;width:100%;font-size:14px;font-variant-numeric:tabular-nums}
caption{text-align:left;color:var(--sec);font-size:13px;padding:8px 12px 0}
th,td{text-align:left;padding:7px 12px;vertical-align:top;border-bottom:1px solid var(--line)}
th{font-weight:600;color:var(--sec);font-size:13px;white-space:nowrap;position:sticky;top:0;background:var(--card)}
tr:last-child td{border-bottom:0}
td.num,th.num{text-align:right}
.ok{color:var(--good);font-weight:600}.ko{color:var(--bad);font-weight:600}.av{color:var(--warn);font-weight:600}
.tag{display:inline-block;font-size:12.5px;padding:1px 9px;border-radius:99px;background:var(--chip);color:var(--sec);margin:0 4px 4px 0;white-space:nowrap}
.tag.g{background:var(--bad-bg);color:var(--bad)}.tag.d{background:var(--chip)}.tag.c{background:color-mix(in srgb,var(--accent) 14%,transparent);color:var(--accent)}
.sw{display:inline-block;width:14px;height:14px;border-radius:4px;vertical-align:-2px;margin-right:6px;box-shadow:inset 0 0 0 1px var(--line)}
.pb{overflow-wrap:anywhere;background:var(--card);border-radius:14px;padding:20px 22px;margin:0 0 22px;scroll-margin-top:70px}
.pb>h2{margin-top:0}
.pb dl{display:grid;grid-template-columns:max-content minmax(0,1fr);gap:6px 16px;margin:0 0 12px}
.pb dt{color:var(--sec);font-size:14px;font-weight:600;padding-top:2px}
.pb dd{margin:0;min-width:0}
.opts{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));margin:6px 0 12px}
.opt{background:var(--mass);border-radius:10px;padding:10px 12px;font-size:14.5px}
.opt.choisi{box-shadow:inset 0 0 0 2px var(--good)}
.opt h5{margin:0 0 4px;font-size:14.5px}
.opt ul{padding-left:18px;margin:0}
.preuves{display:flex;flex-wrap:wrap;gap:14px;margin:8px 0 12px}
.preuves figure{margin:0;max-width:330px}
.preuves img{display:block;max-width:100%;height:auto;border-radius:10px;box-shadow:0 0 0 1px var(--line)}
.preuves figcaption{font-size:13px;color:var(--sec);margin-top:4px;max-width:330px}
.crit{list-style:none;padding:0}
.crit li{padding-left:24px;position:relative}
.crit li::before{content:"☐";position:absolute;left:2px;color:var(--sec)}
.note{border-left:3px solid var(--line);padding:2px 0 2px 12px;color:var(--sec);font-size:14.5px}
.note.choix{border-color:var(--accent)}
.etats{display:grid;gap:14px;grid-template-columns:repeat(auto-fill,minmax(150px,1fr))}
.etats figure{margin:0;font-size:12.5px;color:var(--sec)}
.etats img{width:100%;height:auto;border-radius:8px;box-shadow:0 0 0 1px var(--line);display:block;margin-bottom:4px}
.toc{columns:2 300px;padding-left:20px}
details{background:var(--card);border-radius:10px;padding:10px 14px;margin:0 0 12px}
details summary{cursor:pointer;font-weight:600}
@media (max-width:640px){ h1{font-size:25px} .pb dl{grid-template-columns:1fr} .pb dt{padding-top:8px} th{position:static} }
"""

def css():
    open(f"{DOSSIER}/style.css", "w", encoding="utf-8").write(CSS)
