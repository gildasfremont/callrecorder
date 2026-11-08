"""Captures recadrées et annotées : les positions viennent des relevés (dp × densité), pas de l'œil."""
import json, os
from PIL import Image, ImageDraw, ImageFont

BANC = '/tmp/claude-0/releve/android/app/build/banc'
REL = '/tmp/claude-0/releve/android/app/build/releve'
OUT = '/home/user/callrecorder-app/design/recos/graphisme-android/images'
os.makedirs(OUT, exist_ok=True)
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
if not os.path.exists(FONT):
    import glob
    FONT = (glob.glob('/usr/share/fonts/**/*Sans*.ttf', recursive=True) or [None])[0]
RED = (232, 89, 12); GREEN = (47, 158, 68); BLUE = (25, 113, 194)

def load(var, ecran):
    d = json.load(open(f'{REL}/{var}{ecran}.json'))
    im = Image.open(f'{BANC}/{var}{ecran}.png').convert('RGB')
    return d, im

def find(d, pred):
    return [v for v in d['vues'] if pred(v)]

def box(v, s):
    return [v['x'] * s, v['y'] * s, (v['x'] + v['w']) * s, (v['y'] + v['h']) * s]

def font(sz):
    return ImageFont.truetype(FONT, sz) if FONT else ImageFont.load_default()

def label(dr, xy, text, color=RED, sz=30):
    f = font(sz)
    x, y = xy
    l, t, r, b = dr.textbbox((x, y), text, font=f)
    dr.rectangle([l - 8, t - 6, r + 8, b + 6], fill=color)
    dr.text((x, y), text, fill='white', font=f)

def save(im, name, crop_dp, s, scale=0.5):
    x0, y0, x1, y1 = [c * s for c in crop_dp]
    c = im.crop((int(x0), int(y0), int(x1), int(y1)))
    if scale != 1: c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
    c.save(f'{OUT}/{name}.png', optimize=True)
    return name

made = []

# 1. Voix d'une réunion : même orange
d, im = load('clair/', 'site-reunion'); s = d['density']; dr = ImageDraw.Draw(im)
marks = find(d, lambda v: v.get('text') in ('V1', 'V2', 'M') and v['w'] < 40)
for v in marks[:7]:
    dr.ellipse(box(v, s), outline=RED if v['text'] != 'M' else BLUE, width=5)
label(dr, (70 * s, 470 * s), 'Voix 1 et Voix 2 : #A0470A à 12 % (le même rond)')
made.append(save(im, 'p01-voix-meme-couleur', (0, 80, 412, 500), s))

# 2. Accent en sombre
d, im = load('sombre/', 'accueil-ecoute'); s = d['density']; dr = ImageDraw.Draw(im)
v = find(d, lambda v: v.get('text', '').startswith('● Écoute'))[0]
dr.rectangle(box(v, s), outline=RED, width=5)
label(dr, (v['x'] * s, (v['y'] + v['h'] + 6) * s), '#0064D2 sur #1E1E1E : 2,98:1 · APCA Lc 22,8')
made.append(save(im, 'p02-sombre-ecoute', (0, 60, 412, 175), s))
d, im = load('sombre/', 'reglages'); s = d['density']; dr = ImageDraw.Draw(im)
v = find(d, lambda v: v.get('text') == 'Relier un calendrier')[0]
dr.rectangle(box(v, s), outline=RED, width=5)
label(dr, ((v['x'] + v['w'] + 8) * s, v['y'] * s), '2,61:1', sz=34)
made.append(save(im, 'p02-sombre-relier', (0, 230, 412, 420), s))

# 3. Curseur coupé
d, im = load('clair/', 'conversation'); s = d['density']; dr = ImageDraw.Draw(im)
sb = find(d, lambda v: v['cls'] == 'SeekBar')[0]
dr.rectangle(box(sb, s), outline=RED, width=4)
cx = sb['x'] * s; cy = (sb['y'] + sb['h'] / 2) * s
dr.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], outline=RED, width=5)
label(dr, (sb['x'] * s + 60, (sb['y'] + sb['h'] + 30) * s), 'SeekBar : marge 0 → rond coupé ; 26 dp de haut')
made.append(save(im, 'p03-curseur-coupe', (0, 64, 412, 170), s))

# 4. En cours gris dans l'en-tête
d, im = load('', 'conversation-en-direct'); s = d['density']; dr = ImageDraw.Draw(im)
v = find(d, lambda v: '● En cours' in v.get('text', ''))[0]
dr.rectangle(box(v, s), outline=RED, width=5)
label(dr, (v['x'] * s, (v['y'] + v['h'] + 8) * s), "« ● En cours » en #99000000, pas en LIVE")
made.append(save(im, 'p04-en-cours-gris', (0, 0, 412, 110), s))
d, im = load('clair/', 'accueil-enregistre'); s = d['density']; dr = ImageDraw.Draw(im)
v = find(d, lambda v: '● En cours' in v.get('text', ''))[0]
dr.rectangle(box(v, s), outline=GREEN, width=5)
made.append(save(im, 'p04-en-cours-liste', (0, 90, 412, 165), s))

# 6. Heures des répliques à 50 %
d, im = load('clair/', 'conversation'); s = d['density']; dr = ImageDraw.Draw(im)
for v in find(d, lambda v: v.get('color') == '#7F000000'):
    dr.rectangle(box(v, s), outline=RED, width=4)
label(dr, (90 * s, 300 * s), '13 sp à 50 % : 3,88:1 (requis 4,5:1)')
made.append(save(im, 'p06-heures', (0, 170, 412, 330), s))

# 7. Bords gauches des Réglages
d, im = load('clair/', 'reglages'); s = d['density']; dr = ImageDraw.Draw(im)
edges = {}
for t in ('Enregistrement', 'Intégrations', 'Enregistrer les appels', 'Calendrier', 'Mac'):
    for v in find(d, lambda v: v.get('text') == t): edges[t] = v['x'] + v['pad'][0]
for v in find(d, lambda v: v['cls'] == 'RadioButton'): edges.setdefault('rond des modes', v['x'] + v['pad'][0]);
xs = sorted(set(round(x, 1) for x in edges.values()))
for i, x in enumerate(xs):
    dr.line([(x * s, 0), (x * s, im.height)], fill=RED, width=3)
    label(dr, (x * s + 6, (100 + i * 40) * s), f'{x:g} dp', sz=26)
made.append(save(im, 'p07-bords-reglages', (0, 80, 412, 560), s))
json.dump(edges, open('/home/user/callrecorder-app/design/recos/graphisme-android/donnees/mesure-bords-reglages.json', 'w'), ensure_ascii=False, indent=1)

# 10. Calendrier : flèches et aujourd'hui
d, im = load('clair/', 'calendrier'); s = d['density']; dr = ImageDraw.Draw(im)
for v in find(d, lambda v: v.get('desc') in ('Mois précédent', 'Mois suivant')):
    dr.rectangle(box(v, s), outline=RED, width=5)
v = [v for v in find(d, lambda v: v.get('text') == '8' and v['color'] != '#FF1D1D1F')][0]
dr.rectangle(box(v, s), outline=RED, width=5)
label(dr, (150 * s, 128 * s), 'deux flèches, deux dessins', sz=28)
label(dr, (205 * s, 222 * s), '« 8 » : #0064D2 sur gris 12 % = 3,93:1', sz=28)
made.append(save(im, 'p10-calendrier', (0, 64, 412, 250), s))

# 12. Texte en direct à 16 dp
d, im = load('', 'conversation-en-direct'); s = d['density']; dr = ImageDraw.Draw(im)
for v in find(d, lambda v: v.get('text') in ('on commence par le budget',)):
    dr.line([(v['x'] * s, (v['y'] - 30) * s), (v['x'] * s, (v['y'] + 60) * s)], fill=RED, width=4)
    label(dr, ((v['x'] + 4) * s, (v['y'] + 30) * s), f"x = {v['x']:g} dp (répliques finies : 64 dp)", sz=28)
made.append(save(im, 'p12-direct-retrait', (0, 70, 412, 240), s))

# 13. Mise en route : flèche orpheline
d, im = load('clair/', 'mise-en-route'); s = d['density']; dr = ImageDraw.Draw(im)
v = find(d, lambda v: v.get('text', '').startswith('Sur le Mac'))[0]
dr.rectangle(box(v, s), outline=RED, width=4)
made.append(save(im, 'p13-fleche-orpheline', (0, v['y'] - 70, 412, v['y'] + v['h'] + 70), s))

# 17. En-tête coupé
d, im = load('clair/', 'conversation'); s = d['density']; dr = ImageDraw.Draw(im)
v = find(d, lambda v: 'Sophie Marchand, Karim' in v.get('text', '') and v['y'] < 64)[0]
dr.rectangle(box(v, s), outline=RED, width=4)
made.append(save(im, 'p17-entete-coupe', (0, 0, 412, 70), s))

# 18. Texte à 200 % : barre du bas, en-tête, initiales
d, im = load('texte200/', 'conversation-recherche'); s = d['density']; dr = ImageDraw.Draw(im)
tb = [v for v in find(d, lambda v: v.get('desc') in ('Rechercher', 'Copier', 'Télécharger', 'Détails') and v['y'] > 600)]
for v in tb: dr.rectangle(box(v, s), outline=RED, width=4)
made.append(save(im, 'p18-200-barre', (0, 760, 412, 915), s))
d, im = load('texte200/', 'conversation-recherche'); s = d['density']; dr = ImageDraw.Draw(im)
v = find(d, lambda v: v['cls'] == 'TextView' and v['y'] < 64 and '47 min' in v.get('text', ''))[0]
dr.rectangle(box(v, s), outline=RED, width=4)
for v in find(d, lambda v: v.get('text') in ('SM', 'KB', 'M') and v['w'] < 40): dr.rectangle(box(v, s), outline=RED, width=4)
made.append(save(im, 'p18-200-entete', (0, 0, 412, 330), s))

# 19. Calendrier à 360 dp : cellules 45,7 dp
d, im = load('etroit/', 'calendrier'); s = d['density']; dr = ImageDraw.Draw(im)
cells = find(d, lambda v: v.get('desc', '').startswith(('Lundi', 'Mardi')) and v['clickable'])
for v in cells[:4]: dr.rectangle(box(v, s), outline=RED, width=3)
label(dr, (20 * s, 400 * s), f"cellule : {cells[0]['w']:g} × {cells[0]['h']:g} dp à 360 dp de large", sz=28)
made.append(save(im, 'p19-cellules-360', (0, 64, 360, 420), s))

# 20. Lire 44 dp, champs 42 dp
d, im = load('clair/', 'conversation-recherche'); s = d['density']; dr = ImageDraw.Draw(im)
for v in find(d, lambda v: v.get('desc') == 'Lire' or v['cls'] == 'EditText'):
    dr.rectangle(box(v, s), outline=RED, width=4)
    label(dr, ((v['x'] + v['w'] - 120) * s if v['w'] > 100 else (v['x'] + v['w'] + 4) * s, (v['y'] + 4) * s), f"{v['w']:g}×{v['h']:g}" if v['w'] < 100 else f"h {v['h']:g} dp", sz=26)
made.append(save(im, 'p20-cibles', (0, 64, 412, 240), s))

print(made)
