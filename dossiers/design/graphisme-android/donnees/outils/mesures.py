"""Mesures : contrastes (WCAG 2.x et APCA 0.0.98G-4g) de chaque texte réellement dessiné, cibles tactiles, sémantique d'accessibilité.
Entrée : les relevés JSON de l'arbre des vues (copie du banc, Robolectric). Sortie : CSV et JSON dans donnees/."""
import json, glob, os, csv, collections

REL = '/tmp/claude-0/releve/android/app/build/releve'
OUT = '/home/user/callrecorder-app/design/recos/graphisme-android/donnees'

def parse(h):
    h = h.lstrip('#')
    if len(h) == 6: h = 'FF' + h
    a = int(h[0:2], 16) / 255; r = int(h[2:4], 16); g = int(h[4:6], 16); b = int(h[6:8], 16)
    return (r, g, b, a)

def over(fg, bg):
    r, g, b, a = fg; R, G, B, _ = bg
    return (r * a + R * (1 - a), g * a + G * (1 - a), b * a + B * (1 - a), 1.0)

def lin(c):
    c = c / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def lum(c): return 0.2126 * lin(c[0]) + 0.7152 * lin(c[1]) + 0.0722 * lin(c[2])

def wcag(fg, bg):
    a, b = lum(fg), lum(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)

def apca(txt, bg):
    def Y(c): return sum(((v / 255) ** 2.4) * k for v, k in zip(c[:3], (0.2126729, 0.7151522, 0.0721750)))
    yt, yb = Y(txt), Y(bg)
    thr, cl = 0.022, 1.414
    if yt < thr: yt += (thr - yt) ** cl
    if yb < thr: yb += (thr - yb) ** cl
    if abs(yb - yt) < 0.0005: return 0.0
    if yb > yt:
        s = (yb ** 0.56 - yt ** 0.57) * 1.14
        o = 0 if s < 0.1 else s - 0.027
    else:
        s = (yb ** 0.65 - yt ** 0.62) * 1.14
        o = 0 if s > -0.1 else s + 0.027
    return o * 100

def hexc(c): return '#%02X%02X%02X' % tuple(round(v) for v in c[:3])

def bgfill(v):
    b = v.get('bg')
    while b and b.get('kind') == 'ripple': b = b.get('layer')
    # flat() : le masque noir opaque d'un RippleDrawable n'est pas un fond.
    if b and b.get('color') and b['color'] != '#FF000000': return b['color']
    return None

def short(f): return f

rows_txt, rows_tgt, rows_a11y, rows_over = [], [], [], []
stats = collections.Counter()
for path in sorted(glob.glob(REL + '/**/*.json', recursive=True)):
    d = json.load(open(path))
    var = (d['variante'].strip('/') or 'base')
    if d['night'] and var != 'sombre': var = var + '+nuit'
    ecran = d['ecran']
    vues = d['vues']
    night = d['night']
    page = parse('#FF1E1E1E' if night else '#FFF5F5F5')
    # fond effectif : composé des ancêtres
    eff = {}
    for v in vues:
        base = eff.get(v['parent'], page)
        f = bgfill(v)
        eff[v['i']] = over(parse(f), base) if f else base
    byid = {v['i']: v for v in vues}
    for v in vues:
        p = byid.get(v['parent'])
        if p and v['w'] > 0 and v['h'] > 0 and p['cls'] not in ('ListView', 'ScrollView') and 'text' in v and v['text'].strip():
            ob = (v['y'] + v['h']) - (p['y'] + p['h']); orr = (v['x'] + v['w']) - (p['x'] + p['w']); ot = p['y'] - v['y']
            if max(ob, orr, ot) > 0.5:
                rows_over.append({'variante': var, 'ecran': ecran, 'texte': v['text'][:60].replace('\n', ' ⏎ '), 'sp': round(v['sp'], 1),
                    'deborde_bas': round(ob, 1), 'deborde_droite': round(orr, 1), 'deborde_haut': round(ot, 1), 'parent': p['cls'], 'parent_h': round(p['h'], 1)})
    for v in vues:
        if v['w'] <= 0 or v['h'] <= 0: continue
        if 'text' in v and v['text'].strip():
            bg = eff.get(v['parent'], page)
            own = bgfill(v)
            if own: bg = over(parse(own), bg)
            fgc = over(parse(v['color']), bg)
            r = wcag(fgc, bg); lc = apca(fgc, bg)
            sp = v['sp']; weight = v['weight']
            large = sp >= 24 or (sp >= 18.66 and weight >= 700)
            need = 3.0 if large else 4.5
            # APCA, mode simple « bronze » : 75 pour les colonnes de texte, 60 pour le reste du texte lisible, 45 pour les grands titres.
            role = 'replique' if (sp >= 16 and v['cls'] == 'TextView' and v.get('maxLines', 0) > 100 and len(v['text']) > 30) else 'texte'
            needlc = 75 if role == 'replique' else (45 if sp >= 24 else 60)
            for t in v['text'].split('\n')[:1]: pass
            rows_txt.append({'variante': var, 'ecran': ecran, 'texte': v['text'][:70].replace('\n', ' ⏎ '), 'classe': v['cls'],
                'sp': round(sp, 1), 'dp_rendu': round(v['px'] / d['density'], 1), 'graisse': weight, 'couleur': v['color'], 'texte_compose': hexc(fgc), 'fond_compose': hexc(bg),
                'wcag': round(r, 2), 'wcag_requis': need, 'wcag_ok': r >= need, 'apca_lc': round(abs(lc), 1), 'apca_requis': needlc,
                'apca_ok': abs(lc) >= needlc, 'lignes': v.get('lines'), 'coupe': v.get('ellipsized'),
                'x': round(v['x'], 1), 'y': round(v['y'], 1), 'w': round(v['w'], 1), 'h': round(v['h'], 1), 'tnum': 'tnum' in v.get('features', '')})
            if 'hint' in v and v['hint']:
                hc = over(parse(v['hintColor']), bg)
                rows_txt.append({'variante': var, 'ecran': ecran, 'texte': '(indice) ' + v['hint'], 'classe': v['cls'], 'sp': round(sp, 1), 'dp_rendu': round(v['px'] / d['density'], 1), 'graisse': weight,
                    'couleur': v['hintColor'], 'texte_compose': hexc(hc), 'fond_compose': hexc(bg), 'wcag': round(wcag(hc, bg), 2), 'wcag_requis': 4.5,
                    'wcag_ok': wcag(hc, bg) >= 4.5, 'apca_lc': round(abs(apca(hc, bg)), 1), 'apca_requis': 60, 'apca_ok': abs(apca(hc, bg)) >= 60,
                    'lignes': '', 'coupe': '', 'x': round(v['x'], 1), 'y': round(v['y'], 1), 'w': round(v['w'], 1), 'h': round(v['h'], 1), 'tnum': ''})
        if v['clickable'] and not (v['cls'] == 'TextView' and not v.get('desc') and len(v.get('text', '')) > 0 and not v['focusable'] is False and v.get('maxLines', 0) > 100):
            # le nom : la description, sinon le texte, sinon les textes des enfants
            name = v.get('desc') or v.get('text') or ''
            if not name:
                kids = [u for u in vues if u['parent'] == v['i']]
                name = ' '.join(u.get('text', '') for u in kids).strip()
            rows_tgt.append({'variante': var, 'ecran': ecran, 'classe': v['cls'], 'nom': name[:60].replace('\n', ' ⏎ '),
                'w': round(v['w'], 1), 'h': round(v['h'], 1), 'min48': v['w'] >= 47.5 and v['h'] >= 47.5,
                'min24': v['w'] >= 23.5 and v['h'] >= 23.5, 'x': round(v['x'], 1), 'y': round(v['y'], 1),
                'etat': v.get('state', ''), 'titre': v.get('heading')})
        if v['cls'] in ('ImageView', 'ImageButton') or v.get('heading') or v.get('desc'):
            rows_a11y.append({'variante': var, 'ecran': ecran, 'classe': v['cls'], 'icone': v.get('res', ''), 'description': v.get('desc', ''),
                'importante': {0: 'auto', 1: 'oui', 2: 'non', 4: 'non (descendants)'}.get(v['important'], v['important']),
                'cliquable': v['clickable'], 'titre': v.get('heading'), 'w': round(v['w'], 1), 'h': round(v['h'], 1)})

def write(name, rows):
    if not rows: return
    with open(f'{OUT}/{name}.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, list(rows[0].keys())); w.writeheader(); w.writerows(rows)

write('mesures-contrastes-textes', rows_txt)
write('mesures-cibles', rows_tgt)
write('mesures-accessibilite', rows_a11y)
write('mesures-debordements', rows_over)

# Résumé
def uniq(rows, keys):
    seen, out = set(), []
    for r in rows:
        k = tuple(r[x] for x in keys)
        if k not in seen: seen.add(k); out.append(r)
    return out
s = {}
for var in sorted(set(r['variante'] for r in rows_txt)):
    rr = [r for r in rows_txt if r['variante'] == var]
    s[var] = {'textes': len(rr), 'wcag_echecs': sum(not r['wcag_ok'] for r in rr), 'apca_echecs': sum(not r['apca_ok'] for r in rr),
              'coupes': sum(bool(r['coupe']) for r in rr)}
    tt = [r for r in rows_tgt if r['variante'] == var]
    s[var].update({'cibles': len(tt), 'cibles_sous_48': sum(not r['min48'] for r in tt), 'debordements': sum(r['variante'] == var for r in rows_over)})
json.dump(s, open(f'{OUT}/mesures-resume.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps(s, ensure_ascii=False, indent=1))
print('--- échecs WCAG (uniques par couleur/fond/taille)')
for r in uniq([r for r in rows_txt if not r['wcag_ok']], ['variante', 'texte_compose', 'fond_compose', 'sp']):
    print(r['variante'], r['ecran'], r['texte'][:40], r['sp'], r['couleur'], r['fond_compose'], r['wcag'], r['apca_lc'])
print('--- APCA sous seuil (uniques)')
for r in uniq([r for r in rows_txt if not r['apca_ok'] and r['wcag_ok']], ['variante', 'texte_compose', 'fond_compose', 'sp']):
    print(r['variante'], r['ecran'], r['texte'][:40], r['sp'], r['couleur'], r['fond_compose'], r['wcag'], r['apca_lc'], r['apca_requis'])
print('--- cibles < 48')
for r in uniq([r for r in rows_tgt if not r['min48']], ['variante', 'nom', 'w', 'h']):
    print(r['variante'], r['ecran'], r['nom'], r['w'], r['h'])
