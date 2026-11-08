from commun import *
import re, collections

MDC = 'https://github.com/material-components/material-components-android/blob/master/'

TYPE = [
    # jeton, rôle M3, taille, graisse, interligne, usages
    ('Type.label', 'Label Medium', 12, 500, 16, 'Mots de la barre du bas, lettres des jours'),
    ('Type.small', 'Body Small', 12, 400, 16, 'Temps du lecteur'),
    ('Type.body', 'Body Medium', 14, 400, 20, 'Méta d\'une ligne, détail de l\'en-tête, heures des répliques, explications, valeurs des Réglages'),
    ('Type.bodyStrong', 'Title Small / Label Large', 14, 500, 20, 'Titres de jour et de groupe, nom d\'une réplique, initiales, bouton texte'),
    ('Type.bodyLarge', 'Body Large', 16, 400, 24, 'Titre d\'une ligne, répliques, champs, lignes du pied et des Réglages, états vides, chiffres du calendrier'),
    ('Type.title', 'Title Medium', 16, 500, 24, 'Titre d\'un écran (barre), mois du calendrier, bouton plein'),
    ('Type.headline', 'Headline Small', 24, 400, 32, 'Titre de la mise en route'),
]

# Couleurs : (jeton, clair, sombre, rôle, fond de contrôle)
COLORS = [
    ('background', '#FFF5F5F5', '#FF1E1E1E', 'Fond de page', None),
    ('text', '#FF1D1D1F', '#FFF5F5F7', 'Texte', 'page'),
    ('secondary', '#99000000', '#B3FFFFFF', 'Texte discret, icônes secondaires, chevrons (60 % ; 70 % en sombre)', 'page'),
    ('neutral', '#73000000', '#73FFFFFF', 'Points du calendrier (45 %)', 'page'),
    ('card', '#0D000000', '#0DFFFFFF', 'Carte (5 %)', None),
    ('button', '#12000000', '#12FFFFFF', 'Bouton, vignette (7 %)', None),
    ('touch', '#1F000000', '#1FFFFFFF', 'Toucher, piste (12 %)', None),
    ('floating', '#F0FFFFFF', '#F02C2C2E', 'Ce qui flotte (barre du bas, pastille)', None),
    ('accent', '#FF0064D2', '#FF409CFF', 'Accent (dynamique dès l\'API 31, voir P18)', 'page'),
    ('onAccent', '#FFFFFFFF', '#FF1E1E1E', 'Texte sur l\'accent plein', 'accent'),
    ('me', '#FF0058C0', '#FF7AB8FF', '« Moi »', 'page'),
    ('them', '#FF8A3D06', '#FFFFC79A', 'La personne en face (valeurs du Mac)', 'page'),
    ('voice1', '#FF16692E', '#FF4CD474', 'Voix 1 (vert)', 'avatar'),
    ('voice2', '#FF7E35B0', '#FFD0A8FF', 'Voix 2 (violet)', 'avatar'),
    ('voice3', '#FFA61F55', '#FFFF9EC2', 'Voix 3 (rose)', 'avatar'),
    ('voice4', '#FF066570', '#FF5CCFDC', 'Voix 4 (sarcelle)', 'avatar'),
    ('voice5', '#FF4A4AC8', '#FFB0B3FF', 'Voix 5 (indigo)', 'avatar'),
    ('live', '#FFC41E14', '#FFFF453A', 'En cours, Arrêter, point des appels', 'page'),
    ('warning', '#FFA0470A', '#FFFF9F0A', 'Ce qui empêche quelque chose', 'card'),
    ('ok', '#FF147333', '#FF32D74B', 'Fait, prêt', 'page'),
    ('whatsapp', '#FF0F8A4B', '#FF25D366', 'Vignette WhatsApp', 'button'),
    ('signal', '#FF3B45FD', '#FF8E95FF', 'Vignette Signal', 'button'),
    ('telegram', '#FF1C7FB8', '#FF26A5E4', 'Vignette Telegram', 'button'),
    ('meet', '#FF00897B', '#FF2BB3A6', 'Vignette Meet', 'button'),
]

def contrast_of(fg, mode, kind):
    page_ = '#FFF5F5F5' if mode == 'clair' else '#FF1E1E1E'
    if kind is None: return ''
    if kind == 'page': bg = None
    elif kind == 'card': bg = '#0D000000' if mode == 'clair' else '#0DFFFFFF'
    elif kind == 'button': bg = '#12000000' if mode == 'clair' else '#12FFFFFF'
    elif kind == 'accent': bg = '#FF0064D2' if mode == 'clair' else '#FF409CFF'
    elif kind == 'avatar': bg = ('#1F' if mode == 'clair' else '#33') + fg[3:]
    t, b, r, l = ratio(fg, bg, page_)
    return f'{fr(r)}:1 · Lc {fr(l, 0)}'

SCALE = [4, 6, 8, 10, 12, 16, 20, 24, 32]

def map_size(f, line, v, ctx):
    f = short(f).split('/')[-1]
    key = f'{f}:{line}'
    special = {
        'ConversationScreen.kt:56': ('17', 'Type.title (16, 500)'), 'SettingsScreen.kt:125': ('17', 'Type.title (16, 500)'),
        'SetupScreen.kt:16': ('17 medium', 'Type.headline (24, 400)'),
        'ConversationScreen.kt:61': ('15', 'Type.bodyLarge (16)'), 'ConversationScreen.kt:324': ('15 medium', 'Type.bodyStrong (14, 500)'),
        'Screen.kt:147': ('15', 'Type.body (14)'), 'HomeScreen.kt:316': ('15', 'Type.bodyLarge (16), chiffres tnum'),
        'SetupScreen.kt:17': ('15', 'Type.body (14)'),
        'ConversationScreen.kt:57': ('13', 'Type.body (14)'), 'ConversationScreen.kt:320': ('13 medium', 'Type.bodyStrong (14, 500)'),
        'ConversationScreen.kt:325': ('13', 'Type.body (14), secondary, tnum'), 'SettingsScreen.kt:87': ('13', 'Type.body (14)'),
        'ConversationScreen.kt:98': ('12', 'Type.small (12), tnum'), 'ConversationScreen.kt:178': ('12', 'Type.label (12, 500)'),
        'HomeScreen.kt:289': ('12', 'Type.label (12, 500)'), 'SettingsScreen.kt:58': ('14 medium', 'Type.bodyStrong (14, 500)'), 'HomeScreen.kt:284': ('16 medium', 'Type.title (16, 500)'),
    }
    if key in special: return special[key]
    m = {'16': 'Type.bodyLarge (16)', '16 (défaut)': 'Type.bodyLarge (16)', '14': 'Type.body (14)' if 'bold' not in ctx and 'medium' not in ctx else 'Type.bodyStrong (14, 500)',
         '×0.875': 'Type.body (14)', '17': 'Type.title (16, 500)', '15': 'Type.body (14)', '13': 'Type.body (14)', '12': 'Type.label (12, 500)'}
    return (v, m.get(v, '?'))

def build():
    b = ['<h1>Système et migration</h1><p class="lede">Une proposition de système unifié pour l\'app Android : échelle de texte, couleurs, espacements, rayons, élévation, icônes et composants, puis la table de migration « valeur actuelle → nouvelle », fichier par fichier et ligne par ligne. Le système reprend la règle de DESIGN.md (« une seule valeur par rôle ») et les rôles de Material 3, en gardant les masses en opacités du Mac.</p>']
    b.append('''<h2 id="principes">Principes</h2><div class="card"><ul>
<li><b>Une valeur par rôle</b>, dans <code>Look.kt</code> ; les écrans n'écrivent plus de nombre (aujourd'hui : 31 tailles de texte, 175 valeurs en dp, 24 couleurs écrites dans les écrans).</li>
<li><b>Les rôles de texte de Material 3</b>, pour que l'app parle la langue d'un Pixel, aux tailles qu'Android donne (<a href="''' + MDC + '''docs/theming/Typography.md">Typography.md</a>).</li>
<li><b>Les masses en opacités du texte</b>, comme sur le Mac : c'est l'identité de l'app, pas un écart à corriger.</li>
<li><b>L'échelle d'espacement du Mac</b> (4, 6, 8, 10, 12, 16, 20, 24), plus 32 : une seule échelle pour les deux apps.</li>
<li><b>Sans androidx ni Material Components</b> : l'app n'en dépend pas (<code>MainActivity.kt:160</code>). Le système est fait de constantes et de fonctions de <code>Look</code> et <code>Screen</code>, pas de thèmes XML.</li></ul></div>''')
    b.append('<h2 id="type">Texte</h2><p>Six tailles aujourd\'hui (12, 13, 14, 15, 16, 17) et un × 0,875 ; quatre demain (12, 14, 16, 24), deux graisses (400, 500). Le seul gras 700 (aujourd\'hui dans le calendrier) disparaît.</p>')
    b.append(table(['Jeton', 'Rôle Material 3', 'Taille (sp)', 'Graisse', 'Interligne (sp)', 'Usages'],
        [[f'<code>{t}</code>', r, s, w, lh, u] for t, r, s, w, lh, u in TYPE], num=(2, 3, 4)))
    b.append('<div class="card" style="font-family:Roboto,system-ui,sans-serif">' + ''.join(
        f'<div style="font-size:{s}px;line-height:{lh}px;font-weight:{w};margin:6px 0">{r} · {s}/{lh} · {w} — Point produit, 23:57 · 47 min</div>' for t, r, s, w, lh, u in TYPE) + '</div>')
    b.append('<h2 id="couleurs">Couleurs</h2><p>Contrastes calculés sur le fond où chaque couleur sert (page, carte, vignette, rond à initiales ou accent plein). Les ronds à initiales prennent leur couleur à 12 % en clair, 20 % en sombre.</p>')
    b.append(table(['Jeton', 'Clair', 'Contraste clair', 'Sombre', 'Contraste sombre', 'Rôle'],
        [[f'<code>{t}</code>', sw('#' + c[3:]) + c + ('' if c[1:3] == 'FF' else f' ({round(int(c[1:3], 16) / 2.55)} %)'), contrast_of(c, 'clair', k),
          sw('#' + d[3:]) + d + ('' if d[1:3] == 'FF' else f' ({round(int(d[1:3], 16) / 2.55)} %)'), contrast_of(d, 'sombre', k), r] for t, c, d, r, k in COLORS]))
    b.append('<p>Changements par rapport à aujourd\'hui : <code>secondary</code> sombre 62 → 70 % (P07) ; <code>title</code> fondu dans <code>secondary</code> ; <code>accent</code> sombre <code>#409CFF</code> (P02) ; <code>me</code>, <code>them</code> et les voix (P01) ; les logos par mode (P14) ; le rouge du point des appels devient <code>live</code> (P19) ; l\'heure à 50 % et le chevron à 16 % disparaissent. Note pour le Mac : <code>TranscriptReaderView.me</code> (<code>#0060DF</code>) sur son rond à 14 % donne 4,20:1 pour des initiales de 12 pt, sous 4,5:1 ; la même correction s\'y appliquerait.</p>')
    b.append('''<h2 id="espaces">Espacements, rayons, élévation, icônes</h2>
<div class="grid2"><div class="card"><h3>Espacements (dp)</h3><p><b>4, 6, 8, 10, 12, 16, 20, 24, 32</b>. Le bord de lecture est à 16 dp de l'écran ; le contenu d'une carte à 16 dp du bord de la carte. 2 et 3 deviennent 4 ; 14 devient 12 (vertical) ou 16 (horizontal).</p></div>
<div class="card"><h3>Rayons (dp)</h3><p><b>8</b> (ligne, vignette, à toutes les tailles), <b>12</b> (carte), <b>capsule</b> = moitié de la hauteur (bouton rond, champ, barre du bas, pastille, rond à initiales). La barre du bas a aujourd'hui un rayon de 24 pour 64 dp de haut : ce n'est pas une capsule ; la pastille, 24 pour 48, en est une.</p></div>
<div class="card"><h3>Élévation</h3><p><b>6 dp</b> pour tout ce qui flotte (barre du bas, pastille), au lieu de 6 et 4.</p></div>
<div class="card"><h3>Icônes</h3><p>Grille de 24, <b>trait de 2</b>, bouts et angles ronds. <b>24 dp</b> dans les boutons d'icône (48 × 48) et la barre du bas, <b>20 dp</b> dans les vignettes de 44, <b>18 dp</b> dans celles de 36, <b>16 dp</b> pour le chevron. Aujourd'hui : 16, 18, 20, 22 et 24.</p></div></div>''')
    b.append('<h2 id="composants">Composants</h2>')
    b.append(table(['Composant', 'Forme', 'Texte', 'Couleurs', 'États'], [
        ['Barre d\'un écran (<code>bar</code>)', 'hauteur min 64, Retour 48, vignette 36 (rayon 8)', 'titre <code>Type.title</code>, détail <code>Type.body</code> (« +n » pour les noms)', 'text, secondary ; « ● En cours » en live', 'en direct, Journal, sans vignette'],
        ['Ligne de conversation', 'min 64, padding 8, vignette 44 (rayon 8, icône 20)', 'titre <code>bodyLarge</code>, méta <code>body</code> tnum', 'vignette button ; en cours : live 12 % ; Journal : accent 12 %', 'repos, toucher, en cours, Journal, résultat de recherche'],
        ['Titre de jour, de groupe', 'padding 16 / 12 / 16 / 6', '<code>bodyStrong</code>, secondary', '—', 'titre pour TalkBack'],
        ['Réplique', 'rond capsule ≥ 36, texte à 64 dp du bord', 'nom <code>bodyStrong</code>, heure <code>body</code> secondary tnum, texte <code>bodyLarge</code> × 1,15', 'me, them, voix 1-5 ; fond 12 / 20 %', 'du Mac, du téléphone (rond invisible), en attente (secondary)'],
        ['Lecteur', 'carte 12, Lire 48 (capsule), piste 48 au doigt', 'temps <code>small</code> tnum', 'accent, touch', 'lecture, pause, fin'],
        ['Barre du bas', 'capsule, élévation 6, outils ≥ 76 × 56', 'mot <code>label</code> (masqué au-delà de 130 %)', 'floating, text', 'outils présents seulement s\'ils servent'],
        ['Carte des Réglages', 'rayon 12, contenu à 16', '<code>bodyLarge</code> + explication <code>body</code>', 'card ; avertissement en warning', 'choisi, manque de calendrier'],
        ['Ligne à chevron', 'min 48, padding 16 / 12', 'nom <code>bodyLarge</code>, valeur <code>body</code>', 'chevron secondary', 'valeur en warning si elle alerte'],
        ['Jour du calendrier', '48 × 48, capsule', '<code>bodyLarge</code> tnum', 'aujourd\'hui : anneau accent ; choisi : disque accent, onAccent', 'avec conversations : point neutral'],
        ['Bouton plein', 'capsule, 48', '<code>title</code> blanc', 'accent / onAccent', 'appui'],
        ['Pastille', 'capsule, 48, élévation 6', '—', 'floating ; Arrêter en live', 'déplacée'],
        ['Notification', 'Android', 'titre « Enregistre », chronomètre', 'accent', 'Prêt, Écoute, Enregistre, arrêt'],
    ]))
    # migration
    b.append('<h2 id="migration">Table de migration</h2><p>Générée depuis l\'inventaire : chaque ligne du code qui porte une valeur hors système, avec sa nouvelle valeur. Les lignes déjà conformes (16 sp de texte courant, espacements de l\'échelle) n\'y sont pas.</p>')
    mig = []
    for r in rows('inventaire-texte_tailles'):
        old, new = map_size(r['fichier'], r['ligne'], r['valeur'], r['role'] + r['contexte'])
        if new.startswith('Type.bodyLarge (16)') and old.startswith('16'): continue
        if new.startswith('Type.body (14)') and old == '14' and 'medium' not in r['role']: continue
        mig.append((short(r['fichier']), int(r['ligne']), 'texte', f'{old} sp', new))
    colmap = {'#FFD32F2F': 'look.live (P19)', '#FF25D366': 'look.whatsapp (P14)', '#FF3B45FD': 'look.signal (P14)', '#FF26A5E4': 'look.telegram (P14)', '#FF00897B': 'look.meet (P14)',
              '#FF0064D2': 'Look.accent ; ACCENT ne reste que pour la notification (P02)', '#1F000000': 'look.avatarFill(c) : 12 % / 20 % (P01)', '#FF409CFF': 'Look.accent sombre'}
    for r in rows('inventaire-couleurs'):
        if r['valeur'] in colmap and 'Look.kt' not in r['fichier']:
            mig.append((short(r['fichier']), int(r['ligne']), 'couleur', r['valeur'], colmap[r['valeur']]))
    for r in rows('inventaire-opacites'):
        v = r['valeur']; f = short(r['fichier'])
        new = {'0.5': 'secondary (P07)', '0.4': 'secondary (chevron, P13) / supprimé (outils inactifs, P22)', '0.55': 'secondary', '0.56': 'secondary', '0.62': 'secondary sombre 0,70', '0.122': 'avatarFill (P01)'}.get(v)
        if new: mig.append((f, int(r['ligne']), 'opacité', v, new))
    for r in rows('inventaire-dp'):
        v = float(r['valeur'])
        if r['role'] in ('marge interne (padding)', 'marge externe (margin)') and v not in SCALE and v not in (0,):
            new = {2: '4', 3: '4', 14: '12 (vertical) ou 16 (horizontal)', 18: '16', 22: '24', 26: '24'}.get(int(v), '?')
            mig.append((short(r['fichier']), int(r['ligne']), 'espacement', f'{r["valeur"]} dp', new))
    for r in rows('inventaire-rayons'):
        v = r['valeur']
        new = {'18': 'capsule (h/2)', '20': 'capsule (h/2) : 28 pour un outil de 56', '22': 'capsule : 24 (Lire 48, P04)', '26': 'capsule (h/2) : déjà 26 pour 52', 'size / 5.5': '8 à toutes les tailles'}.get(v)
        if r['fichier'].endswith('ConversationScreen.kt') and r['ligne'] == '130': new = 'capsule : 32 pour 64 dp de haut'
        if new: mig.append((short(r['fichier']), int(r['ligne']), 'rayon', v, new))
    for r in rows('inventaire-elevations'):
        if '4' in r['valeur']: mig.append((short(r['fichier']), int(r['ligne']), 'élévation', '4 dp', '6 dp'))
    for r in rows('inventaire-drawables'):
        m = re.search(r'trait ([\d./]+)', r['role'])
        if m and m.group(1) not in ('2', '—'): mig.append((short(r['fichier']), 1, 'trait', m.group(1), '2'))
    mig.sort()
    byfile = collections.OrderedDict()
    for f, l, k, o, n in mig: byfile.setdefault(f, []).append((l, k, o, n))
    b.append(f'<p><b>{len(mig)}</b> changements dans <b>{len(byfile)}</b> fichiers.</p>')
    for f, items in byfile.items():
        b.append(f'<h3>{esc(f)} · {len(items)}</h3>' + table(['Ligne', 'Nature', 'Actuel', 'Nouveau'], [[src(f if f.startswith('res') is False else f, l) if not f.startswith('res/') else src('phone/android/app/src/main/' + f), k, f'<code>{esc(o)}</code>', esc(n)] for l, k, o, n in items]))
    page('systeme.html', 'Système et migration', '\n'.join(b))
    return len(mig)

if __name__ == '__main__':
    print(build())
