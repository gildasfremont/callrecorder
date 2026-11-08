# Avant / après : les mêmes mesures sur le site en ligne et sur les prototypes.
import json, sys, csv
from collections import Counter, defaultdict
D = sys.argv[1]
def load(n): return json.load(open(f'{D}/{n}.json'))
A, B = load('extraction'), load('extraction-apres')
axA, axB = load('axe'), load('axe-apres')
def dedup(L, key):
    s = {}
    for t in L: s.setdefault(key(t), t)
    return list(s.values())
def stats(X, ax):
    T = dedup(X['textes'], lambda t: (t['page'], t['largeur'], t['sel'], t['texte']))
    C = dedup(X['cibles'], lambda t: (t['page'], t['largeur'], t['sel'], t['texte']))
    I = [i for i in X['images'] if i['visible'] and i['page'] in ('fonctionnalites', 'versions') and i['etat'] == 'repos' and 'gildas' not in i['src']]
    r = {}
    r['textes mesurés'] = len(T)
    r['textes sous WCAG 2 AA (1.4.3)'] = sum(not t['wcag_ok'] for t in T)
    r['textes sous APCA (seuil Bronze)'] = sum(not t['apca_ok'] for t in T)
    r['contraste WCAG le plus bas'] = min(t['wcag'] for t in T)
    for w in (375, 1440): r[f'tailles de texte distinctes à {w}'] = len({round(t['taille'], 1) for t in T if t['largeur'] == w})
    r['styles de texte distincts à 1440 (famille, taille, graisse, interligne, couleur)'] = len({(t['famille'], t['taille'], t['graisse'], t['interligne'], t['couleur']) for t in T if t['largeur'] == 1440})
    r['cibles sous 24 px sans espace (WCAG 2.5.8)'] = sum(1 for c in C if not c['wcag_258'] and not c.get('dans_phrase'))
    for w in (375, 1440):
        e = [i['echelle_2x'] for i in I if i['largeur'] == w and i['echelle_2x']]
        r[f'captures Fonctionnalités et Versions à {w} : échelle min'] = min(e); r[f'captures Fonctionnalités et Versions à {w} : échelle max'] = max(e)
        r[f'captures sous ×0,8 à {w}'] = sum(1 for x in e if x < 0.8)
        r[f'captures au-dessus de ×1,05 à {w}'] = sum(1 for x in e if x > 1.05)
    r['violations axe (nœuds, 5 pages × 2 largeurs)'] = sum(v['noeuds'] for v in ax)
    r['règles axe en échec'] = len({v['regle'] for v in ax})
    r['hauteur des pages à 1440 (px)'] = {p['page']: p['hauteur'] for p in X['pages'] if p['largeur'] == 1440 and p['etat'] == 'repos'}
    r['hauteur des pages à 375 (px)'] = {p['page']: p['hauteur'] for p in X['pages'] if p['largeur'] == 375 and p['etat'] == 'repos'}
    return r
a, b = stats(A, axA), stats(B, axB)
rows = [dict(mesure=k, avant=json.dumps(a[k], ensure_ascii=False) if isinstance(a[k], dict) else a[k], apres=json.dumps(b[k], ensure_ascii=False) if isinstance(b[k], dict) else b[k]) for k in a]
with open(f'{D}/avant-apres.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['mesure', 'avant', 'apres']); w.writeheader(); w.writerows(rows)
for r in rows: print(r['mesure'], '|', r['avant'], '→', r['apres'])
# Échecs APCA restants, pour les décrire
T = dedup(B['textes'], lambda t: (t['page'], t['largeur'], t['sel'], t['texte']))
print(Counter((t['couleur'], t['fond'], t['taille'], t['graisse']) for t in T if not t['apca_ok']).most_common(8))
print([ (t['page'],t['sel'][-50:],t['texte'][:30],t['wcag']) for t in T if not t['wcag_ok']][:10])
