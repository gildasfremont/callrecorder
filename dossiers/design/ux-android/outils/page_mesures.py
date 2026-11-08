"""Page « Mesures » : contrastes, cibles, sémantique d'accessibilité, police agrandie, mise en page, poids."""
import collections, glob, os, json
from commun import *

def sw(h): return f'<span class="sw" style="background:{h}"></span><code>{e(h)}</code>'

def construire():
    r = json_("mesures-resume.json")
    C = lire("contrastes.csv"); S = lire("contrastes-statiques.csv"); T = lire("cibles.csv"); A = lire("accessibilite.csv"); P = lire("police.csv")
    c = []
    echecs = [x for x in C if x["wcag_1.4.3"] != "OK"]
    uniques_echec = {(x["theme"], x["texte"], x["fond"]) for x in echecs}
    c.append(f"<h1>Mesures : {len(uniques_echec)} couples de couleurs sous le seuil WCAG, 4 pièces sous 48 dp, 85 éléments touchables sans rôle, 15 états rognés à 200 %</h1>")
    c.append(f"""<p class="lead">Ce qui suit est calculé, pas estimé. Le banc d'inventaire a rendu {r['etats_captures']} écrans ({r['etats_distincts']} états × clair et sombre × police 100, 130 et 200 %) et relevé
pour chaque vue sa taille, son texte, sa couleur, le fond composé de ses parents, son rôle et son nom pour TalkBack. <code>outils/mesures.py</code> en tire les tableaux ; les CSV bruts sont dans <a href="donnees/">donnees/</a>.</p>""")
    c.append(f"""<div class="grid">
<div class="chiffre"><b>{r['couples_contraste']}</b><span>couples texte/fond distincts mesurés (taille comprise)</span></div>
<div class="chiffre"><b>{len(uniques_echec)}</b><span>couples de couleurs sous WCAG 2 · 1.4.3, sur {len(echecs)} couples × tailles</span></div>
<div class="chiffre"><b>{r['cibles_relevees']}</b><span>cibles touchables relevées (toutes configurations)</span></div>
<div class="chiffre"><b>4</b><span>pièces sous 48 dp : Lire, barre de position, deux champs de recherche</span></div>
<div class="chiffre"><b>85</b><span>éléments touchables distincts sans rôle (TalkBack ne dit pas « bouton »)</span></div>
<div class="chiffre"><b>7</b><span>titres visuels non déclarés comme titres</span></div>
<div class="chiffre"><b>15 / 34</b><span>états avec un texte rogné ou collé à 200 %</span></div>
<div class="chiffre"><b>11</b><span>emplois de l'accent #0064D2 qui ne changent pas en sombre</span></div>
</div>""")
    c.append("""<details><summary>Méthode et limites</summary><ul>
<li><b>Rendu</b> : Robolectric 4 (Android 15, <code>sdk = 35</code>), 412 × 915 dp, xxhdpi (3 px/dp), <code>GraphicsMode.NATIVE</code>. La police agrandie passe par <code>RuntimeEnvironment.setFontScale</code> ; Robolectric applique la courbe non linéaire d'Android 14 (13 sp → 17,2 dp à 130 %, 16 sp → 20,3 dp à 200 %).</li>
<li><b>Fond composé</b> : couleur de chaque parent (ColorDrawable, GradientDrawable, couche non-masque d'un RippleDrawable) posée par transparence sur le fond de l'écran. Les fonds des boîtes de dialogue d'Android (InsetDrawable) ne se lisent pas : les boîtes sont exclues des contrastes, et leurs couleurs relevées à part.</li>
<li><b>WCAG 2</b> : rapport de luminance relative ; seuil 4,5:1, 3:1 pour un texte d'au moins 24 dp, ou 18,66 dp en gras (WCAG 2.2, 1.4.3 et sa note sur le « large scale »). <b>APCA</b> : APCA-W3 0.0.98G-4g, Lc signé (négatif = texte clair sur fond sombre) ; seuils de la table de correspondance « bronze » : Lc 75 pour 16 px, 90 pour 14 px, 60 pour un texte de 24 px ou de 16 px en gras. APCA est donné en indicateur, WCAG 2 reste la règle.</li>
<li><b>Ce que le banc ne voit pas</b> : le bouton radio coché (animation non dessinée, l'état est relevé), la vraie matière des boîtes d'un Pixel, les notifications, la page Accessibilité d'Android, le comportement de TalkBack lui-même (on relève ce qu'il recevra : rôle, nom, état, titre).</li></ul></details>""")

    # Contrastes texte
    c.append('<h2 id="contrastes">1. Contrastes du texte</h2>')
    c.append("<h3>Sous le seuil WCAG 2 (1.4.3)</h3>")
    vus, rangs = set(), []
    for x in echecs:
        k = (x["theme"], x["texte"], x["fond"])
        if k in vus: continue
        vus.add(k)
        tailles = sorted({x2["taille_dp"] for x2 in echecs if (x2["theme"], x2["texte"], x2["fond"]) == k}, key=float)
        rangs.append([e(x["theme"]), sw(x["texte"]), sw(x["fond"]), " · ".join(tailles), f'<span class="ko">{x["wcag2"]}:1</span>', x["seuil_wcag"], x["apca_lc"], e(x["exemples"])])
    c.append(tableau(["Thème", "Texte", "Fond", "Tailles rendues (dp)", "WCAG 2", "Seuil", "APCA Lc", "Où (état : texte)"], rangs, brut=True))
    c.append("""<p class="note">Lecture : les heures des répliques (<code>ink(0.5)</code>, ConversationScreen.kt:325) échouent en clair sur 19 rendus ; l'initiale de « Moi » (accent sur sa teinte à 12 %, ConversationScreen.kt:355) échoue à 4,30 ; le chiffre d'aujourd'hui sur le jour choisi (HomeScreen.kt:316) à 3,93 en clair et 2,10 en sombre ; tout l'accent en sombre échoue (2,10 à 2,98).</p>""")
    par = collections.Counter((x["theme"], x["apca"]) for x in C)
    c.append("<h3>Répartition</h3>")
    c.append(tableau(["Thème", "Couples", "WCAG 2 OK", "WCAG 2 échec", "APCA au seuil", "APCA sous le seuil"],
                     [[t, sum(1 for x in C if x["theme"] == t), sum(1 for x in C if x["theme"] == t and x["wcag_1.4.3"] == "OK"), sum(1 for x in C if x["theme"] == t and x["wcag_1.4.3"] != "OK"),
                       par[(t, "OK")], par[(t, "sous le seuil")]] for t in ("clair", "sombre")]))
    sous = sorted([x for x in C if x["apca"] != "OK" and x["wcag_1.4.3"] == "OK"], key=lambda x: abs(float(x["apca_lc"])))
    c.append(f"<details><summary>{len(sous)} couples conformes à WCAG 2 mais sous le seuil APCA (les plus faibles d'abord)</summary>" +
             tableau(["Thème", "Texte", "Fond", "Taille dp", "Gras", "WCAG 2", "APCA Lc", "Seuil APCA", "Exemples"],
                     [[x["theme"], sw(x["texte"]), sw(x["fond"]), x["taille_dp"], x["gras"], x["wcag2"], x["apca_lc"], x["seuil_apca"], e(x["exemples"][:140])] for x in sous], brut=True) + "</details>")
    c.append('<p class="note">Ce qu\'APCA ajoute : les textes de 13 et 14 sp en gris secondaire (0,6) passent WCAG 2 (5,6:1) mais restent sous Lc 90, le seuil APCA pour un texte de contenu de cette taille. C\'est l\'argument pour ne pas descendre sous 14 sp en gris, et garder 12 sp pour l\'accessoire (heures, mots d\'outil).</p>')

    # Hors texte
    c.append('<h2 id="hors-texte">2. Contrastes hors texte (WCAG 1.4.11, 3:1)</h2>')
    c.append(tableau(["Élément", "Thème", "Couleur", "Fond", "Rapport", "APCA Lc", "1.4.11"],
                     [[e(x["element"]), x["theme"], sw(x["couleur"]), sw(x["fond"]), x["wcag2"], x["apca_lc"],
                       ('<span class="ok">OK</span>' if float(x["wcag2"]) >= 3 else '<span class="ko">sous 3:1</span>')] for x in S], brut=True))
    c.append('<p class="note">1.4.11 vise ce qui est nécessaire pour comprendre ou utiliser : la piste de la barre de position (1,17:1 et 1,26:1), le chevron (2,53:1 en clair), les logos WhatsApp et Telegram sur leur plaque claire (1,56 et 2,18:1) et Signal en sombre (2,23:1) sont sous le seuil. Les masses grises (cartes à 1,11:1) ne portent pas d\'information : elles ne sont pas visées.</p>')

    # Sombre
    c.append('<h2 id="sombre">3. Le thème sombre et l\'accent</h2>')
    ACC = [("ConversationScreen.kt:81", "Fond du bouton Lire", "forme ; texte blanc dessus 5,59:1", "le rond reste lisible ; contour 2,98:1 sur le fond"),
           ("ConversationScreen.kt:87-88", "Barre de position (progression, curseur)", "hors texte", "2,98:1 sur le fond, 2,6:1 sur la carte"),
           ("HomeScreen.kt:242", "« ● Écoute depuis 13:23 » et icône du Journal", "texte 14 sp", "<span class=ko>2,98:1</span>"),
           ("HomeScreen.kt:253", "Plaque du Journal (teinte 12 %)", "fond", "—"),
           ("HomeScreen.kt:316", "Chiffre d'aujourd'hui", "texte 15 sp gras", "<span class=ko>2,10:1</span> sur le jour choisi"),
           ("SettingsScreen.kt:38", "Ronds des modes", "hors texte", "2,6:1 sur la carte"),
           ("SettingsScreen.kt:62", "« Relier un calendrier »", "texte 14 sp medium", "<span class=ko>2,64:1</span>"),
           ("SetupScreen.kt:25", "Fond de « Scanner le code du Mac »", "forme ; texte blanc 5,59:1", "contour 2,98:1"),
           ("ConversationScreen.kt:347 (Tone.INFO)", "« Moi » et son rond", "texte 15 sp gras", "<span class=ok>5,89:1</span> : seul emploi qui passe par Tone.INFO"),
           ("Pastille.kt / Look.floating", "—", "—", "—")]
    c.append(tableau(["Où", "Quoi", "Nature", "En sombre (#0064D2 sur #1E1E1E ou la carte)"], [[f"<code>{e(a)}</code>", e(b), e(n), d] for a, b, n, d in ACC[:-1]], brut=True))
    c.append('<p class="note">Cause unique : <code>LinkService.ACCENT</code> est une constante, quand <code>Look.Tone.INFO</code> prévoit #409CFF en sombre (5,89:1). Les emplois passent par la constante.</p>')

    # Cibles
    c.append('<h2 id="cibles">4. Cibles tactiles</h2>')
    dist = {}
    for x in T:
        if x["police_%"] != "100" or x["theme"] != "clair": continue
        k = (x["ecran"], x["classe"], x["nom_a11y"][:50])
        dist.setdefault(k, x)
    petits = [x for x in dist.values() if x["sous_48dp"]]
    c.append(f"<p>{len(dist)} cibles distinctes à 100 % (clair). Seuil : 48 × 48 dp (Android, « Make apps more accessible » ; Material 3) ; 24 × 24 px pour WCAG 2.2 · 2.5.8 (AA), que toutes atteignent.</p>")
    c.append(tableau(["Écran", "Pièce", "Nom pour TalkBack", "Largeur", "Hauteur", "Écart à 48"], [[x["ecran"], x["classe"], e(x["nom_a11y"]), x["largeur_dp"], x["hauteur_dp"], f"{48 - min(float(x['largeur_dp']), float(x['hauteur_dp'])):.1f} dp"] for x in sorted(petits, key=lambda x: x["nom_a11y"])]))
    tailles = collections.Counter()
    for x in dist.values():
        h = float(x["hauteur_dp"]); tailles["< 44" if h < 44 else "44–47" if h < 48 else "48" if h < 49 else "49–63" if h < 64 else "64 et plus"] += 1
    c.append(tableau(["Hauteur de cible (dp)", "Cibles"], [[k, tailles[k]] for k in ("< 44", "44–47", "48", "49–63", "64 et plus")]))
    c.append('<p class="note">Les répliques sont « cliquables » pour Android (texte sélectionnable) : elles sont exclues, ce ne sont pas des cibles. La pastille : deux cibles de 48 × 48 dp, sans écart entre elles.</p>')
    c.append(f"<details><summary>Les {len(dist)} cibles, avec taille et nom</summary>" + tableau(["Écran", "État", "Pièce", "Rôle", "Nom", "L", "H"], [[x["ecran"], x["etat"], x["classe"], x["role_a11y"].split(".")[-1], e(x["nom_a11y"]), x["largeur_dp"], x["hauteur_dp"]] for x in dist.values()]) + "</details>")

    # A11y
    c.append('<h2 id="talkback">5. Ce que TalkBack recevra</h2>')
    cnt = collections.Counter(); ex = collections.defaultdict(set)
    for x in A:
        for m in x["manques"].split("; "):
            if m: cnt[m] += 1; ex[m].add(x["nom"][:40])
    c.append(tableau(["Manque", "Occurrences (34 états)", "Éléments distincts", "Exemples", "Règle"],
                     [[e(m), n, len(ex[m]), e(" · ".join(sorted(ex[m])[:6])), {"rôle absent (pas « bouton »)": "WCAG 4.1.2 Nom, rôle, valeur", "titre non déclaré (isAccessibilityHeading)": "WCAG 1.3.1 ; Android : headings", "grisé mais actif": "WCAG 4.1.2 (état)", "interrupteur annoncé comme bloc": "WCAG 4.1.2 (rôle)"}.get(m, "")] for m, n in cnt.most_common()]))
    LECTURE = [
        ("Ligne « En cours » (accueil)", "« Réunion, 14:23 · ● En cours · 0 s » ; lu « … point, cercle noir, En cours, point, zéro s » selon la voix", "« Réunion, en cours depuis 14:23, 12 minutes, bouton »"),
        ("Ligne de conversation", "« Point produit 13:23 · 47 min · Sophie Marchand, Karim Benali », sans rôle", "« Point produit, 13 h 23, 47 minutes, avec Sophie Marchand et Karim Benali, bouton »"),
        ("Jour du calendrier choisi", "« Dimanche 8 novembre, des conversations », rien ne dit qu'il est choisi", "« … sélectionné »"),
        ("Liste / Calendrier", "« Liste, bouton, sélectionné » : juste", "—"),
        ("Copier sans texte", "« Copier » (grisé à 40 %, actif, sans effet)", "« Copier, désactivé »"),
        ("Enregistrer les appels", "« Enregistrer les appels, Éteint » sans rôle d'interrupteur", "« Enregistrer les appels, interrupteur, désactivé »"),
        ("Barre de position", "« Position dans le son, 0 % »", "« Position dans le son, 0 min sur 47 min, curseur »"),
        ("Pastille", "« Prendre une photo » et « Arrêter l'enregistrement », sans rôle", "« … bouton »"),
        ("Point rouge", "« Callrecorder enregistre votre voix » (vue non touchable, non annoncée hors exploration)", "—"),
        ("Titres de jour et de groupe", "texte simple ; la navigation par titres de TalkBack ne s'y arrête pas", "« Vendredi 6 novembre, titre »"),
    ]
    c.append("<h3>Lecture élément par élément</h3>")
    c.append(tableau(["Élément", "Reçu aujourd'hui (d'après le nœud d'accessibilité)", "Attendu"], LECTURE))

    # Police
    c.append('<h2 id="police">6. Police agrandie (WCAG 1.4.4)</h2>')
    par_pol = collections.defaultdict(set)
    for x in P:
        if x["theme"] != "clair": continue
        par_pol[(x["police_%"], "rogné" if x["rogne"] else "collé" if x["autre"] else "points")].add((x["ecran"], x["etat"]))
    c.append(tableau(["Police", "États avec texte rogné en hauteur", "États avec textes collés", "États avec une ligne coupée par des points"],
                     [[f"{p} %", len(par_pol[(p, 'rogné')]), len(par_pol[(p, 'collé')]), len(par_pol[(p, 'points')])] for p in ("100", "130", "200")]))
    rog = {}
    for x in P:
        if x["theme"] == "clair" and x["police_%"] == "200" and (x["rogne"] or x["autre"]):
            rog.setdefault(x["texte"][:40], x)
    CAUSE = {"13:": "ConversationScreen.kt:145 (barre en hauteur fixe 64 dp)", "SM": "ConversationScreen.kt:331 (rond fixe 36 dp)", "Scanner": "SetupScreen.kt:51 (bouton en hauteur fixe 48 dp)",
             "Écoute": "ConversationScreen.kt:145 (barre du Journal)", "Télé": "ConversationScreen.kt:171 (outil de 76 dp mini, libellés côte à côte)", "12:": "ConversationScreen.kt:145", "14:": "ConversationScreen.kt:145"}
    c.append(tableau(["Texte", "Écran / état", "Problème", "Cause"], [[e(k), f"{x['ecran']} / {x['etat']}", x["rogne"] or x["autre"], next((v for kk, v in CAUSE.items() if k.startswith(kk)), "")] for k, x in rog.items()]))
    c.append('<div class="preuves"><figure><img src="images/p04-conversation-200.webp" width="309" alt="Conversation à 200 %"><figcaption>200 % : 1 détail de l\'en-tête rogné, 2 « SM » réduit à « S », 3 libellés collés.</figcaption></figure><figure><img src="images/p04-mise-en-route-200.webp" width="309" alt="Mise en route à 200 %"><figcaption>200 % : le libellé du bouton déborde de ses 48 dp fixes.</figcaption></figure></div>')

    # Mise en page
    c.append('<h2 id="mise-en-page">7. Mise en page mesurée</h2>')
    c.append(tableau(["Mesure", "Valeur", "Source"], [
        ["Hauteur d'une ligne de conversation", "64 dp (mini), vignette 44 dp", "accueil--liste (JSON)"],
        ["Lignes du pied", "48 dp × 2, largeur 388 dp", "accueil--liste"],
        ["Position de l'icône, mise en route", "y = 346 dp (aucun Mac), 349 (sans Google Play), 407 (connexion), 346 (autre Wi-Fi) : saut de 61 dp à la connexion", "mise-en-route--* (JSON)"],
        ["Barre flottante d'une conversation", "4 outils de 76 × 56 dp, bord bas à 24 dp, liste rembourrée de 108 dp en bas", "ConversationScreen.kt:121, 151, 171"],
        ["Barre du haut", "64 dp fixes sur les trois écrans", "HomeScreen.kt:102, ConversationScreen.kt:145, SettingsScreen.kt:125"],
        ["Lignes visibles sans défiler (accueil, 915 dp)", "6 conversations et 5 titres de jour avant le pied", "accueil--liste"],
    ]))

    # Poids
    c.append('<h2 id="poids">8. Poids des images de l\'app</h2>')
    rangs = []
    for f in sorted(glob.glob("phone/android/app/src/main/res/*/*")):
        rangs.append([f"<code>{e(f.split('res/')[1])}</code>", os.path.getsize(f)])
    tot = sum(r[1] for r in rangs)
    c.append(f"<p>{len(rangs)} fichiers, {tot / 1024:.1f} Ko en tout : 26 icônes vectorielles (249 à 1 894 octets) et l'icône de l'app en 5 densités. Rien à gagner ici.</p>")
    c.append(f"<details><summary>Détail</summary>{tableau(['Fichier', 'Octets'], rangs, brut=True)}</details>")
    page("mesures.html", "Mesures UX Android", "\n".join(c), "Contrastes WCAG et APCA, cibles, sémantique d'accessibilité, police agrandie, mesurés sur 246 rendus.")

if __name__ == "__main__":
    construire()
