from commun import *
import json, collections
import valeurs

def build():
    res = json.load(open(f'{D}/mesures-resume.json'))
    txt = rows('mesures-contrastes-textes')
    tgt = rows('mesures-cibles')
    typo = rows('mesures-typographie')
    nt = valeurs.write_non_text()
    b = ['<h1>Mesures</h1><p class="lede">Ce qui se calcule : contrastes de chaque texte réellement dessiné, contrastes des icônes et des états, tailles de cible, débordements à 360 dp et à 200 %, sémantique d\'accessibilité, typographie des textes, poids des images. Les données brutes sont à côté, en CSV.</p>']
    b.append('''<h2 id="methode">Méthode</h2>
<div class="card"><ul>
<li><b>Relevé</b> : une copie du banc Android (hors du dépôt, rien n'est changé dans le code) ajoute, à chaque image, un relevé de l'arbre des vues : place et taille en dp, texte, taille en sp, graisse, couleur, fond (<code>GradientDrawable</code>, <code>RippleDrawable</code>), description, état, titre, cliquable. Le fond effectif d'un texte est la composition de ses ancêtres sur le fond de la page. Outils dans <a href="donnees/outils/">donnees/outils/</a>.</li>
<li><b>Variantes</b> : clair et sombre en 412 × 915 dp ; 360 × 780 dp (petit téléphone) ; 600 × 960 dp (pliable ouvert) ; texte à 200 % (<code>fontScale = 2</code>, échelle non linéaire d'Android 14, <a href="https://developer.android.com/about/versions/14/features">Android 14 › Accessibility › Non-linear font scaling to 200%</a>).</li>
<li><b>WCAG 2.2</b> : 1.4.3 (4,5:1 pour le texte, 3:1 au-delà de 24 px ou 18,66 px gras), 1.4.11 (3:1 pour les composants et objets graphiques), 2.5.8 (cible de 24 × 24 px au moins), 1.4.4 (texte agrandi à 200 % sans perte) ; <a href="https://www.w3.org/TR/WCAG22/">w3.org/TR/WCAG22</a>.</li>
<li><b>APCA</b> (0.0.98G-4g, mode simple) : Lc 75 au moins pour une colonne de texte (les répliques), Lc 60 pour le reste du texte lu, Lc 45 pour les grands titres, Lc 30 pour un indice, Lc 15 pour le non-texte ; <a href="https://git.apcacontrast.com/documentation/APCA_in_a_Nutshell">APCA in a Nutshell › Use-Case &amp; Size Ranges</a>. APCA n'est pas une norme : il sert ici à départager, surtout en sombre, où WCAG 2 surestime le contraste.</li>
<li><b>Cible</b> : 48 × 48 dp, la règle d'Android (<a href="https://developer.android.com/guide/topics/ui/accessibility/apps">Make apps more accessible › Use large, simple controls</a>).</li>
</ul></div>''')
    # résumé
    order = ['base', 'sombre', 'etroit', 'large', 'texte200']
    labels = {'base': 'Clair, 412 dp', 'sombre': 'Sombre, 412 dp', 'etroit': 'Clair, 360 dp', 'large': 'Clair, 600 dp', 'texte200': 'Texte 200 %'}
    b.append('<h2 id="resume">Résumé par variante</h2>')
    b.append(table(['Variante', 'Textes relevés', 'Sous 4,5:1 (WCAG)', 'Sous le seuil APCA', 'Textes coupés « … »', 'Cibles', 'Cibles &lt; 48 dp'],
        [[labels[k], res[k]['textes'], res[k]['wcag_echecs'], res[k]['apca_echecs'], res[k]['coupes'], res[k]['cibles'], res[k]['cibles_sous_48']] for k in order if k in res], num=(1, 2, 3, 4, 5, 6)))
    b.append('<p class="small">Les nombres comptent des occurrences (un même texte répété dans plusieurs états compte plusieurs fois). Les tableaux suivants regroupent les couples uniques. Le clair « base » contient aussi trois écrans en sombre (le test <code>enSombre</code> du banc) : ils sont comptés à part ci-dessous.</p>')
    # couples uniques
    def uniq(mode_filter):
        seen = collections.OrderedDict()
        for r in txt:
            if not mode_filter(r): continue
            k = (r['texte_compose'], r['fond_compose'], r['sp'], r['graisse'])
            if k not in seen:
                seen[k] = dict(r, ex=[])
            if len(seen[k]['ex']) < 3 and r['texte'] not in seen[k]['ex']: seen[k]['ex'].append(r['texte'])
            seen[k]['n'] = seen[k].get('n', 0) + 1
        return sorted(seen.values(), key=lambda r: (r['wcag_ok'] == 'True', r['apca_ok'] == 'True', float(r['wcag'])))
    def ctable(us):
        return table(['Texte (exemples)', 'sp', 'Graisse', 'Texte composé', 'Fond composé', 'WCAG', '', 'APCA Lc', '', 'Fois'],
            [['<br>'.join(esc(e[:48]) for e in r['ex']), r['sp'], r['graisse'], sw(r['texte_compose']) + r['texte_compose'], sw(r['fond_compose']) + r['fond_compose'],
              fr(float(r['wcag'])) + ':1', ('<span class="ok">✓</span>' if r['wcag_ok'] == 'True' else f'<span class="ko">✗ {r["wcag_requis"]}</span>'),
              fr(float(r['apca_lc']), 1), ('<span class="ok">✓</span>' if r['apca_ok'] == 'True' else f'<span class="ko">✗ {r["apca_requis"]}</span>'), r['n']] for r in us], num=(1, 2, 5, 7, 9))
    clair = uniq(lambda r: r['variante'] == 'base')
    sombre = uniq(lambda r: r['variante'] == 'sombre')
    b.append(f'<h2 id="textes">Contrastes des textes</h2><h3>Clair : {len(clair)} couples uniques</h3>' + ctable(clair))
    b.append(f'<h3>Sombre : {len(sombre)} couples uniques</h3>' + ctable(sombre))
    b.append('<p>Lecture : en clair, les échecs WCAG sont l\'heure des répliques (50 %, 3,88:1), l\'initiale de « Moi » sur son rond (4,31:1), le chiffre d\'aujourd\'hui sur le jour choisi (3,93:1). En sombre, tout ce qui garde <code>#0064D2</code> : « ● Écoute depuis… » (2,98:1), « Relier un calendrier » (2,61:1), aujourd\'hui (2,08:1). APCA ajoute en sombre le texte secondaire (blanc à 62 %, Lc 54 sur la page, Lc 55 sur une carte), les heures à 50 % (Lc 40), « Moi » (Lc 46) et LIVE (Lc 40) : lisibles, mais sous Lc 60.</p>')
    # non texte
    b.append('<h2 id="non-texte">Contrastes des icônes, traits et états (WCAG 1.4.11)</h2><p>Les teintes des icônes ne se lisent pas dans l\'arbre des vues (elles sont posées par <code>setTint</code>) : elles sont reprises du code, composées sur leur fond réel, dans les deux modes.</p>')
    b.append(table(['Mode', 'Élément', 'Où', 'Premier plan', 'Fond', 'WCAG', '3:1', 'APCA'],
        [[r['mode'], esc(r['role']), esc(r['ou']), sw(r['premier_plan']) + r['premier_plan'], sw(r['fond']) + r['fond'], fr(r['wcag']) + ':1',
          ('' if r['ok'] == '' else ('<span class="ok">✓</span>' if r['ok'] else '<span class="ko">✗</span>')), fr(r['apca_lc'], 1)] for r in nt], num=(5, 7)))
    kos = [r for r in nt if r['ok'] is False]
    b.append(f'<p><b>{len(kos)}</b> éléments sous 3:1 sur {sum(1 for r in nt if r["ok"] != "")} mesurés. Les plus visibles : le logo WhatsApp en clair (1,56:1), le chevron des Réglages (1,44:1 clair, 1,68:1 sombre), la flèche « Mois suivant » (1,77:1), et l\'état « choisi » du sélecteur Liste/Calendrier et du jour, qui ne tient qu\'à une masse de 12 % (1,18:1 à 1,45:1). Pour ce dernier, l\'icône choisie passe aussi du secondaire au texte : l\'état se lit, mais faiblement.</p>')
    # cibles
    def tuniq(var):
        seen = collections.OrderedDict()
        for r in tgt:
            if r['variante'] != var: continue
            k = (r['nom'][:30], r['w'], r['h'])
            if k not in seen: seen[k] = dict(r, n=0, ecrans=set())
            seen[k]['n'] += 1; seen[k]['ecrans'].add(r['ecran'])
        return list(seen.values())
    b.append('<h2 id="cibles">Cibles tactiles</h2>')
    for var in ('base', 'etroit', 'texte200'):
        us = [r for r in tuniq(var) if r['min48'] == 'False']
        b.append(f'<h3>{labels[var]} : {len(us)} cibles sous 48 dp</h3>')
        if us:
            b.append(table(['Cible', 'Classe', 'Largeur', 'Hauteur', 'Écrans'], [[esc(r['nom'] or '(sans nom)'), r['classe'], fr(float(r['w']), 1), fr(float(r['h']), 1), esc(', '.join(sorted(r['ecrans']))[:90])] for r in us], num=(2, 3)))
    b.append('<p>À cela s\'ajoute la <b>SeekBar</b> du lecteur : 308 × 26 dp, que le relevé ne compte pas parmi les « cliquables » (elle se déplace au doigt). Sa hauteur de 26 dp est sous les 48 dp d\'Android. Aucune cible n\'est sous les 24 × 24 px de WCAG 2.5.8.</p>')
    # débordements
    cut = [r for r in txt if r['coupe'] == 'True']
    cnt = collections.Counter(r['variante'] for r in cut)
    b.append('<h2 id="debordements">Textes coupés et débordements</h2>')
    b.append(table(['Variante', 'Textes coupés par « … »'], [[labels.get(k, k), v] for k, v in sorted(cnt.items()) if k in labels], num=(1,)))
    seen = set(); ex = []
    for r in cut:
        if r['variante'] in ('base', 'texte200', 'etroit') and (r['variante'], r['texte'][:30]) not in seen:
            seen.add((r['variante'], r['texte'][:30])); ex.append([labels[r['variante']], r['ecran'], esc(r['texte'][:70]), r['sp'], fr(float(r['w']), 1)])
    b.append('<details><summary>Les textes coupés, un par variante</summary>' + table(['Variante', 'Écran', 'Texte complet', 'sp', 'Largeur dp'], ex, num=(3, 4)) + '</details>')
    b.append('''<p>Les coupures verticales ne se voient pas dans le relevé (Android réduit la vue au lieu de la faire déborder) mais se voient dans les images à 200 % :</p>
<div class="grid2"><figure><img src="images/p18-200-entete.webp" alt="En-tête et répliques à 200 %"><figcaption>200 % : la ligne de détail de l'en-tête est coupée par la barre de 64 dp ; « SM » devient « S » dans un rond de 36 dp ; l'indice du champ est tronqué sans « … ».</figcaption></figure>
<figure><img src="images/p18-200-barre.webp" alt="Barre du bas à 200 %"><figcaption>200 % : les quatre mots de la barre du bas se touchent ; les icônes restent à 22 dp.</figcaption></figure></div>''')
    # sémantique
    b.append('''<h2 id="semantique">Sémantique d'accessibilité</h2>
<div class="tw"><table><thead><tr><th>Contrôle</th><th>Relevé</th><th>Lecture</th></tr></thead><tbody>
<tr><td>Titres (<code>isAccessibilityHeading</code>)</td><td class="n">0 sur 1 084 vues</td><td>Ni les jours de la liste, ni les groupes des Réglages, ni le titre d'un écran ne sont des titres : TalkBack ne peut pas sauter de jour en jour (WCAG 1.3.1).</td></tr>
<tr><td>Outils inactifs (Copier, Télécharger sans texte)</td><td>alpha 0,4, toujours actifs</td><td><code>ConversationScreen.kt:183-184</code> : seule l'opacité change ; TalkBack annonce « Copier, bouton » sans dire qu'il ne fait rien (WCAG 4.1.2).</td></tr>
<tr><td>États annoncés</td><td>2 : Liste/Calendrier (<code>isSelected</code>), Enregistrer les appels (<code>stateDescription</code>)</td><td>Le lecteur dit « Lire » ou « Pause » ; le jour choisi du calendrier n'a pas d'état « sélectionné ».</td></tr>
<tr><td>Annonces vivantes (<code>accessibilityLiveRegion</code>)</td><td>0</td><td>« ● En cours », le texte en direct et la durée changent sans être annoncés ; c'est le bon choix pour une durée qui change chaque seconde, moins pour l'arrivée du texte du Mac.</td></tr>
<tr><td>Images décoratives</td><td>toutes cachées (<code>IMPORTANT_FOR_ACCESSIBILITY_NO</code>)</td><td>Correct : les vignettes ne doublent pas le titre.</td></tr>
<tr><td>Boutons d'icône</td><td>tous nommés</td><td>Retour, Plus, Rechercher, Fermer la recherche, Liste, Calendrier, Mois précédent / suivant, Lire / Pause, Prendre une photo, Arrêter l'enregistrement. « Plus » nomme le bouton ⋯ : Android dit « Plus d'options ».</td></tr>
<tr><td>Jours du calendrier</td><td>« Dimanche 8 novembre, des conversations »</td><td>Bien nommés ; « Aujourd'hui · dimanche 8 novembre » lu tel quel avec son point médian.</td></tr>
</tbody></table></div>''')
    # typographie
    tc = collections.Counter(r['controle'] for r in typo)
    b.append('<h2 id="typo">Typographie des textes visibles</h2><p>180 chaînes visibles contrôlées (<code>donnees/mesures-typographie.csv</code>). Règles : espace insécable avant « : », espace fine insécable avant « ? » « ! » « ; » (<a href="https://fr.wikipedia.org/wiki/Espace_ins%C3%A9cable">Wikipédia, Espace insécable › Usage › En France</a>).</p>')
    b.append(table(['Contrôle', 'Chaînes', 'Exemples'], [[esc(k), v, '<br>'.join([esc(r['texte'][:60]) + ' ' + src(r['fichier'], r['ligne']) for r in typo if r['controle'] == k][:3])] for k, v in tc.most_common()], num=(1,)))
    b.append('<p>Autres écarts relevés : « Pas encore transcrit. » (Journal) et « Pas encore transcrite. » (conversation) ; « Aucune parole reconnue » sans point quand ses voisines en ont un (<code>ConversationScreen.kt:242</code>) ; « CallRecorder » visible dans 4 textes (étiquette de l\'app, service d\'accessibilité, toast, boîte des Réglages) quand la marque écrit « Callrecorder ». Les apostrophes droites sont celles du Mac et du site : elles ne sont pas un écart.</p>')
    # poids
    b.append('''<h2 id="poids">Poids des images de l'app</h2>
<div class="tw"><table><thead><tr><th>Fichier</th><th class="n">Pixels</th><th class="n">Octets</th><th class="n">Micro</th></tr></thead><tbody>
<tr><td>mipmap-mdpi/ic_launcher_devant.png</td><td class="n">108</td><td class="n">3 816</td><td class="n">38 px (35,2 %)</td></tr>
<tr><td>mipmap-hdpi/ic_launcher_devant.png</td><td class="n">162</td><td class="n">7 848</td><td class="n">56 px (34,6 %)</td></tr>
<tr><td>mipmap-xhdpi/ic_launcher_devant.png</td><td class="n">216</td><td class="n">14 621</td><td class="n">74 px (34,3 %)</td></tr>
<tr><td>mipmap-xxhdpi/ic_launcher_devant.png</td><td class="n">324</td><td class="n">31 675</td><td class="n">112 px (34,6 %)</td></tr>
<tr><td>mipmap-xxxhdpi/ic_launcher_devant.png</td><td class="n">432</td><td class="n">54 980</td><td class="n">150 px (34,7 %)</td></tr>
<tr><td>res/drawable/*.xml (26 vecteurs)</td><td class="n">—</td><td class="n">15 696</td><td class="n">—</td></tr>
</tbody></table></div>
<p>Le micro occupe 37,3 dp sur les 108 du calque, soit 57 % de la zone sûre de 66 dp (<a href="https://developer.android.com/develop/ui/views/launch/icon_design_adaptive">Adaptive icons › Design adaptive icons</a> : « The 66x66 safe zone … is never clipped »). Seul le fichier xxxhdpi dépasse 128 px de micro : c'est le seul qui garde le mot de la plaque, et il sert aux téléphones au-dessus de 480 dpi. Le poids total, 113 Ko, ne pose pas de problème.</p>''')
    page('mesures.html', 'Mesures', '\n'.join(b))
    return {'textes_mesures': len(txt), 'couples_clair': len(clair), 'couples_sombre': len(sombre), 'non_texte': len(nt), 'cibles': len(tgt), 'typo': len(typo)}

if __name__ == '__main__':
    print(build())
