import json, sys, os
from PIL import Image, ImageDraw, ImageFont
SRC, OUT = sys.argv[1], sys.argv[2]
M = json.load(open(f'{SRC}/preuves.json'))
RED = (200, 30, 30); GREEN = (20, 130, 60)
for id, m in M.items():
    im = Image.open(f'{SRC}/{id}.png').convert('RGB')
    s = m.get('scale') or 1
    if m.get('full'):
        sc = m['scale']; im = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS); s = sc
        im = im.crop((0, 0, im.width, min(im.height, 2400)))
    F = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-SemiBold.otf', int(13 * max(s, 1)) if not m.get('full') else 14)
    d = ImageDraw.Draw(im)
    for l in (m.get('lines') or []):
        x = l['x'] * s; c = RED if l['c'] == 'r' else GREEN
        for y in range(0, im.height, 12): d.line([(x, y), (x, y + 6)], fill=c, width=2)
        d.text((x + 4, 6), l['t'], font=F, fill=c)
    notes = m.get('notes') or []
    pad = int(26 * max(s, 1)) * len(notes)
    if notes:
        canvas = Image.new('RGB', (im.width, im.height + pad + 8), (255, 255, 255)); canvas.paste(im, (0, 0)); im = canvas; d = ImageDraw.Draw(im)
    for i, n in enumerate(notes, 1):
        x, y, w, h = n['x'] * s, n['y'] * s, n['w'] * s, n['h'] * s
        d.rectangle([x - 3, y - 3, x + w + 3, y + h + 3], outline=RED, width=max(2, int(1.5 * s)))
        r = int(11 * max(s, 1)); cx, cy = max(r, x - 3), max(r, y - 3)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED); d.text((cx, cy), str(i), font=F, fill='white', anchor='mm')
        ty = im.height - pad - 8 + (i - 1) * int(26 * max(s, 1)) + 6
        d.ellipse([8, ty, 8 + 2 * r, ty + 2 * r], fill=RED); d.text((8 + r, ty + r), str(i), font=F, fill='white', anchor='mm')
        d.text((16 + 2 * r, ty + r), n['txt'], font=F, fill=RED, anchor='lm')
    # Taille raisonnable pour le dossier
    if im.width > 1600: im = im.resize((1600, int(im.height * 1600 / im.width)), Image.LANCZOS)
    im.save(f'{OUT}/{id}.png', optimize=True)
    print(id, im.size, os.path.getsize(f'{OUT}/{id}.png') // 1024, 'Ko')
