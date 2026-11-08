from commun import *

def S(f, l=None): return src(f, l)
MDC = 'https://github.com/material-components/material-components-android/blob/master/'

# Chaque problème : id, titre, gravité, effort, lot, symptôme, preuve, cause, impact, options [(titre, pour, contre, choisi)], choix, refs, spec [(fichier:ligne, avant, après)], criteres, conflit
P = []

P.append(dict(id='P01', titre='Les voix d\'une réunion ont toutes la même couleur', grav='gêne', effort='2 h', lot='L2',
 symptome='Dans une réunion enregistrée par le téléphone, « Voix 1 » et « Voix 2 » ont le même rond orange (<code>#A0470A</code> à 12 %) et le même nom noir. Pour suivre qui répond à qui, il faut lire « V1 » ou « V2 » dans un rond de 36 dp.',
 preuve='<figure><img src="images/p01-voix-meme-couleur.webp" alt="Réunion : V1 et V2 dans le même orange"><figcaption>Banc, <code>site-reunion</code>, clair. Bleu : Moi. Orange : toutes les autres voix.</figcaption></figure>'
        '<p>Le Mac donne une teinte par voix de la pièce (<code>TranscriptReader.swift:1313</code> : vert, violet, rose, sarcelle, indigo) et écrit son numéro seul (« 1 », « 2 ») dans le rond (<code>:1324</code>). Le fond du rond y est à 14 % en clair, 24 % en sombre ; Android met 12 % (<code>0x1F</code>) dans les deux modes.</p>',
 cause=S('ConversationScreen.kt', 347) + ' : <code>if (l.me) Tone.INFO else Tone.WARNING</code> ; ' + S('ConversationScreen.kt', 355) + ' fond <code>0x1F</code> ; ' + S('ConversationScreen.kt', 314) + ' initiales « V1 ».',
 impact='Chaque réunion en salle enregistrée par le téléphone (mode Tout le temps ou Événements du calendrier), sur toutes ses répliques. Les réunions du Mac reçues au téléphone ont souvent des noms : elles gardent l\'orange, comme sur le Mac.',
 options=[('A. Ne rien changer', 'Rien à coder ; l\'orange dit « quelqu\'un d\'autre ».', 'Le téléphone montre moins que le Mac pour la même conversation ; les voix se confondent.', False),
          ('B. Les teintes du Mac pour « Voix N », son numéro seul', 'Même lecture que sur le Mac ; aucune règle nouvelle ; chiffres plus lisibles que « V1 ».', 'Cinq couleurs de plus à tenir accessibles en clair et en sombre.', True),
          ('C. Une teinte pour chaque autre personne, nommée ou non', 'Distingue aussi Sophie et Karim.', 'Va plus loin que le Mac, qui garde l\'orange pour les personnes nommées : les deux apps divergeraient.', False)],
 choix='B. Le téléphone ressemble au Mac (DESIGN.md › Téléphone), et le Mac a déjà tranché ce cas. Les teintes du Mac (<code>.green</code>, <code>.purple</code>…) sont des couleurs système trop claires pour du texte de 13 sp sur un fond de 12 % : elles sont foncées en clair et éclaircies en sombre jusqu\'à 5:1 au moins (voir <a href="systeme.html#couleurs">Système › Couleurs</a>).',
 refs='WCAG 2.2 › 1.4.1 Use of Color (la couleur double le numéro, elle ne le remplace pas) et 1.4.3 (4,5:1 pour les initiales). Mac : <code>TranscriptReader.swift:1310-1342</code>.',
 spec=[('Look.kt (nouveau, après la ligne 25)', '—', 'val me = if (dark) 0xFF7AB8FF.toInt() else 0xFF0058C0.toInt()\nval them = if (dark) 0xFFFFC79A.toInt() else 0xFF8A3D06.toInt()\nval voices = if (dark) intArrayOf(0xFF4CD474.toInt(), 0xFFD0A8FF.toInt(), 0xFFFF9EC2.toInt(), 0xFF5CCFDC.toInt(), 0xFFB0B3FF.toInt())\n    else intArrayOf(0xFF16692E.toInt(), 0xFF7E35B0.toInt(), 0xFFA61F55.toInt(), 0xFF066570.toInt(), 0xFF4A4AC8.toInt())\n/** Le fond d\'un rond à initiales : 12 % en clair, 20 % en sombre. */\nfun avatarFill(c: Int) = (c and 0x00FFFFFF) or ((if (dark) 0x33 else 0x1F) shl 24)'),
       ('ConversationScreen.kt:347', 'val color = if (l.me) Look.Tone.INFO.color(look) else Look.Tone.WARNING.color(look)', 'val voice = l.who.removePrefix("Voix ").toIntOrNull()?.takeIf { l.who.startsWith("Voix ") }\nval color = when { l.me -> look.me; voice != null -> look.voices[(voice - 1) % look.voices.size]; else -> look.them }'),
       ('ConversationScreen.kt:353', 'h.mark.text = initials(l.who)', 'h.mark.text = voice?.toString() ?: initials(l.who)'),
       ('ConversationScreen.kt:355', 'h.mark.background = look.mass(18, color = (color and 0x00FFFFFF) or 0x1F000000)', 'h.mark.background = look.mass(18, color = look.avatarFill(color))')],
 criteres=['Banc <code>site-reunion</code> : les ronds de Voix 1 et Voix 2 ont deux teintes différentes ; le rond affiche « 1 » et « 2 ».', 'Relevé : chaque initiale à 4,5:1 au moins sur son rond, en clair et en sombre.', 'Une conversation avec Sophie et Karim garde l\'orange <code>them</code> pour les deux, comme sur le Mac.']))

P.append(dict(id='P02', titre='En sombre, le bleu de l\'app reste celui du clair', grav='gêne', effort='45 min', lot='L1',
 symptome='En sombre, « ● Écoute depuis 08:12 », « Relier un calendrier », le chiffre d\'aujourd\'hui, les ronds des modes, le curseur et l\'onde du Journal restent en <code>#0064D2</code>, un bleu fait pour le fond clair.',
 preuve='<div class="grid2"><figure><img src="images/p02-sombre-ecoute.webp" alt="Journal en sombre"><figcaption>« ● Écoute depuis » : 2,98:1, APCA Lc 22,8.</figcaption></figure><figure><img src="images/p02-sombre-relier.webp" alt="Relier un calendrier en sombre"><figcaption>« Relier un calendrier » : 2,61:1 sur la carte.</figcaption></figure></div>'
        '<p>Mesures en sombre : aujourd\'hui sur le jour choisi 2,08:1 ; ronds des modes et curseur 2,58:1 (non-texte, seuil 3:1) ; onde du Journal 2,72:1. La variante sombre existe déjà : <code>Tone.INFO</code> vaut <code>#409CFF</code> en sombre (5,89:1 sur la page).</p>',
 cause='<code>LinkService.ACCENT</code> est une constante, utilisée 14 fois hors de sa définition : ' + ', '.join(S(f, l) for f, l in [('HomeScreen.kt', 242), ('HomeScreen.kt', 253), ('HomeScreen.kt', 316), ('SettingsScreen.kt', 38), ('SettingsScreen.kt', 62), ('ConversationScreen.kt', 87), ('ConversationScreen.kt', 88)]) + '.',
 impact='Toute personne en thème sombre : l\'écoute, état le plus important de l\'accueil en mode Tout le temps, s\'y lit à 2,98:1.',
 options=[('A. Remplacer chaque usage texte ou trait par Tone.INFO', 'Rien de nouveau ; 7 lignes.', 'INFO garde deux rôles (accent et information).', False),
          ('B. Un jeton Look.accent, clair et sombre, pour tout ce qui est accent', 'Une valeur par rôle (DESIGN.md) ; prépare la couleur dynamique (P18).', 'Un jeton de plus.', True)],
 choix='B : <code>Look.accent</code> = <code>#0064D2</code> en clair, <code>#409CFF</code> en sombre. <code>LinkService.ACCENT</code> ne sert plus qu\'à la notification, qu\'Android teinte lui-même, et aux fonds pleins sous du blanc (Lire, Scanner le code du Mac : blanc sur <code>#0064D2</code> = 5,59:1).',
 refs='WCAG 2.2 › 1.4.3 Contrast (Minimum) et 1.4.11 Non-text Contrast.',
 spec=[('Look.kt (après la ligne 25)', '—', 'val accent = if (dark) 0xFF409CFF.toInt() else LinkService.ACCENT'),
       ('HomeScreen.kt:242', 'tint = LinkService.ACCENT, plate = accentPlate(), metaColor = LinkService.ACCENT', 'tint = look.accent, plate = accentPlate(), metaColor = look.accent'),
       ('HomeScreen.kt:253', 'setColor((LinkService.ACCENT and 0x00FFFFFF) or 0x1F000000)', 'setColor((look.accent and 0x00FFFFFF) or (if (look.dark) 0x33000000 else 0x1F000000))'),
       ('HomeScreen.kt:316', 'if (today) LinkService.ACCENT else look.text', 'voir P12'),
       ('SettingsScreen.kt:38', 'buttonTintList = ColorStateList.valueOf(LinkService.ACCENT)', 'buttonTintList = ColorStateList.valueOf(look.accent)'),
       ('SettingsScreen.kt:62', 'setTextColor(LinkService.ACCENT)', 'setTextColor(look.accent)'),
       ('ConversationScreen.kt:87-88', 'ColorStateList.valueOf(LinkService.ACCENT)', 'ColorStateList.valueOf(look.accent)')],
 criteres=['Relevé sombre : aucun texte ni trait en <code>#0064D2</code> ; textes ≥ 4,5:1, traits ≥ 3:1.', '<code>grep -n "LinkService.ACCENT" *.kt</code> ne renvoie plus que LinkService.kt (notifications), ConversationScreen.kt (fond de Lire) et SetupScreen.kt (fond du bouton).']))

P.append(dict(id='P03', titre='À 200 % de texte, la barre du bas, l\'en-tête et les ronds se coupent', grav='gêne', effort='3 h', lot='L2',
 symptome='Avec la taille de police au maximum (200 % depuis Android 14), les quatre mots de la barre du bas se touchent et débordent de la capsule, la ligne de détail de l\'en-tête est coupée par le bas, « SM » devient « S » dans son rond, l\'indice « Rechercher dans la conversa » est tronqué sans « … ».',
 preuve='<div class="grid2"><figure><img src="images/p18-200-barre.webp" alt="Barre du bas à 200 %"><figcaption>Texte 200 % : « RechercherCopierTéléchargerDétails ».</figcaption></figure><figure><img src="images/p18-200-entete.webp" alt="En-tête à 200 %"><figcaption>Texte 200 % : détail coupé, initiales coupées.</figcaption></figure></div><p>Relevé : 38 textes coupés par « … » à 200 %, contre 4 à 100 %.</p>',
 cause='Hauteurs fixes en dp autour de textes en sp : ' + S('ConversationScreen.kt', 145) + ' (barre, 64 dp), ' + S('SettingsScreen.kt', 125) + ', ' + S('HomeScreen.kt', 102) + ' ; ' + S('ConversationScreen.kt', 331) + ' (rond 36 × 36) ; outils de largeur libre mais mot sur une ligne, ' + S('ConversationScreen.kt', 178) + '.',
 impact='Les personnes qui grossissent le texte, nombreuses sur téléphone ; à 150 % déjà, la barre du bas touche les bords sur un écran de 360 dp.',
 options=[('A. Laisser grandir : hauteurs minimales au lieu de fixes, rond qui suit son texte', 'Rien ne se coupe ; les écrans restent les mêmes à 100 %.', 'La barre du bas ne tient toujours pas : quatre mots à 24 sp ne passent pas dans 360 dp.', False),
          ('B. A, et la barre du bas en icônes seules au-delà de 130 %', 'Tout tient ; les noms restent dits par TalkBack et par un appui long (<code>tooltipText</code>) ; c\'est la forme de la barre d\'outils flottante de Material 3 (icônes seules).', 'Les mots disparaissent pour ceux qui en ont le plus besoin.', True),
          ('C. A, et une barre du bas sur deux rangs', 'Garde les mots.', 'La barre couvre jusqu\'à 140 dp de texte ; dessin nouveau.', False)],
 choix='B. Les quatre icônes sont celles du Mac et d\'Android (loupe, copier, télécharger, document) ; au-delà de 130 %, le mot est ce qui empêche la barre de tenir. Le Mac montre déjà ces outils en icônes seules (<code>captures-mac-0.24.0/lecture.webp</code>).',
 refs='WCAG 2.2 › 1.4.4 Resize Text (200 % sans perte de contenu). Android 14 › Non-linear font scaling to 200%. Material Components › <a href="' + MDC + 'docs/components/FloatingToolbar.md">FloatingToolbar.md</a> (« the recommendation exists for icon buttons »).',
 spec=[('ConversationScreen.kt:145', 'LinearLayout.LayoutParams(-1, dp(64))', 'LinearLayout.LayoutParams(-1, -2)  // bar() garde minimumHeight = dp(64)'),
       ('SettingsScreen.kt:125, HomeScreen.kt:102', 'LinearLayout.LayoutParams(-1, dp(64))', 'LinearLayout.LayoutParams(-1, -2).also { /* minimumHeight 64 dans bar() / topBar */ }'),
       ('ConversationScreen.kt:331', 'addView(mark, LinearLayout.LayoutParams(dp(36), dp(36)))', 'addView(mark, LinearLayout.LayoutParams(-2, -2))\n// mark : minWidth = minHeight = dp(36), padding dp(4), rond = capsule'),
       ('ConversationScreen.kt:178', 'addView(label(text, 12f), …)', 'if (a.resources.configuration.fontScale <= 1.3f) addView(label(text, 12f), …)\ntooltipText = text'),
       ('ConversationScreen.kt:62-68 et HomeScreen.kt:69', 'EditText(a).apply { … }', 'ellipsize = TextUtils.TruncateAt.END ; minHeight = dp(48)')],
 criteres=['Relevé <code>texte200</code> : aucun texte dont la hauteur de ses lignes dépasse celle de sa vue ; la barre du bas tient dans 360 dp.', 'Image <code>texte200/conversation-recherche</code> : « SM » entier, détail de l\'en-tête entier ou coupé par « … » seulement à droite.']))

P.append(dict(id='P04', titre='Le lecteur : curseur coupé, piste de 26 dp, bouton de 44 dp', grav='gêne', effort='45 min', lot='L1',
 symptome='Au début du son, le rond du curseur est coupé en deux contre le bord gauche de la piste. La piste fait 26 dp de haut pour le doigt ; le bouton Lire, 44 dp.',
 preuve='<figure><img src="images/p03-curseur-coupe.webp" alt="Curseur coupé"><figcaption>Banc <code>conversation</code> : demi-disque à 00:00. Relevé : SeekBar 308 × 26 dp, padding 0 à gauche et à droite ; Lire 44 × 44 dp.</figcaption></figure>',
 cause=S('ConversationScreen.kt', 90) + ' : <code>setPadding(0, dp(4), 0, dp(4))</code> retire la marge où la SeekBar dessine son rond ; ' + S('ConversationScreen.kt', 105) + ' : <code>LayoutParams(dp(44), dp(44))</code>.',
 impact='Chaque conversation qui a encore son son léger (24 h et plus), à chaque ouverture : c\'est le premier objet de l\'écran.',
 options=[('A. Rendre à la SeekBar ses marges, hauteur de 48 dp', '3 lignes ; le rond entier ; la cible conforme.', 'La piste se décale de 8 dp vers la droite (aligner le temps dessous).', True),
          ('B. Slider de Material Components', 'Le composant de référence.', 'L\'app n\'a pas androidx ni Material Components (<code>MainActivity.kt:160</code>) : une dépendance pour un curseur.', False)],
 choix='A. Le bouton Lire passe à 48 dp (l\'icône reste à 16 dp), la piste garde son dessin et prend 48 dp de haut au doigt.',
 refs='Android › Make apps more accessible › Use large, simple controls (48 × 48 dp).',
 spec=[('ConversationScreen.kt:90', 'setPadding(0, dp(4), 0, dp(4))', 'setPadding(dp(8), dp(11), dp(8), dp(11))  // 26 + 22 = 48 dp'),
       ('ConversationScreen.kt:105', 'addView(playButton, LinearLayout.LayoutParams(dp(44), dp(44)))', 'addView(playButton, LinearLayout.LayoutParams(dp(48), dp(48)))'),
       ('ConversationScreen.kt:80-83 (playButton)', 'background = pressable(look.mass(22, …)) ; setPadding(dp(14) …)', 'background = pressable(look.mass(24, …)) ; setPadding(dp(16) …)'),
       ('ConversationScreen.kt:98', 'private val time = label("", 12f, look.secondary)', 'private val time = label("", 12f, look.secondary, digits = true).apply { setPadding(dp(8), 0, 0, 0) }')],
 criteres=['Image <code>conversation</code> : le rond du curseur entier à 00:00 et à la fin.', 'Relevé : SeekBar ≥ 48 dp de haut ; Lire 48 × 48 dp.']))

P.append(dict(id='P05', titre='« En cours » perd son rouge en ouvrant la conversation', grav='gêne', effort='30 min', lot='L1',
 symptome='Dans la liste, « 00:57 · ● En cours · 12 min » est rouge. En ouvrant la conversation, la même ligne passe en gris, point compris. La vignette en cours est une masse grise, quand le Journal a sa masse teintée.',
 preuve='<div class="grid2"><figure><img src="images/p04-en-cours-liste.webp" alt="En cours rouge dans la liste"><figcaption>Liste : LIVE.</figcaption></figure><figure><img src="images/p04-en-cours-gris.webp" alt="En cours gris dans l\'en-tête"><figcaption>En-tête : <code>#99000000</code>.</figcaption></figure></div>',
 cause=S('ConversationScreen.kt', 204) + ' : la ligne entière dans <code>detail</code>, de couleur secondaire ; ' + S('HomeScreen.kt', 244) + ' : <code>plate = null</code>.',
 impact='Chaque enregistrement ouvert pendant qu\'il tourne. « Ça enregistre ou non » est la première chose que l\'écran doit dire (principe tranché par Gildas).',
 options=[('A. Toute la ligne de l\'en-tête en LIVE', 'Simple.', 'L\'heure et la durée en rouge : plus de rouge que dans la liste.', False),
          ('B. Seulement « ● En cours » en LIVE, vignette teintée LIVE à 12 %', 'Exactement la forme de la liste et du Mac (<code>encours.webp</code> : le point et les mots en rouge).', 'Un Spannable.', True)],
 choix='B.', refs='DESIGN.md › Couleurs : « En cours, REC : Palette.live ». Cohérence d\'un état d\'un écran à l\'autre.',
 spec=[('ConversationScreen.kt:204', 'detail.text = listOfNotNull(Dates.hour(r.startedAt), "● En cours", …).joinToString(" · ")', 'detail.text = SpannableStringBuilder(Dates.hour(r.startedAt) + " · ").append("● En cours", ForegroundColorSpan(Look.Tone.LIVE.color(look)), 0).append(" · " + …)'),
       ('ConversationScreen.kt:202', 'paintPlate(kind, R.drawable.ic_micro, Look.Tone.LIVE.color(look))', 'paintPlate(…) ; kind.background = look.mass(8, color = look.avatarFill(Look.Tone.LIVE.color(look)))'),
       ('HomeScreen.kt:244', 'plate = null', 'plate = livePlate()  // comme accentPlate(), en LIVE')],
 criteres=['Images <code>conversation-en-direct</code> et <code>accueil-enregistre</code> : « ● En cours » de la même couleur ; vignettes teintées.']))

P.append(dict(id='P06', titre='La notification d\'enregistrement montre une barre de chargement', grav='gêne', effort='30 min', lot='L1',
 symptome='Pendant un enregistrement, la notification dit « Enregistre », « Depuis 14:02 », répète l\'heure dans son en-tête, et fait filer une barre indéterminée. L\'action « Arrêter » porte l\'icône de pause d\'Android.',
 preuve='<p>Code (le banc ne dessine pas les notifications) : ' + S('LinkService.kt', 982) + ' « Depuis … » ; ' + S('LinkService.kt', 1039) + ' <code>setWhen(cur.startedAt)</code> ; ' + S('LinkService.kt', 1042) + ' <code>setProgress(0, 0, true)</code> ; ' + S('LinkService.kt', 1045) + ' <code>android.R.drawable.ic_media_pause</code>.</p>',
 cause='Choix du commit <code>9dea502</code> (6 novembre) : « Pas de rouge : un enregistrement en cours se voit à une barre qui file sous le texte, comme un travail en tâche de fond. »',
 impact='Chaque enregistrement, dans le volet des notifications et sur l\'écran verrouillé.',
 options=[('A. Garder la barre', 'Le mouvement dit que quelque chose tourne.', 'Material : « Progress indicators express an unspecified wait time » (une attente) ; ici, rien n\'est attendu. L\'heure est dite deux fois.', False),
          ('B. Le chronomètre d\'Android à la place de la barre et de « Depuis »', 'Dit la durée qui avance, sans rouge, sans texte ; le texte de la notification disparaît.', 'Le mouvement devient un chiffre qui change chaque seconde.', True),
          ('C. Barre et chronomètre', 'Rien ne se perd.', 'Deux signaux pour un même fait.', False)],
 choix='B. <code>setUsesChronometer(true)</code> montre le champ <code>when</code> « as a stopwatch » (référence Android) : le temps écoulé, comme une durée d\'appel. On garde « jamais de rouge ». L\'icône d\'action devient <code>ic_arreter</code> : Android ne l\'affiche plus sur le téléphone depuis 7.0 (« action button icons will not be displayed »), mais la montre et la voiture, si.',
 refs='Android › <a href="https://developer.android.com/reference/android/app/Notification.Builder#setUsesChronometer(boolean)">Notification.Builder#setUsesChronometer</a> ; <a href="https://developer.android.com/reference/android/app/Notification.Action.Builder">Notification.Action.Builder</a>. Material Components › <a href="' + MDC + 'docs/components/ProgressIndicator.md">ProgressIndicator.md</a> (« express an unspecified wait time »).',
 spec=[('LinkService.kt:982', '"Enregistre" to listOfNotNull("Depuis …", test).joinToString(". ")', '"Enregistre" to (test ?: "")'),
       ('LinkService.kt:1042', 'if (busy) builder.setProgress(0, 0, true)', 'if (busy) builder.setUsesChronometer(true)'),
       ('LinkService.kt:1045', 'if (busy) android.R.drawable.ic_media_pause else R.drawable.micro_notif', 'if (busy) R.drawable.ic_arreter else R.drawable.micro_notif')],
 criteres=['Sur un téléphone : l\'en-tête de la notification compte 00:01, 00:02… ; pas de barre ; un seul rappel de l\'heure.', 'DESIGN.md › Notifications mis à jour dans le même commit.'],
 conflit='Revient sur <code>9dea502</code> (barre qui file). À trancher par Gildas ; le « jamais de rouge » est gardé.'))

P.append(dict(id='P07', titre='Trois petits textes sous 4,5:1 en clair, le secondaire faible en sombre', grav='gêne', effort='20 min', lot='L1',
 symptome='En clair : l\'heure de chaque réplique (noir à 50 %, 13 sp) est à 3,88:1 ; l\'initiale « M » de Moi à 4,31:1 sur son rond ; le chiffre d\'aujourd\'hui à 3,93:1 sur le jour choisi. En sombre, WCAG passe mais APCA met le texte secondaire (blanc à 62 %) à Lc 54, sous Lc 60.',
 preuve='<figure><img src="images/p06-heures.webp" alt="Heures des répliques"><figcaption>Heures des répliques : <code>#7F000000</code>, 3,88:1.</figcaption></figure><p>Mesures complètes : <a href="mesures.html#textes">Mesures › Contrastes des textes</a>.</p>',
 cause=S('ConversationScreen.kt', 325) + ' <code>look.ink(0.5)</code> ; ' + S('Look.kt', 22) + ' et ' + S('Look.kt', 23) + ' <code>0.62</code> en sombre.',
 impact='Chaque réplique de chaque conversation ; en sombre, toute méta (heure, durée, personnes), tout libellé de pied et toute valeur des Réglages.',
 options=[('A. Heures en secondaire (60 %), secondaire sombre à 70 %', 'Une nuance de gris de moins ; 5,59:1 en clair ; Lc 64 en sombre.', 'Les heures pèsent un peu plus.', True),
          ('B. Heures à 55 %', 'Plus discrètes.', '4,5:1 tout juste ; une valeur de plus.', False)],
 choix='A. Le secondaire devient la seule nuance de texte discret ; « M » et aujourd\'hui sont réglés par P01 et P12.',
 refs='WCAG 2.2 › 1.4.3. APCA in a Nutshell › Use-Case & Size Ranges (Lc 60 pour le texte qui se lit).',
 spec=[('ConversationScreen.kt:325', 'val at = label("", 13f, look.ink(0.5))', 'val at = label("", 14f, look.secondary, digits = true)'),
       ('Look.kt:22', 'val secondary = ink(if (dark) 0.62 else 0.6)', 'val secondary = ink(if (dark) 0.70 else 0.6)'),
       ('Look.kt:23', 'val title = ink(if (dark) 0.62 else 0.56)', 'val title = secondary')],
 criteres=['Relevé clair : aucun texte sous 4,5:1.', 'Relevé sombre : texte secondaire à Lc 60 au moins.']))

P.append(dict(id='P08', titre='Aucun titre pour TalkBack', grav='gêne', effort='20 min', lot='L1',
 symptome='Les jours de la liste (« Samedi 7 novembre »), les groupes des Réglages (« Enregistrement », « Intégrations ») et le titre d\'un écran se voient comme des titres mais n\'en sont pas pour l\'accessibilité.',
 preuve='<p>Relevé : <b>0</b> vue marquée titre sur <b>1 084</b> vues des 24 états en clair.</p>',
 cause=S('HomeScreen.kt', 240) + ', ' + S('SettingsScreen.kt', 121) + ', ' + S('Screen.kt', 107) + ' : aucun <code>isAccessibilityHeading</code>.',
 impact='Les personnes aveugles ou malvoyantes, à chaque passage dans une liste longue : sans titres, TalkBack lit chaque conversation une à une pour atteindre un jour.',
 options=[('A. Marquer les titres', '3 lignes ; la navigation « par titres » de TalkBack fonctionne.', 'Aucun.', True)],
 choix='A.', refs='WCAG 2.2 › 1.3.1 Info and Relationships. Android › <code>View#setAccessibilityHeading</code> (API 28 ; minSdk de l\'app : 29).',
 spec=[('HomeScreen.kt:240', 'label(r.text, 14f, look.title, bold = true).apply { setPadding(…) }', 'label(…).apply { setPadding(…); isAccessibilityHeading = true }'),
       ('SettingsScreen.kt:121', 'label(text, 14f, look.title, bold = true).apply { setPadding(…) }', 'label(…).apply { setPadding(…); isAccessibilityHeading = true }'),
       ('Screen.kt:115 (bar, titre)', 'addView(title)', 'addView(title.apply { isAccessibilityHeading = true })')],
 criteres=['Relevé : chaque titre de jour et de groupe a <code>heading = true</code>.', 'TalkBack, navigation par titres : passe de jour en jour.']))

P.append(dict(id='P09', titre='Cinq cibles sous 48 dp', grav='détail', effort='45 min', lot='L1',
 symptome='Le bouton Lire (44 × 44), le champ de recherche de l\'accueil (42,7 dp de haut), celui de la conversation (41,7), la piste du lecteur (26), et à 360 dp de large, les jours du calendrier (45,7 dp de large).',
 preuve='<div class="grid2"><figure><img src="images/p20-cibles.webp" alt="Cibles"><figcaption>Lire 44 × 44, champ 41,7 dp.</figcaption></figure><figure><img src="images/p19-cellules-360.webp" alt="Calendrier à 360 dp"><figcaption>360 dp : cellule de 45,7 × 48 dp.</figcaption></figure></div>',
 cause=S('ConversationScreen.kt', 105) + ' ; ' + S('HomeScreen.kt', 69) + ' et ' + S('ConversationScreen.kt', 62) + ' (hauteur du texte + padding) ; ' + S('HomeScreen.kt', 88) + ' : le calendrier a 8 dp de marge en plus des 12 de la liste.',
 impact='Chaque recherche, chaque lecture ; le calendrier sur les petits téléphones (360 dp : Pixel 4a, nombreux Android d\'entrée de gamme).',
 options=[('A. 48 dp partout', 'La règle d\'Android, tenue par toutes les autres cibles de l\'app.', 'Le calendrier perd 16 dp de marge.', True)],
 choix='A. Pour le calendrier, la grille prend toute la largeur de la liste : (360 − 24) / 7 = 48 dp.', refs='Android › Use large, simple controls (48 × 48 dp). WCAG 2.2 › 2.5.8 (24 px) est tenu partout.',
 spec=[('ConversationScreen.kt:105', 'dp(44), dp(44)', 'dp(48), dp(48)  (voir P04)'),
       ('HomeScreen.kt:69 et ConversationScreen.kt:62', '—', 'minHeight = dp(48)'),
       ('HomeScreen.kt:88', 'setPadding(dp(8), dp(4), dp(8), dp(4))', 'setPadding(0, dp(4), 0, dp(4))')],
 criteres=['Relevés clair, 360 dp et 200 % : aucune cible sous 48 dp.']))

P.append(dict(id='P10', titre='Les chiffres bougent : pas de chiffres tabulaires', grav='détail', effort='30 min', lot='L1',
 symptome='La durée d\'un enregistrement (« 9 s », « 11 s »), le temps du lecteur et les heures n\'ont pas de chiffres à chasse fixe : la ligne change de largeur chaque seconde.',
 preuve='<p>Relevé : <code>fontFeatureSettings</code> vide sur les 2 101 textes mesurés. Le Mac le fait (<code>.monospacedDigit()</code>, DESIGN.md › Texte).</p>',
 cause=S('Screen.kt', 37) + ' : <code>label()</code> n\'a pas d\'option pour les chiffres.',
 impact='Chaque seconde d\'un enregistrement à l\'écran ; à la lecture d\'un son.',
 options=[('A. <code>fontFeatureSettings = "tnum"</code> sur les heures, durées et nombres', 'Roboto les a ; comme le Mac.', 'Aucun.', True)],
 choix='A.', refs='DESIGN.md › Texte (« Heures, durées, nombres : .monospacedDigit() »).',
 spec=[('Screen.kt:37', 'fun label(…, oneLine: Boolean = false)', 'fun label(…, oneLine: Boolean = false, digits: Boolean = false) … if (digits) fontFeatureSettings = "tnum"'),
       ('HomeScreen.kt:273, ConversationScreen.kt:57, 98, 325, HomeScreen.kt:316', 'label(…)', 'label(…, digits = true)')],
 criteres=['Relevé : <code>features = "tnum"</code> sur chaque texte d\'heure ou de durée.']))

P.append(dict(id='P11', titre='Quatre bords gauches dans les Réglages', grav='détail', effort='30 min', lot='L3',
 symptome='Dans un écran de trois blocs : titres de groupe à 20 dp, « Enregistrer les appels » à 28, « Calendrier » et « Mac » à 32, ronds des modes à 34.',
 preuve='<figure><img src="images/p07-bords-reglages.webp" alt="Bords des Réglages"><figcaption>Bords mesurés dans le relevé (x + padding) : 20, 28, 32, 34 dp.</figcaption></figure>',
 cause=S('SettingsScreen.kt', 121) + ' (padding 4) ; ' + S('SettingsScreen.kt', 76) + ' (8) + ' + S('SettingsScreen.kt', 43) + ' (10) ; ' + S('SettingsScreen.kt', 92) + ' (12) ; ' + S('SettingsScreen.kt', 118) + ' (4) + ' + S('Screen.kt', 141) + ' (12).',
 impact='Chaque visite des Réglages.',
 options=[('A. Contenu des cartes à 16 dp du bord de la carte, titres alignés dessus', 'Un seul bord (32 dp de l\'écran) ; la marge de liste de Material (16 dp).', 'Les ronds se décalent de 2 dp.', True),
          ('B. Titres à 16 dp de l\'écran, contenu à 32', 'Titres en retrait inverse.', 'Deux bords.', False)],
 choix='A.', refs='Material Components › <a href="' + MDC + 'docs/components/List.md">List.md</a> : <code>paddingStart="16dp"</code>, <code>paddingEnd="16dp"</code>.',
 spec=[('SettingsScreen.kt:121', 'setPadding(dp(4), dp(top), dp(4), dp(8))', 'setPadding(dp(16), dp(top), dp(16), dp(8))'),
       ('SettingsScreen.kt:76', 'setPadding(dp(8), dp(4), dp(4), dp(4))', 'setPadding(0, dp(4), 0, dp(4))'),
       ('SettingsScreen.kt:43', 'setPadding(dp(10), dp(12), dp(12), dp(12))', 'setPadding(dp(16), dp(12), dp(16), dp(12))  // le rond à 16 dp'),
       ('SettingsScreen.kt:92', 'setPadding(dp(12), dp(8), dp(12), dp(8))', 'setPadding(dp(16), dp(8), dp(16), dp(8))'),
       ('SettingsScreen.kt:118 et Screen.kt:141', 'setPadding(dp(4), …) ; setPadding(dp(12), 0, dp(8), 0)', 'setPadding(0, …) ; setPadding(dp(16), 0, dp(12), 0)')],
 criteres=['Relevé <code>reglages</code> : titres, noms et ronds partent tous de x = 32 dp.']))

P.append(dict(id='P12', titre='Calendrier : deux flèches différentes, aujourd\'hui et le jour choisi mal distingués', grav='détail', effort='30 min', lot='L3',
 symptome='« Mois précédent » et « Mois suivant » n\'ont ni le même dessin ni le même gris. Aujourd\'hui est un chiffre bleu gras ; le jour choisi, un disque gris à 12 % ; les deux à la fois donnent du bleu sur gris à 3,93:1 (2,08:1 en sombre).',
 preuve='<figure><img src="images/p10-calendrier.webp" alt="Calendrier"><figcaption>Banc <code>calendrier</code>. Flèche suivante : 1,77:1 (40 % gravé dans <code>chevron.xml</code> × teinte secondaire).</figcaption></figure>',
 cause=S('HomeScreen.kt', 283) + ' (<code>ic_retour</code>) et ' + S('HomeScreen.kt', 285) + ' (<code>chevron</code>, trait 2,4, <code>#66000000</code>) ; ' + S('HomeScreen.kt', 312) + ' ; ' + S('HomeScreen.kt', 316) + ' (le seul gras 700 de l\'app).',
 impact='Chaque passage au calendrier.',
 options=[('A. La forme de Material : aujourd\'hui en anneau, choisi en disque plein', 'Ce que montre le sélecteur de date d\'Android ; aujourd\'hui et choisi se lisent ensemble.', 'Le disque choisi devient bleu.', True),
          ('B. Garder le disque gris, aujourd\'hui en anneau', 'Moins de bleu.', 'Le choisi reste à 1,32:1 contre la page.', False)],
 choix='A. Une seule flèche, retournée pour le mois précédent.',
 refs='Material Components › <a href="' + MDC + 'lib/java/com/google/android/material/datepicker/res/values/styles.xml">datepicker/styles.xml</a> : <code>Day.Selected</code> → <code>itemFillColor ?attr/colorPrimary</code>, <code>itemTextColor ?attr/colorOnPrimary</code> ; <code>Day.Today</code> → <code>itemStrokeColor</code>, <code>itemStrokeWidth</code>.',
 spec=[('HomeScreen.kt:283', 'iconButton(R.drawable.ic_retour, look.secondary, "Mois précédent", 18)', 'iconButton(R.drawable.chevron, look.secondary, "Mois précédent", 18).apply { scaleX = -1f }'),
       ('HomeScreen.kt:312', 'background = if (selected) pressable(look.mass(24, 0.12)) else flat(24)', 'background = when { selected -> pressable(look.mass(24, color = look.accent)); today -> ring(look.accent, 1); else -> flat(24) }'),
       ('HomeScreen.kt:316', 'label(n.toString(), 15f, if (today) LinkService.ACCENT else look.text) … Typeface.BOLD', 'label(n.toString(), 16f, when { selected -> look.onAccent; today -> look.accent; else -> look.text }, digits = true)  // sans gras'),
       ('chevron.xml:10', 'android:strokeColor="#66000000"', 'android:strokeColor="#FF000000"')],
 criteres=['Image <code>calendrier</code> : flèches symétriques, même gris ; aujourd\'hui en anneau ; jour choisi en disque plein, chiffre à 4,5:1.']))

P.append(dict(id='P13', titre='Icônes : quatre épaisseurs de trait, un chevron presque invisible', grav='détail', effort='1 h', lot='L3',
 symptome='Les icônes au trait mélangent 1,8, 1,9, 2 et 2,4 dp sur 24. Dans le pied, le rond d\'Enregistrer et la roue des Réglages (1,8) sont plus maigres que la loupe (2). Le chevron des Réglages sort à 16 % (opacité gravée × teinte).',
 preuve='<p>Relevé des <code>res/drawable</code> : <a href="inventaire.html#valeurs">Inventaire › Dessin des icônes</a>. Chevron des Réglages : 1,44:1 en clair, 1,68:1 en sombre.</p>',
 cause='Dessins faits un par un ; ' + S('phone/android/app/src/main/res/drawable/chevron.xml', 10) + ' grave <code>#66000000</code>, que <code>setTint</code> multiplie ; ' + S('Screen.kt', 148) + ' teinte à 0,4.',
 impact='Chaque écran ; le chevron, sur chaque ligne des Réglages.',
 options=[('A. Trait de 2 partout, chevron sans opacité gravée et teinté secondaire', 'Un seul trait, comme Material Symbols (poids 400) ; chevron à 5,4:1.', 'Revoir 9 fichiers.', True),
          ('B. Passer à Material Symbols', 'Le jeu de référence.', 'Change le dessin de toutes les icônes, faites pour ressembler au Mac.', False)],
 choix='A.', refs='WCAG 2.2 › 1.4.11 (3:1 pour un objet qui dit qu\'on peut toucher).',
 spec=[('ic_arreter, ic_copier, ic_details, ic_enregistrer, ic_photo, ic_reglages, ic_telecharger (.xml)', 'android:strokeWidth="1.8"', 'android:strokeWidth="2"'),
       ('ic_calendrier, ic_liste (.xml)', 'android:strokeWidth="1.9"', 'android:strokeWidth="2"'),
       ('chevron.xml:10-11', 'strokeColor="#66000000" strokeWidth="2.4"', 'strokeColor="#FF000000" strokeWidth="2"'),
       ('Screen.kt:148', 'icon(R.drawable.chevron, look.ink(0.4), 16)', 'icon(R.drawable.chevron, look.secondary, 16)')],
 criteres=['Tous les <code>strokeWidth</code> de <code>res/drawable</code> valent 2 ; chevron ≥ 3:1 dans les deux modes.']))

P.append(dict(id='P14', titre='Les logos WhatsApp et Telegram disparaissent en clair, Signal en sombre', grav='gêne', effort='30 min', lot='L1',
 symptome='Sur la vignette grise (masse 0,07), le vert de WhatsApp est à 1,56:1 et le bleu de Telegram à 2,17:1 en clair ; le bleu de Signal à 2,24:1 en sombre.',
 preuve='<p><a href="mesures.html#non-texte">Mesures › Contrastes des icônes</a>. Images : <a href="images/etats/clair-icones.webp">clair</a>, <a href="images/etats/sombre-icones.webp">sombre</a>.</p>',
 cause=S('Screen.kt', 87) + ' à ' + S('Screen.kt', 90) + ' : une seule couleur de marque pour les deux modes.',
 impact='Chaque appel WhatsApp, Telegram ou Signal dans la liste, la recherche et l\'en-tête ; c\'est le seul repère de la sorte d\'appel.',
 options=[('A. Une variante par mode, dans la famille de la marque', 'WhatsApp <code>#0F8A4B</code> (3,46:1), Telegram <code>#1C7FB8</code> (3,45:1) en clair ; Signal <code>#8E95FF</code> (5,11:1), Meet <code>#2BB3A6</code> en sombre.', 'Les couleurs s\'écartent un peu des logos.', True),
          ('B. Le logo blanc sur un fond de la marque', 'Le logo exact.', 'Blanc sur <code>#25D366</code> : 1,98:1 ; une masse colorée dans une liste grise.', False),
          ('C. Garder les couleurs de marque', 'Fidèle.', 'Sous 3:1 pour l\'objet qui dit la sorte d\'appel.', False)],
 choix='A.', refs='WCAG 2.2 › 1.4.11 Non-text Contrast.',
 spec=[('Screen.kt:87-90', '"whatsapp" -> 0xFF25D366 … "meet" -> 0xFF00897B', '"whatsapp" -> if (look.dark) 0xFF25D366 else 0xFF0F8A4B\n"signal" -> if (look.dark) 0xFF8E95FF else 0xFF3B45FD\n"telegram" -> if (look.dark) 0xFF26A5E4 else 0xFF1C7FB8\n"meet" -> if (look.dark) 0xFF2BB3A6 else 0xFF00897B')],
 criteres=['Les quatre logos à 3:1 au moins sur leur vignette, en clair et en sombre.']))

P.append(dict(id='P15', titre='Le texte en direct saute de 48 dp quand le texte du Mac arrive', grav='détail', effort='10 min', lot='L3',
 symptome='Pendant l\'enregistrement, le texte du téléphone part à 16 dp du bord ; les répliques finies partent à 64 dp, derrière leur rond. Quand le texte du Mac remplace celui du téléphone, tout le bloc se décale.',
 preuve='<figure><img src="images/p12-direct-retrait.webp" alt="Texte en direct"><figcaption>Relevé : x = 16 dp en direct, 64 dp une fois transcrit.</figcaption></figure>',
 cause=S('ConversationScreen.kt', 349) + ' : sans nom, le rond passe en <code>GONE</code>.',
 impact='Chaque enregistrement suivi à l\'écran, au moment où il se termine.',
 options=[('A. Rond <code>INVISIBLE</code> au lieu de <code>GONE</code>', 'Le texte reste à sa place ; le téléphone ne prétend toujours pas savoir qui parle.', '48 dp de largeur en moins pour le texte en direct.', True)],
 choix='A.', refs='Cohérence de position d\'un même contenu.',
 spec=[('ConversationScreen.kt:349', 'h.mark.visibility = if (l.who.isEmpty()) View.GONE else View.VISIBLE', 'h.mark.visibility = if (l.who.isEmpty()) View.INVISIBLE else View.VISIBLE\nh.who.visibility = if (l.who.isEmpty()) View.GONE else View.VISIBLE')],
 criteres=['Relevé <code>conversation-en-direct</code> : texte à x = 64 dp.']))

P.append(dict(id='P16', titre='Espaces insécables et petites incohérences de textes', grav='détail', effort='45 min', lot='L3',
 symptome='La mise en route coupe « Téléphones › » en fin de ligne. 12 chaînes ont une espace ordinaire avant « : », 2 avant « ? », 4 dans des guillemets « », 2 entre un nombre et son unité. « Pas encore transcrit. » (Journal) et « Pas encore transcrite. » (conversation) ; « Aucune parole reconnue » sans point quand ses voisines en ont un.',
 preuve='<figure><img src="images/p13-fleche-orpheline.webp" alt="Flèche orpheline"><figcaption>Mise en route : « › » seul en fin de ligne.</figcaption></figure><p>Liste complète : <code>donnees/mesures-typographie.csv</code>.</p>',
 cause=S('SetupScreen.kt', 64) + ' ; ' + S('Screen.kt', 160) + ' à 162 ; ' + S('ConversationScreen.kt', 195) + ', ' + S('ConversationScreen.kt', 242) + '.',
 impact='La mise en route (premier écran vu) ; chaque durée longue (« 2 h 41 » peut se couper) ; les états vides.',
 options=[('A. Insécables dans les chaînes et dans Dates', 'Rien ne se coupe mal ; règle typographique française.', 'Caractères invisibles dans le code : les écrire <code>\\u00A0</code> et <code>\\u202F</code>.', True)],
 choix='A. Les apostrophes droites restent : ce sont celles du Mac et du site.',
 refs='Wikipédia › <a href="https://fr.wikipedia.org/wiki/Espace_ins%C3%A9cable">Espace insécable › Usage › En France</a> (espace fine insécable devant « ; ? ! », espace insécable devant « : »). TEXTES.md › Ponctuation.',
 spec=[('SetupScreen.kt:64', '"Sur le Mac : Réglages › Paramètres › Téléphones › Ajouter un téléphone."', '"Sur le Mac\\u00A0: Réglages\\u00A0› Paramètres\\u00A0› Téléphones\\u00A0› Ajouter un téléphone."'),
       ('Screen.kt:160-162', '"$seconds s" ; "${…} min" ; "${…} h ${…}"', '"$seconds\\u00A0s" ; "${…}\\u00A0min" ; "${…}\\u00A0h\\u00A0${…}"'),
       ('ConversationScreen.kt:195', '"Pas encore transcrit."', '"Pas encore transcrit."  (le Journal : masculin, correct ; garder)'),
       ('ConversationScreen.kt:242', '"Aucune parole reconnue"', '"Aucune parole reconnue."'),
       ('12 chaînes avec « : »', '" : "', '"\\u00A0: "  (liste : mesures-typographie.csv)')],
 criteres=['<code>mesures-typographie.csv</code> refait : 0 ligne pour « : », « ? », « › » et les unités.']))

P.append(dict(id='P17', titre='L\'icône de l\'app : le mot de la plaque sur les téléphones les plus denses', grav='détail', effort='1 h', lot='L4',
 symptome='Le micro occupe 37,3 dp sur 108 (57 % de la zone sûre de 66 dp). En xxxhdpi, il fait 150 px, au-dessus du seuil de 128 px : la plaque garde le mot « callrecorder », qui s\'affiche à environ 1,7 dp de haut sur l\'écran d\'accueil. Les autres densités ont déjà la bande.',
 preuve='<p><a href="mesures.html#poids">Mesures › Poids des images</a> : micro de 38, 56, 74, 112 et 150 px selon la densité.</p>',
 cause='<code>scripts/icone.swift</code> choisit la bande d\'après la taille du fichier, pas d\'après la taille affichée.',
 impact='Les téléphones au-dessus de 480 dpi (xxxhdpi), sur l\'écran d\'accueil et dans le tiroir.',
 options=[('A. La bande à toutes les densités d\'Android', 'Applique la règle écrite (<code>b94d18c</code> : « Sous 128 px et sur Android, … le mot devient une bande »).', 'Aucun.', True),
          ('B. A, et le micro agrandi à 48 % du calque', 'Plus présent à côté des autres icônes.', 'Revient sur « le micro, petit » (<code>12fdcff</code>).', False)],
 choix='A, retenue. B est laissée à Gildas.', refs='Android › <a href="https://developer.android.com/develop/ui/views/launch/icon_design_adaptive">Adaptive icons</a> (calques de 108 dp, zone sûre de 66 dp). marque/README.md.',
 spec=[('scripts/icone.swift (sortie Android)', 'plaque avec le mot si le micro dépasse 128 px', 'toujours la bande pour mipmap-*/ic_launcher_devant.png')],
 criteres=['<code>mipmap-xxxhdpi/ic_launcher_devant.png</code> : plaque en bande, sans lettres.'],
 conflit='B irait contre <code>12fdcff</code> (« Android : le micro, petit, sur un fond blanc »).'))

P.append(dict(id='P18', titre='L\'accent ne suit pas le téléphone', grav='détail', effort='1 h', lot='L4',
 symptome='L\'accent est fixé à <code>#0064D2</code>. Sur le Mac, il suit le système (<code>Color.accentColor</code>) et seul « Moi » garde un bleu fixe.',
 preuve='<p>DESIGN.md › Couleurs : « Accent … <code>Color.accentColor</code>, celui du système » ; « Moi » : <code>TranscriptReaderView.me</code>.</p>',
 cause=S('LinkService.kt', 40) + ' ; ' + S('Look.kt', 50) + '.',
 impact='Sur un Pixel, les apps du système prennent les couleurs du fond d\'écran (couleur dynamique, Android 12).',
 options=[('A. Garder le bleu fixe', 'La marque est stable.', 'S\'écarte du principe du Mac (« une app du système »).', False),
          ('B. Accent dynamique (API 31+), « Moi » fixe', 'Traduit le principe du Mac sur Android ; repli <code>#0064D2</code> / <code>#409CFF</code>.', 'L\'accent peut devenir proche de LIVE ou de l\'orange : à vérifier sur 3 fonds d\'écran.', True),
          ('C. Tout Material You (fonds, cartes)', 'Le plus Pixel.', 'Les masses grises en opacités du Mac disparaissent.', False)],
 choix='B, après P02 (qui crée <code>Look.accent</code>).', refs='Android › <a href="https://developer.android.com/develop/ui/views/theming/dynamic-colors">Dynamic color</a> (« added in Android 12 »).',
 spec=[('Look.kt (P02)', 'val accent = if (dark) 0xFF409CFF.toInt() else LinkService.ACCENT', 'val accent = if (Build.VERSION.SDK_INT >= 31) c.getColor(if (dark) android.R.color.system_accent1_200 else android.R.color.system_accent1_600)\n    else if (dark) 0xFF409CFF.toInt() else LinkService.ACCENT')],
 criteres=['Sur trois fonds d\'écran (bleu, vert, rouge) : boutons pleins, ronds et curseur prennent l\'accent ; « Moi » reste bleu ; textes en accent à 4,5:1.']))

P.append(dict(id='P19', titre='Le point rouge des appels : un autre rouge, dans la barre d\'état', grav='détail', effort='20 min', lot='L3',
 symptome='Le point qui garde le micro pendant un appel est <code>#D32F2F</code>, le seul rouge hors palette (LIVE : <code>#C41E14</code> / <code>#FF453A</code>). Il est posé à 36 dp du haut et 12 dp du bord droit, là où la barre d\'état montre déjà l\'indicateur du micro d\'Android.',
 preuve='<p>' + S('CallService.kt', 129) + ', ' + S('CallService.kt', 136) + '-137. ΔE76 entre <code>#C41E14</code> et <code>#D32F2F</code> : voir <a href="inventaire.html#valeurs">Inventaire › Couleurs proches</a>.</p>',
 cause='Écrit avant <code>Look</code> (<code>e20c252</code>, 4 novembre).',
 impact='Chaque appel enregistré quand la pastille ne peut pas se montrer (écran verrouillé, app ouverte).',
 options=[('A. LIVE, et sous la barre d\'état', 'Un seul rouge ; ne se mêle pas aux icônes du système.', 'Lire la hauteur de la barre d\'état.', True)],
 choix='A.', refs='Android 12 › Microphone and camera indicators (« an icon appears in the status bar »).',
 spec=[('CallService.kt:129', 'setColor(0xFFD32F2F.toInt())', 'setColor(Look.Tone.LIVE.color(Look(this)))'),
       ('CallService.kt:137', 'y = size * 3', 'y = statusBarHeight() + size / 2')],
 criteres=['Sur un téléphone en appel : le point sous la barre d\'état, au rouge de l\'app.']))

P.append(dict(id='P20', titre='« CallRecorder » sous l\'icône et dans les Paramètres', grav='détail', effort='10 min', lot='L3',
 symptome='Le nom affiché sous l\'icône, dans l\'en-tête de chaque notification et dans la liste Accessibilité est « CallRecorder ».',
 preuve='<p>' + S('phone/android/app/src/main/AndroidManifest.xml', 28) + ', ' + S('phone/android/app/src/main/AndroidManifest.xml', 60) + ', ' + S('SettingsScreen.kt', 101) + '.</p>',
 cause='Étiquette posée au premier commit Android (<code>ef64907</code>, 1er novembre), avant la règle du nom.',
 impact='Le texte de la marque le plus vu sur le téléphone.',
 options=[('A. « Callrecorder »', 'La règle de la marque (marque/README.md › Le nom dans le texte).', 'Aucun.', True)],
 choix='A. Le dossier « Téléchargements › CallRecorder » est un nom de fichier : il reste.', refs='marque/README.md.',
 spec=[('AndroidManifest.xml:28', 'android:label="CallRecorder"', 'android:label="Callrecorder"'),
       ('AndroidManifest.xml:60', '"CallRecorder : enregistrer les appels"', '"Callrecorder\\u00A0: enregistrer les appels"'),
       ('SettingsScreen.kt:101', '"1. Touchez CallRecorder dans la liste…"', '"1. Touchez Callrecorder dans la liste…"')],
 criteres=['<code>grep -rn "CallRecorder" res AndroidManifest.xml *.kt</code> : seulement les chemins de fichiers.']))

P.append(dict(id='P21', titre='Des noms coupés à la lettre', grav='détail', effort='1 h', lot='L3',
 symptome='« 23:57 · 47 min · Sophie Marchand, Karim B… » : le second nom est coupé au milieu. 4 textes coupés à 100 %, 10 à 360 dp, 38 à 200 %.',
 preuve='<figure><img src="images/p17-entete-coupe.webp" alt="En-tête coupé"><figcaption>En-tête d\'une conversation, 412 dp.</figcaption></figure>',
 cause=S('ConversationScreen.kt', 57) + ' et ' + S('HomeScreen.kt', 273) + ' : une ligne, « … » en fin.',
 impact='Chaque conversation à deux personnes ou plus.',
 options=[('A. Couper au nom : « Sophie Marchand +1 »', 'Le nombre de personnes reste ; aucun nom tronqué.', 'Mesurer le texte au rendu.', True),
          ('B. Deux lignes', 'Tout se lit.', 'La barre et la ligne grandissent.', False)],
 choix='A. Les noms complets restent dans Détails.', refs='Lisibilité ; même règle que la colonne de liste du Mac, qui a la place de tout montrer.',
 spec=[('Screen.kt (nouveau)', '—', 'fun people(names: List<String>, paint: TextPaint, room: Float): String  // retire les noms de la fin et ajoute « +n » tant que ça dépasse'),
       ('ConversationScreen.kt:231 et HomeScreen.kt:258', 'i.people.joinToString(", ")', 'people(i.people, label.paint, largeur disponible)')],
 criteres=['Relevé : aucun nom coupé par « … » à 412 dp.']))

P.append(dict(id='P22', titre='Des outils qui ne font rien, et des états vides sans forme commune', grav='détail', effort='45 min', lot='L3',
 symptome='Sans texte, Copier et Télécharger restent dans la barre, à 40 % d\'opacité, et toujours actifs pour TalkBack. Les états vides sont une phrase grise de 15 sp au milieu, avec ou sans point.',
 preuve='<p>Images : <a href="images/etats/clair-journal-vide.webp">Journal vide</a>, <a href="images/etats/clair-avant-transcription.webp">pas encore arrivée</a>, <a href="images/etats/clair-aucune-parole.webp">aucune parole</a>.</p>',
 cause=S('ConversationScreen.kt', 183) + '-184 (<code>alpha</code> seul) ; ' + S('ConversationScreen.kt', 61) + ' (15 sp).',
 impact='Chaque conversation sans texte : en attente du Mac, en écoute, ou vide.',
 options=[('A. Masquer Copier et Télécharger quand il n\'y a rien', '« Zéro bouton inutile » (principe tranché) ; TalkBack n\'annonce plus de bouton mort.', 'La barre change de largeur.', True),
          ('B. Les désactiver (<code>isEnabled = false</code>)', 'La barre ne bouge pas ; l\'état est dit.', 'Des boutons inutiles restent.', False)],
 choix='A, et l\'état vide en 16 sp secondaire, toujours avec son point.', refs='WCAG 2.2 › 4.1.2 Name, Role, Value (un bouton à 40 % qui reste actif). DESIGN.md › Principes (« Zéro bouton inutile »).',
 spec=[('ConversationScreen.kt:183-184', 'copyButton.alpha = if (all.isEmpty()) 0.4f else 1f', 'copyButton.visibility = if (all.isEmpty()) View.GONE else View.VISIBLE ; downloadButton.visibility = copyButton.visibility'),
       ('ConversationScreen.kt:61', 'label("", 15f, look.secondary)', 'label("", 16f, look.secondary)')],
 criteres=['Images <code>journal-vide</code>, <code>avant-transcription</code> : barre réduite à Rechercher (et Détails).']))

P.append(dict(id='P23', titre='Six tailles de texte pour quatre rôles', grav='détail', effort='3 h', lot='L4',
 symptome='12, 13, 14, 15, 16 et 17 sp, plus un × 0,875. Le nom d\'une réplique (15), la valeur d\'un réglage (15) et un état vide (15) ont une taille que rien d\'autre n\'a ; le titre de barre (17) est hors de l\'échelle de Material.',
 preuve='<p><a href="inventaire.html#valeurs">Inventaire › Tailles de texte</a> : 31 réglages, avec leurs lignes.</p>',
 cause='Chaque écran fixe ses tailles (DESIGN.md : « chaque écran … n\'y fixe que ses tailles de texte »).',
 impact='Toute l\'app : des écarts d\'un sp se voient comme des hésitations.',
 options=[('A. Une échelle de quatre tailles : 12, 14, 16, 24, avec les rôles de Material 3', 'Une valeur par rôle (DESIGN.md) ; Material 3 donne les rôles.', 'Le nom des répliques passe de 15 à 14 medium ; le titre de barre de 17 à 16 medium.', True),
          ('B. Garder les tailles, les nommer', 'Rien ne change à l\'écran.', 'Les quasi-doublons restent.', False)],
 choix='A, détaillé dans <a href="systeme.html#type">Système › Texte</a> avec la table de migration.', refs='Material Components › <a href="' + MDC + 'docs/theming/Typography.md">Typography.md</a> (Title Medium : Medium 16 sp ; Body Large : Regular 16 sp ; Body Medium : Regular 14 sp ; Label Medium : Medium 12 sp ; Headline Small : Regular 24 sp).',
 spec=[('Look.kt (nouveau)', '—', 'object Type { const val label = 12f; const val body = 14f; const val bodyLarge = 16f; const val headline = 24f }'),
       ('31 lignes', 'label(…, 13f) / 15f / 17f', 'voir la table de migration')],
 criteres=['<code>grep -n "f, " *.kt</code> ne trouve plus de taille hors de <code>Look.Type</code>.']))

P.append(dict(id='P24', titre='Le choix Liste / Calendrier ne tient qu\'à un gris de 12 %', grav='détail', effort='15 min', lot='L3',
 symptome='Le bouton choisi a une masse à 12 % sur une capsule à 5 % : 1,18:1 en clair, 1,26:1 en sombre. L\'icône choisie passe du gris secondaire au noir.',
 preuve='<p><a href="mesures.html#non-texte">Mesures › Contrastes des icônes</a>.</p>',
 cause=S('HomeScreen.kt', 114) + '-115.',
 impact='Le haut de l\'accueil, à chaque ouverture.',
 options=[('A. Icône choisie à l\'accent', 'L\'état se lit par la couleur et le fond ; comme les boutons segmentés de Material (couleur du conteneur et de l\'icône).', 'Un bleu de plus en haut de l\'accueil.', True),
          ('B. Garder', 'Sobre ; l\'icône noire distingue déjà.', '1,18:1 pour l\'état.', False)],
 choix='A.', refs='WCAG 2.2 › 1.4.11 (états des composants).',
 spec=[('HomeScreen.kt:115', 'setTint(if (on) look.text else look.secondary)', 'setTint(if (on) look.accent else look.secondary)')],
 criteres=['Image <code>accueil</code> : l\'icône choisie à l\'accent.']))

P.append(dict(id='P25', titre='Examiné, non retenu : le point rouge d\'« Enregistrer une réunion »', grav='détail', effort='—', lot='—',
 symptome='Dans le pied de l\'accueil, le seul geste d\'enregistrement est gris, comme Réglages.',
 preuve='<p><a href="images/etats/clair-accueil.webp">Banc accueil</a> ; Mac : <code>captures-mac-0.24.0/vide.webp</code>, pied identique, gris.</p>',
 cause=S('HomeScreen.kt', 234) + ' : <code>look.secondary</code>.',
 impact='—',
 options=[('A. Point plein en LIVE, anneau et texte gris', 'Le point rouge veut dire « enregistrer ».', 'Le pied du téléphone ne serait plus celui du Mac (DESIGN.md › Accueil).', False),
          ('B. Ne rien changer', 'Le pied est celui du Mac, voulu ; le rouge reste réservé à ce qui enregistre.', 'Le geste se lit au mot.', True)],
 choix='B. Le rouge dit « ça enregistre » (P05) ; le mettre au repos brouillerait ce sens.', refs='DESIGN.md › Couleurs (« En cours, REC : Palette.live »).',
 spec=[], criteres=[]))

def opt_html(o):
    t, pour, contre, ch = o
    return f'<div class="opt{" choisi" if ch else ""}"><b>{t}{" · choisie" if ch else ""}</b><span class="ok">Pour</span> : {pour}<br><span class="ko">Contre</span> : {contre}</div>'

def spec_html(sp):
    if not sp: return ''
    return '<div class="tw"><table><thead><tr><th>Où</th><th>Avant</th><th>Après</th></tr></thead><tbody>' + ''.join(
        f'<tr><td><code>{esc(w)}</code></td><td><pre>{esc(a)}</pre></td><td><pre>{esc(b)}</pre></td></tr>' for w, a, b in sp) + '</tbody></table></div>'

def build():
    b = ['<h1>Problèmes et recommandations</h1><p class="lede">25 problèmes, du plus gênant au plus fin. Pour chacun : symptôme, preuve (image recadrée du banc ou mesure), cause dans le code, impact, options avec leurs pour et contre, choix argumenté, règle de référence, spécification prête à coder (avant → après) et critères d\'acceptation vérifiables.</p>']
    b.append('<div class="tw"><table><thead><tr><th>N°</th><th>Problème</th><th>Gravité</th><th>Effort</th><th>Lot</th></tr></thead><tbody>' + ''.join(
        f'<tr><td><a href="#{p["id"]}">{p["id"]}</a></td><td>{p["titre"]}</td><td><span class="pill {"gene" if p["grav"] == "gêne" else ""}">{p["grav"]}</span></td><td>{p["effort"]}</td><td>{p["lot"]}</td></tr>' for p in P) + '</tbody></table></div>')
    for p in P:
        b.append(f'<section class="prob" id="{p["id"]}"><h2>{p["id"]} · {p["titre"]}</h2><span class="pill {"gene" if p["grav"] == "gêne" else ""}">{p["grav"]}</span> <span class="pill">effort : {p["effort"]}</span> <span class="pill">lot {p["lot"]}</span>')
        b.append('<dl>')
        b.append(f'<dt>Symptôme</dt><dd>{p["symptome"]}</dd><dt>Preuve</dt><dd>{p["preuve"]}</dd><dt>Cause</dt><dd>{p["cause"]}</dd><dt>Impact</dt><dd>{p["impact"]}</dd>')
        b.append(f'<dt>Options</dt><dd><div class="opts">{"".join(opt_html(o) for o in p["options"])}</div></dd><dt>Choix</dt><dd>{p["choix"]}</dd><dt>Référence</dt><dd>{p["refs"]}</dd>')
        if p.get('conflit'): b.append(f'<dt class="against">Choix déjà tranché</dt><dd class="against">{p["conflit"]}</dd>')
        if p['spec']: b.append(f'<dt>Spécification</dt><dd>{spec_html(p["spec"])}</dd>')
        if p['criteres']: b.append('<dt>Acceptation</dt><dd><ul>' + ''.join(f'<li>{c}</li>' for c in p['criteres']) + '</ul></dd>')
        b.append(f'<dt>Prototype</dt><dd><a href="prototypes.html">Prototypes</a></dd></dl></section>')
    b.append('''<h2 id="hors">Hors graphisme, relevé en passant</h2><div class="card"><p><b><code>stateDescription</code> sur Android 10.</b> ''' + S('SettingsScreen.kt', 171) + ''' appelle <code>View.stateDescription</code>, ajouté à l'API 30, sans garde de version ; l'app accepte l'API 29 (<code>build.gradle.kts</code> : <code>minSdk = 29</code>). Sur un téléphone en Android 10, ouvrir les Réglages devrait lever <code>NoSuchMethodError</code>. À vérifier sur un émulateur API 29, puis entourer d'un <code>if (Build.VERSION.SDK_INT >= 30)</code>.</p></div>''')
    page('problemes.html', 'Problèmes et recos', '\n'.join(b))
    return P

if __name__ == '__main__':
    print(len(build()))
