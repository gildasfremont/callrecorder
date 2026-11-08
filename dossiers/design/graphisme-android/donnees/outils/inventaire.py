"""Inventaire statique de l'app Android : chaque valeur visuelle du code, avec fichier:ligne."""
import csv, json, re, os, glob, collections

ROOT = '/home/user/callrecorder-app/phone/android/app/src/main'
OUT = '/home/user/callrecorder-app/design/recos/graphisme-android/donnees'
os.makedirs(OUT, exist_ok=True)
KT = sorted(glob.glob(ROOT + '/java/fyi/gildas/callrecorder/*.kt')) + sorted(glob.glob(ROOT + '/java/fyi/gildas/callrecorder/*.java'))

def rel(p): return os.path.relpath(p, '/home/user/callrecorder-app')

lines = {}
for f in KT:
    lines[f] = open(f, encoding='utf-8').read().split('\n')

rows = collections.defaultdict(list)

def add(kind, f, n, value, role, ctx):
    rows[kind].append({'fichier': rel(f), 'ligne': n, 'valeur': value, 'role': role, 'contexte': ctx.strip()[:180]})

# Parse label(...) calls robustly: find 'label(' and extract balanced args.
def calls(text, name):
    for m in re.finditer(r'\b' + name + r'\(', text):
        i = m.end(); depth = 1; j = i
        while j < len(text) and depth:
            if text[j] == '(': depth += 1
            elif text[j] == ')': depth -= 1
            elif text[j] == '"':
                j += 1
                while j < len(text) and text[j] != '"':
                    if text[j] == '\\': j += 1
                    j += 1
            j += 1
        yield m.start(), text[i:j - 1]

def split_args(a):
    out, depth, cur, q = [], 0, '', False
    for ch in a:
        if ch == '"' : q = not q
        if not q and ch in '([{': depth += 1
        if not q and ch in ')]}': depth -= 1
        if ch == ',' and depth == 0 and not q:
            out.append(cur.strip()); cur = ''
        else: cur += ch
    if cur.strip(): out.append(cur.strip())
    return out

for f in KT:
    text = '\n'.join(lines[f])
    def lineno(pos): return text.count('\n', 0, pos) + 1
    # --- tailles de texte
    for pos, a in calls(text, 'label'):
        if 'fun label' in text[max(0, pos - 4):pos + 6]: continue
        args = split_args(a)
        size = '16 (défaut)'; color = 'look.text (défaut)'; bold = 'non'
        pos_args = [x for x in args if '=' not in x.split('(')[0]]
        named = dict(x.split('=', 1) for x in args if re.match(r'^\w+\s*=', x))
        named = {k.strip(): v.strip() for k, v in named.items()}
        if len(pos_args) >= 2: size = pos_args[1]
        if 'size' in named: size = named['size']
        if len(pos_args) >= 3: color = pos_args[2]
        if 'color' in named: color = named['color']
        if named.get('bold') == 'true' or (len(pos_args) >= 4 and pos_args[3] == 'true'): bold = 'medium'
        n = lineno(pos)
        add('texte_tailles', f, n, re.sub(r'(?<=\d)f$', '', size), f'couleur {color} · graisse {bold}', lines[f][n - 1])
    for i, l in enumerate(lines[f], 1):
        m = re.search(r'textSize\s*=\s*([\d.]+)f', l)
        if m: add('texte_tailles', f, i, m.group(1), 'textSize direct', l)
        m = re.search(r'RelativeSizeSpan\(([\d.]+)f\)', l)
        if m: add('texte_tailles', f, i, f'×{m.group(1)}', 'RelativeSizeSpan', l)
        # graisses
        if re.search(r'typeface\s*=\s*medium|bold = true|Typeface\.BOLD|sans-serif-medium', l):
            add('graisses', f, i, 'BOLD' if 'Typeface.BOLD' in l else 'medium (500)', '', l)
        # interlignage
        m = re.search(r'setLineSpacing\(([^)]*)\)', l)
        if m: add('interlignes', f, i, m.group(1), '', l)
        # couleurs littérales
        for m in re.finditer(r'0x([0-9A-Fa-f]{8})', l):
            v = m.group(1).upper()
            if v in ('00FFFFFF', 'FF000000') and ('and' in l or 'or' in l) and 'setColor' not in l: role = 'masque binaire'
            else: role = ''
            add('couleurs', f, i, '#' + v, role, l)
        for m in re.finditer(r'Color\.(TRANSPARENT|WHITE|BLACK)', l):
            add('couleurs', f, i, m.group(0), '', l)
        # opacités
        for m in re.finditer(r'ink\(([\d.]+)\)', l):
            add('opacites', f, i, m.group(1), 'ink()', l)
        for m in re.finditer(r'mass\([^)]*?,\s*([\d.]+)\)', l):
            add('opacites', f, i, m.group(1), 'mass() fond', l)
        for m in re.finditer(r'alpha\s*=\s*if[^\n]*?([\d.]+)f', l):
            add('opacites', f, i, m.group(1), 'View.alpha', l)
        for m in re.finditer(r'or 0x([0-9A-F]{2})000000', l):
            add('opacites', f, i, f'{int(m.group(1),16)/255:.3f}', 'alpha composé sur une couleur', l)
        # tailles en dp
        for m in re.finditer(r'dp\(([\d.]+)\)', l):
            v = m.group(1)
            role = 'autre'
            if re.search(r'setPadding|padding', l): role = 'marge interne (padding)'
            elif re.search(r'Margin|margin|setMargins', l): role = 'marge externe (margin)'
            elif re.search(r'LayoutParams', l): role = 'taille (LayoutParams)'
            elif re.search(r'minimum|minHeight|minWidth', l): role = 'taille minimale'
            elif re.search(r'cornerRadius|radius', l): role = 'rayon'
            elif re.search(r'elevation', l): role = 'élévation'
            add('dp', f, i, v, role, l)
        # rayons
        for m in re.finditer(r'\b(mass|flat)\(([^,)]*)', l):
            if 'fun ' in l: continue
            v = m.group(2).strip() or '12 (défaut flat)'
            add('rayons', f, i, v, m.group(1) + '()', l)
        for m in re.finditer(r'cornerRadius\s*=\s*([^\n;]+)', l):
            add('rayons', f, i, m.group(1).strip(), 'cornerRadius', l)
        # icônes
        for m in re.finditer(r'(?:R\.drawable|android\.R\.drawable)\.(\w+)', l):
            add('icones', f, i, m.group(0).replace('R.drawable.', ''), '', l)
        for m in re.finditer(r'R\.mipmap\.(\w+)', l):
            add('icones', f, i, 'mipmap/' + m.group(1), '', l)
        # élévation
        m = re.search(r'elevation\s*=\s*([^\n]+)', l)
        if m: add('elevations', f, i, m.group(1).strip(), '', l)
        # textes visibles
        if re.search(r'Link\.log|\.log\(|Log\.|getString\(|optString|put\("|getInt\(|getLong\(|getBoolean\(|getSharedPreferences|putExtra|setAction|Intent\(|createNotificationChannel\(NotificationChannel\("|startsWith|endsWith|contains\("|Regex|split\(|"%|SimpleDateFormat|replace\(', l) and not re.search(r'setTitle|setMessage|Button\(|text\s*=|hint\s*=|label\(|setContentTitle|setContentText|Toast|footRow|chevronRow|tool\(|iconButton\(|menu\.add|Triple\(|to "|-> "', l):
            continue
        for m in re.finditer(r'"((?:[^"\\]|\\.)*)"', l):
            s = m.group(1)
            if not re.search(r'[A-Za-zÀ-ÿ]', s): continue
            if re.fullmatch(r'[a-z0-9_.\-/:]+', s): continue
            if re.fullmatch(r'[A-Za-z_]+', s) and s[0].islower(): continue
            if s.startswith('android.') or 'sans-serif' in s or s.startswith('fyi.'): continue
            if re.search(r"CalendarContract|\$\{android|SELECT|AND |content://", l + s): continue
            if re.search(r'@Suppress|Hmac|SHA|Digest|Cipher|MissingPermission|DEPRECATION|UTF-8|application/|\$id\.|\.json|\.wav|\.m4a|\.opus', l + s): continue
            if s in ('\\n', '\\n\\n', ' else ', ' ', ', ', ' · ') or s.strip() in ('·', ''): continue
            if not (' ' in s or re.search(r'[À-ÿ]', s) or (s[0].isupper() and len(s) > 1)): continue
            if 'Link.log' in l or 'log(' in l: continue
            add('textes', f, i, s, '', l)

# Drawables
for x in sorted(glob.glob(ROOT + '/res/drawable/*.xml')):
    t = open(x).read()
    name = os.path.basename(x)[:-4]
    vw = re.search(r'viewportWidth="([\d.]+)"', t); w = re.search(r'android:width="([\d.]+)dp"', t)
    strokes = re.findall(r'strokeWidth="([\d.]+)"', t)
    fills = re.findall(r'fillColor="(#[0-9A-Fa-f]+)"', t); scol = re.findall(r'strokeColor="(#[0-9A-Fa-f]+)"', t)
    caps = re.findall(r'strokeLineCap="(\w+)"', t); joins = re.findall(r'strokeLineJoin="(\w+)"', t)
    nums = [float(v) for v in re.findall(r'-?\d+\.?\d*', ' '.join(re.findall(r'pathData="([^"]+)"', t)))]
    rows['drawables'].append({'fichier': rel(x), 'ligne': 1, 'valeur': name,
        'role': f"{w.group(1) if w else '?'} dp, viewport {vw.group(1) if vw else '?'}, trait {'/'.join(sorted(set(strokes))) or '—'}, remplissage {'/'.join(sorted(set(fills))) or '—'}, couleur trait {'/'.join(sorted(set(scol))) or '—'}, bouts {'/'.join(sorted(set(caps))) or 'butt (défaut)'}, angles {'/'.join(sorted(set(joins))) or 'miter (défaut)'}",
        'contexte': ''})

FIELDS = ['fichier', 'ligne', 'valeur', 'role', 'contexte']
summary = {}
for kind, rs in rows.items():
    with open(f'{OUT}/inventaire-{kind}.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, FIELDS); w.writeheader(); w.writerows(rs)
    c = collections.Counter(r['valeur'] for r in rs)
    summary[kind] = {'occurrences': len(rs), 'valeurs': len(c), 'comptes': c.most_common()}
json.dump(summary, open(f'{OUT}/inventaire-resume.json', 'w'), ensure_ascii=False, indent=1)
for k, v in summary.items():
    print(k, v['occurrences'], v['valeurs'], v['comptes'][:25])
