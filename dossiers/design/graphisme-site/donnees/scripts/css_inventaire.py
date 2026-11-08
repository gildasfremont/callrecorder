# Inventaire de chaque valeur de style.css (et des styles posés par les HTML et le JS), avec sélecteur et ligne.
import re, csv, sys, json, glob, os
SITE = '/tmp/site'; OUT = sys.argv[1]
def decls(path, text, origin):
    out = []; stack = []; buf = ''; line = 1; start = 1; i = 0; media = []
    text = re.sub(r'/\*.*?\*/', lambda m: re.sub(r'[^\n]', ' ', m.group(0)), text, flags=re.S)
    while i < len(text):
        c = text[i]
        if c == '\n': line += 1
        if c == '{':
            s = buf.strip(); stack.append(s); buf = ''; start = line
        elif c == '}':
            d = buf.strip()
            if d and ':' in d and stack: out.append((path, start, stack[-1], d, [x for x in stack[:-1] if x.startswith('@')]))
            buf = ''; stack and stack.pop(); start = line
        elif c == ';' and stack:
            d = buf.strip()
            if d and ':' in d: out.append((path, start, stack[-1], d, [x for x in stack[:-1] if x.startswith('@')]))
            buf = ''; start = line
        else:
            if not buf.strip(): start = line
            buf += c
        i += 1
    return out
rows = []
css = open(f'{SITE}/style.css').read()
D = decls('style.css', css, 'css')
# styles en ligne dans les HTML
for f in ['index.html'] + sorted(glob.glob(f'{SITE}/*/index.html')):
    p = f if f.startswith('/') else f'{SITE}/{f}'; rel = os.path.relpath(p, SITE)
    for n, l in enumerate(open(p), 1):
        for m in re.finditer(r'style="([^"]+)"', l):
            for d in m.group(1).split(';'):
                if ':' in d: D.append((rel, n, '[style]', d.strip(), []))
for f in sorted(glob.glob(f'{SITE}/*.js')):
    rel = os.path.basename(f)
    for n, l in enumerate(open(f), 1):
        for m in re.finditer(r'\.style\.(\w+)\s*=\s*([^;]+)', l): D.append((rel, n, '[js]', f'{m.group(1)}: {m.group(2).strip()}', []))
COLOR = re.compile(r'#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)|\b(white|black|transparent|currentColor)\b')
LEN = re.compile(r'-?\d*\.?\d+(px|em|rem|%|vw|vh|cqw|vmax|ch)|\b0\b')
def cat(prop):
    p = prop.lower()
    if p in ('font-size',): return 'taille'
    if p == 'font-weight': return 'graisse'
    if p == 'line-height': return 'interligne'
    if p == 'letter-spacing': return 'approche'
    if p == 'font-family': return 'famille'
    if p == 'font': return 'font'
    if 'radius' in p: return 'rayon'
    if p in ('box-shadow', 'filter', 'text-shadow'): return 'ombre'
    if re.match(r'(margin|padding|gap|row-gap|column-gap|top|left|right|bottom|inset)', p): return 'espacement'
    if p in ('width', 'height', 'max-width', 'min-width', 'min-height', 'max-height'): return 'dimension'
    if p in ('transition', 'animation') or 'duration' in p: return 'mouvement'
    if p == 'opacity': return 'opacite'
    if p == 'z-index': return 'plan'
    return 'autre'
for path, line, sel, d, media in D:
    prop, val = d.split(':', 1); prop = prop.strip(); val = val.strip()
    if prop.startswith('--'):
        rows.append(dict(fichier=path, ligne=line, selecteur=sel, media=' '.join(media), propriete=prop, categorie='variable', valeur=val)); continue
    c = cat(prop)
    base = dict(fichier=path, ligne=line, selecteur=sel, media=' '.join(media), propriete=prop)
    for m in COLOR.finditer(val): rows.append(dict(base, categorie='couleur', valeur=re.sub(r'\s+', '', m.group(0)).lower()))
    if c == 'font':
        m = re.match(r'(?:(\d{3})\s+)?(\d+(?:\.\d+)?px)(?:/([\d.]+\w*))?\s+(.*)', val)
        if m:
            if m.group(1): rows.append(dict(base, categorie='graisse', valeur=m.group(1)))
            rows.append(dict(base, categorie='taille', valeur=m.group(2)))
            if m.group(3): rows.append(dict(base, categorie='interligne', valeur=m.group(3)))
            rows.append(dict(base, categorie='famille', valeur=m.group(4).split(',')[0].strip()))
        else: rows.append(dict(base, categorie='taille', valeur=val))
    elif c in ('taille', 'graisse', 'interligne', 'approche', 'famille', 'opacite', 'plan', 'mouvement'):
        rows.append(dict(base, categorie=c, valeur=val if c != 'famille' else val.split(',')[0].strip()))
    elif c in ('espacement', 'rayon', 'dimension'):
        if 'clamp' in val or 'calc' in val or 'max(' in val or 'var(' in val: rows.append(dict(base, categorie=c, valeur=val))
        else:
            for m in LEN.finditer(val): rows.append(dict(base, categorie=c, valeur=m.group(0)))
    elif c == 'ombre':
        rows.append(dict(base, categorie='ombre', valeur=val))
# points de rupture
for n, l in enumerate(css.split('\n'), 1):
    for m in re.finditer(r'@media\s*([^{]+)', l):
        for b in re.findall(r'(max|min)-width:\s*(\d+)px', m.group(1)): rows.append(dict(fichier='style.css', ligne=n, selecteur='@media', media='', propriete=b[0] + '-width', categorie='rupture', valeur=b[1] + 'px'))
with open(f'{OUT}/css-valeurs.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['categorie', 'valeur', 'propriete', 'selecteur', 'media', 'fichier', 'ligne']); w.writeheader(); w.writerows(sorted(rows, key=lambda r: (r['categorie'], r['valeur'], r['fichier'], r['ligne'])))
# résumé : chaque valeur, combien de fois, où
from collections import defaultdict
agg = defaultdict(list)
for r in rows: agg[(r['categorie'], r['valeur'])].append(f"{r['fichier']}:{r['ligne']}")
summ = [dict(categorie=k[0], valeur=k[1], occurrences=len(v), lieux=' '.join(v)) for k, v in agg.items()]
summ.sort(key=lambda r: (r['categorie'], -r['occurrences']))
with open(f'{OUT}/css-resume.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['categorie', 'valeur', 'occurrences', 'lieux']); w.writeheader(); w.writerows(summ)
from collections import Counter
print(len(rows), 'valeurs', Counter(r['categorie'] for r in rows))
for c in ['taille', 'graisse', 'interligne', 'rayon', 'couleur', 'rupture', 'approche', 'famille']:
    print(c, len([s for s in summ if s['categorie'] == c]), [(s['valeur'], s['occurrences']) for s in summ if s['categorie'] == c][:40])
