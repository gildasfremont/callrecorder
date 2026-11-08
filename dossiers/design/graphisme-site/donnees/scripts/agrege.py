import json, csv, os, re, sys
from collections import defaultdict, Counter
D = sys.argv[1]; SITE = '/tmp/site'
X = json.load(open(f'{D}/extraction.json'))
def w(name, rows, fields=None):
    fields = fields or list(rows[0].keys())
    with open(f'{D}/{name}', 'w', newline='') as f:
        c = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore'); c.writeheader(); c.writerows(rows)
# Textes : dédoublonnés par (page, largeur, sélecteur, texte) en gardant les états
seen = {}
for t in X['textes']:
    k = (t['page'], t['largeur'], t['sel'], t['texte'])
    if k in seen: seen[k]['etat'] += ',' + t['etat'] if t['etat'] not in seen[k]['etat'] else ''; continue
    seen[k] = dict(t)
T = list(seen.values())
w('textes.csv', T)
# Styles de texte réellement rendus : combinaison famille/taille/graisse/interligne/couleur
combo = defaultdict(lambda: {'n': 0, 'ex': set(), 'pages': set()})
for t in T:
    if t['largeur'] != 1440: continue
    k = (t['famille'], t['taille'], t['graisse'], t['interligne'], t['couleur'])
    combo[k]['n'] += 1; combo[k]['pages'].add(t['page']); combo[k]['ex'].add(t['sel'].split(' > ')[-1])
rows = [dict(famille=k[0], taille=k[1], graisse=k[2], interligne=k[3], couleur=k[4], occurrences=v['n'], pages=' '.join(sorted(v['pages'])), selecteurs=' | '.join(sorted(v['ex']))[:300]) for k, v in sorted(combo.items(), key=lambda x: (-x[0][1], -x[1]['n']))]
w('styles-texte-1440.csv', rows)
print('styles de texte distincts à 1440 :', len(rows))
for lw in (375, 768, 1440):
    sz = Counter(round(t['taille'], 2) for t in T if t['largeur'] == lw)
    print(lw, 'tailles distinctes', len(sz), sorted(sz.items()))
print('couleurs de texte', Counter(t['couleur'] for t in T if t['largeur'] == 1440).most_common())
# Contrastes : chaque couple texte/fond, pire cas
pair = defaultdict(lambda: {'n': 0, 'min_wcag': 99, 'min_apca': 999, 'tailles': set(), 'ex': [], 'echecs_wcag': 0, 'echecs_apca': 0, 'complexe': ''})
for t in T:
    k = (t['couleur'], t['fond']); p = pair[k]
    p['n'] += 1; p['min_wcag'] = min(p['min_wcag'], t['wcag']); p['min_apca'] = min(p['min_apca'], t['apca_lc']); p['tailles'].add(t['taille'])
    p['echecs_wcag'] += not t['wcag_ok']; p['echecs_apca'] += not t['apca_ok']; p['complexe'] = p['complexe'] or t['fond_complexe']
    if len(p['ex']) < 3 and t['texte'][:40] not in [e[:40] for e in p['ex']]: p['ex'].append(f"{t['page']}@{t['largeur']} {t['sel'].split(' > ')[-1]} « {t['texte'][:50]} »")
rows = [dict(texte=k[0], fond=k[1], occurrences=v['n'], wcag_min=v['min_wcag'], apca_lc_min=v['min_apca'], tailles=' '.join(str(s) for s in sorted(v['tailles'])), echecs_wcag=v['echecs_wcag'], echecs_apca=v['echecs_apca'], fond_complexe=v['complexe'], exemples=' | '.join(v['ex'])) for k, v in sorted(pair.items(), key=lambda x: x[1]['min_wcag'])]
w('contrastes.csv', rows)
print('couples texte/fond', len(rows), 'échecs WCAG (couples)', sum(1 for r in rows if r['echecs_wcag']), 'échecs APCA (couples)', sum(1 for r in rows if r['echecs_apca']))
print('éléments en échec WCAG', sum(not t['wcag_ok'] for t in T), 'APCA', sum(not t['apca_ok'] for t in T), 'sur', len(T))
for r in rows[:14]: print(' ', r['texte'], r['fond'], r['wcag_min'], r['apca_lc_min'], r['echecs_wcag'], r['echecs_apca'], r['fond_complexe'][:20], r['exemples'][:120])
# Cibles
seen = {}
for t in X['cibles']:
    k = (t['page'], t['largeur'], t['sel'], t['texte'])
    if k not in seen: seen[k] = t
C = list(seen.values()); w('cibles.csv', C)
for lw in (375, 1440):
    cc = [c for c in C if c['largeur'] == lw]
    print('cibles', lw, len(cc), '<24 et sans espace', sum(not c['wcag_258'] for c in cc), '<44', sum(not c['hig_44'] for c in cc))
    for c in sorted(cc, key=lambda c: c['min'])[:12]: print('   ', c['page'], c['sel'].split(' > ')[-1][:40], c['texte'][:25], c['l'], c['h'], c['dist_voisin'])
# Images : par image unique, l'échelle à chaque largeur + poids du fichier
imgs = defaultdict(dict)
for i in X['images']:
    if not i['visible'] or i['etat'] not in ('repos', 'onglet-reunions', 'onglet-notes', 'tout-deplie'): continue
    src = i['src'].split('?')[0]; k = (i['page'], src)
    imgs[k].update({'page': i['page'], 'src': src, 'nat_l': i['nat_l'], 'nat_h': i['nat_h'], f"aff_{i['largeur']}": i['aff_l'], f"echelle_{i['largeur']}": i['echelle_2x'], 'attr_dim': bool(i['attr_l']), 'loading': i['loading'], 'alt_long': len(i['alt'] or ''), 'decoupe': i['decoupe'], 'bord': i['bord'], 'rayon': i['rayon'], 'ombre_boite': i['ombre_boite'], 'filtre': i['filtre']})
rows = []
for (pg, src), v in imgs.items():
    path = os.path.normpath(os.path.join(SITE, '' if pg == 'accueil' else pg, src))
    v['octets'] = os.path.getsize(path) if os.path.exists(path) else ''
    v['format'] = src.rsplit('.', 1)[-1]
    rows.append(v)
F = ['page', 'src', 'format', 'octets', 'nat_l', 'nat_h', 'aff_375', 'aff_768', 'aff_1440', 'echelle_375', 'echelle_768', 'echelle_1440', 'attr_dim', 'loading', 'alt_long', 'decoupe', 'bord', 'rayon', 'ombre_boite', 'filtre']
w('images.csv', rows, F)
print('images visibles uniques', len(rows), 'octets', sum(r['octets'] or 0 for r in rows))
for r in rows:
    if r.get('echelle_1440') and (r['echelle_1440'] < 0.8 or r['echelle_1440'] > 1.05) and r['page'] in ('fonctionnalites', 'versions', 'guides'): print('  ', r['page'], r['src'], r['echelle_1440'], r.get('echelle_375'))
