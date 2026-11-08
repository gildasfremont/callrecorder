"""Reconstruit tout le dossier : python3 build.py"""
import json, csv, os
from commun import *
import p_inventaire, p_mesures, p_problemes, p_prototypes, p_systeme

inv = p_inventaire.build()
mes = p_mesures.build()
probs = p_problemes.build()
protos = p_prototypes.build()
nmig = p_systeme.build()

summary = json.load(open(f'{D}/inventaire-resume.json'))
valeurs_inv = sum(v['occurrences'] for v in summary.values())
nbmes = sum(1 for _ in open(f'{D}/mesures-contrastes-textes.csv')) - 1 + mes['non_texte'] + mes['cibles'] + (sum(1 for _ in open(f'{D}/mesures-accessibilite.csv')) - 1) + mes['typo']
retenues = [p for p in probs if p['lot'] != '—']

TOP = [
    ('P02', 'En sombre, le bleu de l\'app reste celui du clair', '« ● Écoute depuis » à 2,98:1, « Relier un calendrier » à 2,61:1, aujourd\'hui à 2,08:1 ; 7 usages de la constante.'),
    ('P01', 'Les voix d\'une réunion ont toutes la même couleur', '100 % des voix autres que Moi en <code>#A0470A</code> ; le Mac en a 5.'),
    ('P03', 'À 200 % de texte, la barre du bas, l\'en-tête et les ronds se coupent', '38 textes coupés à 200 % contre 4 à 100 % ; 4 mots collés dans la barre du bas.'),
    ('P14', 'Les logos WhatsApp et Telegram disparaissent en clair', 'WhatsApp 1,56:1, Telegram 2,17:1 (clair) ; Signal 2,24:1 (sombre) ; seuil 3:1.'),
    ('P05', '« En cours » perd son rouge en ouvrant la conversation', 'Rouge dans la liste, <code>#99000000</code> dans l\'en-tête.'),
    ('P04', 'Le lecteur : curseur coupé, piste de 26 dp, bouton de 44 dp', 'Demi-disque à 00:00 ; 2 cibles sous 48 dp.'),
    ('P06', 'La notification d\'enregistrement montre une barre de chargement', 'Barre indéterminée + « Depuis 14:02 » + heure d\'en-tête ; icône de pause pour « Arrêter ».'),
    ('P07', 'Trois petits textes sous 4,5:1 en clair', 'Heures des répliques 3,88:1 sur chaque réplique ; « M » 4,31:1 ; aujourd\'hui 3,93:1 ; secondaire sombre à Lc 54.'),
    ('P08', 'Aucun titre pour TalkBack', '0 titre sur 1 084 vues.'),
    ('P09', 'Cinq cibles sous 48 dp', 'Lire 44, champs 41,7 et 42,7, piste 26, jours du calendrier 45,7 à 360 dp.'),
]

idx = [f'''<h1>App Android : dossier graphique</h1>
<p class="lede">Relecture graphique complète de l'app Android de Callrecorder, par un graphiste habitué à Android : inventaire de tout ce qu'elle dessine, mesures, problèmes et recommandations sourcées, prototypes, système unifié avec sa migration, plan. Branche <code>recos-design</code>, 8 novembre 2026. Ce dossier part de la <a href="../graphisme-android.html">première liste</a> (17 recos), qu'il remplace.</p>
<div class="kpi"><div><b>{inv["etats"]}</b><span>états d'écran (24 au banc, 22 lus dans le code)</span></div><div><b>{valeurs_inv}</b><span>valeurs inventoriées dans le code, avec fichier:ligne</span></div><div><b>{nbmes:,}</b><span>mesures (contrastes, cibles, sémantique, typographie)</span></div><div><b>{len(retenues)}</b><span>recos retenues, et 1 examinée puis écartée</span></div></div>
<div class="kpi"><div><b>6</b><span>variantes relevées : clair, sombre, 360 dp, 600 dp, texte 200 %</span></div><div><b>{protos}</b><span>prototypes (13 écrans × avant/après × clair/sombre)</span></div><div><b>{nmig}</b><span>changements dans la table de migration</span></div><div><b>4</b><span>lots, environ 4 jours de travail</span></div></div>
<h2>Les dix problèmes qui comptent le plus</h2>'''.replace(f'{nbmes:,}', f'{nbmes:,}'.replace(',', ' '))]
idx.append(table(['', 'Problème', 'Chiffre', 'Gravité'], [[f'<a href="problemes.html#{i}">{i}</a>', t, c, '<span class="pill gene">gêne</span>' if next(p for p in probs if p['id'] == i)['grav'] == 'gêne' else '<span class="pill">détail</span>'] for i, t, c in TOP]))
idx.append('''<h2>Ce qui tient bien</h2><div class="card"><p>La liste par jour et ses vignettes de 44 dp ; toutes les cibles d'icône à 48 dp ; l'absence de filets ; les masses en opacités du texte, fidèles au Mac ; la barre flottante du bas ; la pastille à deux gestes ; des contrastes de texte sains en clair (27 couples uniques sur 30 passent WCAG et APCA) ; les images décoratives toutes cachées à TalkBack ; tous les boutons d'icône nommés. Les recos ne touchent pas à cela.</p></div>
<h2>Comment ce dossier a été fait</h2><div class="card"><ol>
<li><b>Lu</b> : DESIGN.md, TEXTES.md, SPEC-telephone.md, marque/README.md, les captures du Mac 0.24.0, tout le code de <code>phone/android</code> (5 399 lignes) et l'historique complet des choix (<code>git log -S</code> sur 916 commits).</li>
<li><b>Relevé</b> : une copie du banc, hors du dépôt, rejoue 24 états en 6 variantes et relève l'arbre des vues ; un script lit le code pour inventorier chaque valeur. Aucune ligne du code de l'app n'est changée.</li>
<li><b>Mesuré</b> : WCAG 2.2 et APCA pour chaque texte dessiné et chaque icône, cibles, débordements, sémantique, typographie, poids.</li>
<li><b>Sourcé</b> : chaque reco cite un critère WCAG, une page Android, le code source de Material Components (Typography.md, List.md, datepicker/styles.xml, ProgressIndicator.md, FloatingToolbar.md) ou une règle de DESIGN.md. Les pages de m3.material.io ne se lisent pas sans JavaScript : elles ne sont pas citées. Les comportements d'apps Google que je n'ai pas pu vérifier ne sont pas cités non plus.</li>
<li><b>Prototypé</b> : 13 écrans en HTML/CSS au dp près, avant et après, clair et sombre.</li></ol></div>
<h2>Sommaire</h2><ol class="toc">
<li><a href="inventaire.html">Inventaire</a> : états, composants, tailles, graisses, couleurs, opacités, espacements, rayons, icônes, textes</li>
<li><a href="mesures.html">Mesures</a> : contrastes textes et non-textes, cibles, débordements, sémantique, typographie, poids</li>
<li><a href="problemes.html">Problèmes et recos</a> : 25 fiches, spécifications avant → après, critères d'acceptation</li>
<li><a href="prototypes.html">Prototypes</a> : 13 écrans × 4</li>
<li><a href="systeme.html">Système et migration</a> : échelle, couleurs, espacements, composants, 78 changements fichier par fichier</li>
<li><a href="plan.html">Plan</a> : 4 lots, efforts, risques, choix déjà tranchés</li>
<li><a href="donnees/">donnees/</a> : CSV et JSON bruts, outils du relevé</li></ol>''')
page('index.html', 'Android graphisme', '\n'.join(idx))

LOTS = [
    ('L1', 'Lisibilité et états', 'P02, P04, P05, P06, P07, P08, P09, P10, P14', '1 jour',
     'Petits changements locaux, sans dessin nouveau ; tous vérifiables au banc (relevé clair, sombre, 360 dp).',
     'P06 revient sur un choix (<code>9dea502</code>) : le livrer seul, après réponse de Gildas. Le reste est sans risque de régression visible hors des éléments visés.'),
    ('L2', 'Voix et grand texte', 'P01, P03', '1 jour',
     'Touche la réplique et les barres, que tous les écrans partagent ; à faire après L1 pour ne relever qu\'une fois.',
     'P03 change la mise en page à 200 % : refaire les relevés <code>texte200</code> et <code>etroit</code>. P01 crée des couleurs : contrôler les deux modes.'),
    ('L3', 'Finitions', 'P11, P12, P13, P15, P16, P19, P20, P21, P22, P24', '1 jour',
     'Retouches de forme écran par écran ; indépendantes entre elles.',
     'P13 retouche 9 fichiers d\'icônes : comparer les images avant / après. P20 change le nom vu dans les Paramètres d\'Android et la liste Accessibilité (boîte des Réglages à suivre).'),
    ('L4', 'Système', 'P23, P18, P17', '1 à 1,5 jour',
     'La migration complète (78 changements) ; à faire sujet par sujet, comme le dit DESIGN.md › Écarts connus, pour ne pas entrer en conflit avec les sujets en cours.',
     'Conflits avec les autres sessions qui touchent les mêmes écrans. P18 (couleur dynamique) et P17 B (micro agrandi) sont à trancher par Gildas.'),
]
CHOIX = [
    ('P06', 'Barre qui file sous le texte de la notification', '9dea502', '6 novembre 2026', 'Remplacée par le chronomètre ; « jamais de rouge » gardé.'),
    ('P17 B', 'Le micro, petit, sur fond blanc', '12fdcff', '7 novembre 2026', 'Option laissée à Gildas ; la reco retenue (bande partout) applique <code>b94d18c</code>.'),
    ('P18', 'Accent fixe <code>#0064D2</code> sur Android (DESIGN.md › Téléphone)', '9dea502', '6 novembre 2026', 'Accent dynamique, « Moi » fixe ; à trancher.'),
    ('P23', 'Chaque écran fixe ses tailles de texte (DESIGN.md › Téléphone)', '55625a5', '6 novembre 2026', 'Une échelle dans Look ; DESIGN.md › Écarts connus prévoit déjà de ramener les tailles en dur.'),
    ('P25', 'Pied de l\'accueil gris, comme le Mac', '55625a5', '6 novembre 2026', 'Examiné, non retenu : le choix tient.'),
    ('P01', 'Orange pour la personne en face', 'Mac : TranscriptReader.swift', '—', 'Gardé pour les personnes nommées ; les « Voix N » suivent le Mac.'),
]
pl = ['<h1>Plan</h1><p class="lede">Les recos retenues, regroupées en quatre lots, dans l\'ordre où les faire, avec l\'effort, les risques, et ce qui touche à un choix déjà tranché.</p>']
pl.append(table(['Lot', 'Nom', 'Recos', 'Effort', 'Pourquoi cet ordre', 'Risques'], [[l, n, ', '.join(f'<a href="problemes.html#{x.strip()}">{x.strip()}</a>' for x in r.split(',')), e, w, k] for l, n, r, e, w, k in LOTS]))
pl.append('<h2>Détail par reco</h2>' + table(['Reco', 'Lot', 'Effort', 'Gravité', 'Fichiers'], [[f'<a href="problemes.html#{p["id"]}">{p["id"]}</a> {p["titre"]}', p['lot'], p['effort'], p['grav'], esc(', '.join(sorted(set(s[0].split(':')[0].split(' ')[0] for s in p['spec']))))] for p in probs]))
pl.append('<h2>Ce qui touche à un choix déjà tranché</h2>' + table(['Reco', 'Choix', 'Commit', 'Date', 'Ce que propose le dossier'], [[f'<a href="problemes.html#{i.split()[0]}">{i}</a>', c, f'<code>{h}</code>', d, w] for i, c, h, d, w in CHOIX]))
pl.append('''<h2>Ce que Gildas est seul à trancher</h2><div class="card"><ol>
<li><b>P06</b> : remplacer la barre qui file par le chronomètre dans la notification d'enregistrement.</li>
<li><b>P18</b> : accent dynamique (couleurs du fond d'écran) ou bleu fixe.</li>
<li><b>P17 B</b> : agrandir le micro de l'icône (aujourd'hui 57 % de la zone sûre).</li></ol></div>
<h2>Vérifier sans téléphone</h2><div class="card"><p>Chaque lot se vérifie avec le banc et les outils de <a href="donnees/outils/LISEZMOI.md">donnees/outils</a> : refaire le relevé dans les 6 variantes, puis comparer <code>mesures-resume.json</code> avant et après (échecs WCAG, APCA, cibles, coupures) et les critères d'acceptation de chaque fiche. Ce qui demande un téléphone : la notification (P06), le point des appels (P19), la couleur dynamique (P18), l'icône sur l'écran d'accueil (P17).</p></div>
<h2>À mettre à jour dans DESIGN.md, avec le code</h2><div class="card"><ul>
<li>Téléphone › Fond et texte : secondaire sombre 0,70 ; plus de titre à 0,56 ; jeton <code>accent</code> clair / sombre.</li>
<li>Téléphone › Une conversation : couleurs de Moi, de la personne en face et des voix ; numéro seul pour « Voix N ».</li>
<li>Téléphone › Notifications : chronomètre (si P06 est retenue).</li>
<li>Téléphone : échelle de texte (12, 14, 16, 24) et règle « une valeur par rôle dans Look ».</li>
<li>Écarts connus : retirer les lignes réglées.</li></ul></div>''')
page('plan.html', 'Plan', '\n'.join(pl))
print({'etats': inv['etats'], 'valeurs': valeurs_inv, 'mesures': nbmes, 'recos': len(retenues), 'protos': protos, 'migration': nmig})
