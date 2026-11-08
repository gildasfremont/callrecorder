# Pièces communes aux pages du dossier.
import html, csv, json, os
D = '/home/user/callrecorder-app/design/recos/graphisme-site'
DON = D + '/donnees'
PAGES = [('index.html', 'Synthèse'), ('inventaire.html', 'Inventaire'), ('mesures.html', 'Mesures'), ('problemes.html', 'Problèmes et recos'),
         ('prototypes.html', 'Prototypes'), ('systeme.html', 'Système et migration'), ('plan.html', 'Plan')]
def e(s): return html.escape(str(s), quote=True)
def page(fichier, titre, description, corps):
    nav = ''.join(f'<a href="{f}"' + (' aria-current="page"' if f == fichier else '') + f'>{t}</a>' for f, t in PAGES)
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>{e(titre)}</title>
<meta name="description" content="{e(description)}">
<link rel="stylesheet" href="dossier.css">
</head>
<body>
<header class="tete"><b>Site · graphisme</b>{nav}</header>
<main>
{corps}
<p class="petit" style="margin-top:64px">Relevé du 8 novembre 2026 sur le site en ligne (<code>gildasfremont/callrecorder</code>, commit <code>953f6d3</code>). Données brutes dans <a href="donnees/">donnees/</a>, scripts dans <a href="donnees/scripts/">donnees/scripts/</a>.</p>
</main>
</body>
</html>
'''
def table(rows, cols, num=(), raw=(), classes=None):
    h = '<div class="tableau"><table><thead><tr>' + ''.join(f'<th class="{"n" if c in num else ""}">{e(c)}</th>' for c in cols) + '</tr></thead><tbody>'
    for r in rows:
        h += '<tr>' + ''.join(f'<td class="{"n" if c in num else ""}">' + (str(r.get(c, '')) if c in raw else e(r.get(c, ''))) + '</td>' for c in cols) + '</tr>'
    return h + '</tbody></table></div>'
def lire(n): return list(csv.DictReader(open(f'{DON}/{n}')))
def fr(x, d=2):
    if isinstance(x, (int,)) : return f'{x:,}'.replace(',', ' ')
    try: return (f'{float(x):.{d}f}').rstrip('0').rstrip('.').replace('.', ',')
    except Exception: return x
def sw(c): return f'<span class="nuancier" style="background:{e(c)}"></span>'
def ecrire(f, s): open(f'{D}/{f}', 'w').write(s); print(f, len(s) // 1024, 'Ko')
