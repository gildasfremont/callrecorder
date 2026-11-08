import json
D="2026-11-08"
R=[]
def a(q,site,url,larg,obs,mes,cap): R.append(dict(question=q,site=site,url=url,date=D,largeur=larg,observation=obs,mesures=mes,capture=cap))
Q1="1. Ligne de commande d'installation"
a(Q1,"brew.sh","https://brew.sh",375,"La commande est montrée en entier : elle passe à la ligne (white-space: pre-wrap, l'URL est coupée en plein mot) sur 3 lignes, sans défilement ni ellipse ; bouton copier toujours visible à droite.",
 {"police":"13px monospace","interligne":"19,24px","whiteSpace":"pre-wrap","overflowX":"auto","clientWidth":291,"scrollWidth":291,"hauteurBloc":74,"lignes":3,"boutonCopier":{"visibleSansSurvol":True,"opacite":1,"taille":"44x74"}},"brew-commande-375.webp")
a(Q1,"brew.sh","https://brew.sh",1440,"Commande entière sur une ligne, bouton copier (icône ⧉, aria-label « Copy to clipboard ») toujours visible.",
 {"police":"13px monospace","whiteSpace":"pre-wrap","clientWidth":908,"scrollWidth":908,"hauteurBloc":44,"lignes":1,"boutonCopier":{"visibleSansSurvol":True,"taille":"44x44"}},"brew-commande-1440.webp")
a(Q1,"rustup.rs","https://rustup.rs",375,"La commande reste sur une ligne (nowrap) et défile horizontalement dans son cadre : 217 px visibles sur 607, coupée net sans ellipse ; bouton copier toujours visible.",
 {"police":"15px Fira Mono","interligne":"26px","whiteSpace":"nowrap","overflowX":"auto","textOverflow":"clip","clientWidth":217,"scrollWidth":607,"partVisible":"36 %","boutonCopier":{"visibleSansSurvol":True,"taille":"51x58"}},"rustup-commande-375.webp")
a(Q1,"rustup.rs","https://rustup.rs",1440,"Commande entière sur une ligne (607 px), bouton copier toujours visible.",
 {"police":"15px Fira Mono","whiteSpace":"nowrap","clientWidth":607,"scrollWidth":607,"boutonCopier":{"visibleSansSurvol":True,"taille":"51x58"}},"rustup-commande-1440.webp")
a(Q1,"tailscale.com","https://tailscale.com/download/linux",375,"Une ligne (white-space: pre) qui défile horizontalement : 263 px visibles sur 397, coupée sans ellipse ; police réduite à 14 px ; bouton copier (icône 17 px) toujours visible.",
 {"police":"14,06px SF Mono","whiteSpace":"pre","overflowX":"auto","textOverflow":"clip","clientWidth":263,"scrollWidth":397,"partVisible":"66 %","boutonCopier":{"visibleSansSurvol":True,"taille":"17x21"}},"tailscale-commande-375.webp")
a(Q1,"tailscale.com","https://tailscale.com/download/linux",1440,"Commande entière sur une ligne à 16 px, bouton copier toujours visible.",
 {"police":"16px SF Mono","whiteSpace":"pre","clientWidth":453,"scrollWidth":453,"boutonCopier":{"visibleSansSurvol":True,"taille":"17x24"}},"tailscale-commande-1440.webp")
Q2="2. Anneau de focus au clavier"
a(Q2,"apple.com","https://www.apple.com/fr/macos/",1440,"Contour plein bleu 2 px (#0071E3) sur tous les éléments tabulés ; le décalage varie : 0 à 3 px sur les boutons, −7 px (à l'intérieur) dans la barre de navigation.",
 {"outline":"2px solid rgb(0,113,227)","outlineOffset":{"selecteurPays":"0px","boutonContinuer":"3px","boutonFermer":"1px","liensNavGlobale":"-7px"},"boxShadow":"none","focusVisible":True},"apple-focus-1440.webp")
a(Q2,"raycast.com","https://www.raycast.com",1440,"Anneau natif du navigateur (outline-style: auto) teinté gris très clair #EEE, 1 px, décalé de 1 px, qui suit l'arrondi 6 px des liens.",
 {"outline":"auto 1px rgb(238,238,238)","outlineOffset":"1px","boxShadow":"none","borderRadius":"6px"},"raycast-focus-1440.webp")
a(Q2,"linear.app","https://linear.app",1440,"Contour plein 1 px à la couleur de marque (violet #5E69D1), décalé de 2 px, sur des liens en pilule.",
 {"outline":"1px solid rgb(94,105,209)","outlineOffset":"2px","boxShadow":"none","borderRadius":"9999px"},"linear-focus-1440.webp")
a(Q2,"culturedcode.com/things","https://culturedcode.com/things/",1440,"Anneau natif du navigateur (outline-style: auto) presque noir #101010, 1 px, décalé de 1 px.",
 {"outline":"auto 1px rgb(16,16,16)","outlineOffset":"1px","boxShadow":"none","borderRadius":"6px"},"things-focus-1440.webp")
a(Q2,"notion.com","https://www.notion.com/fr",1440,"Contour plein bleu 2 px (#0075DE), décalé de 2 px, identique sur tous les liens et boutons de l'en-tête.",
 {"outline":"2px solid rgb(0,117,222)","outlineOffset":"2px","boxShadow":"none","borderRadius":"4px"},"notion-focus-1440.webp")
Q3="3. Contrôles segmentés / onglets : survol"
a(Q3,"apple.com","https://www.apple.com/fr/macbook-air/",1440,"Onglets texte (role=tab) : au survol, l'onglet non choisi ne change que la couleur du texte, de #6E6E73 à #424245 ; pas de fond. L'onglet choisi est en #1D1D1F.",
 {"nonChoisiRepos":{"couleur":"rgb(110,110,115)","fond":"transparent"},"nonChoisiSurvol":{"couleur":"rgb(66,66,69)","fond":"transparent"},"choisi":{"couleur":"rgb(29,29,31)"},"opacite":"1 inchangée"},"apple-onglets-survol-1440.webp")
a(Q3,"raycast.com","https://www.raycast.com/pricing",1440,"Contrôle segmenté Pro/Plus/Max : au survol, le segment non choisi passe du gris #9C9C9D au blanc, sans fond ; seul le segment choisi a un fond (blanc 9 %) et un liseré intérieur.",
 {"nonChoisiRepos":{"couleur":"rgb(156,156,157)","fond":"transparent"},"nonChoisiSurvol":{"couleur":"rgb(255,255,255)","fond":"transparent"},"choisi":{"fond":"rgba(255,255,255,0.09)","boxShadow":"inset 0 1px 0 rgba(255,255,255,0.06)"},"rail":"rgba(255,255,255,0.04)"},"raycast-onglets-survol-1440.webp")
a(Q3,"notion.com","https://www.notion.com/fr/pricing",1440,"Contrôle segmenté Facturation mensuelle/annuelle : aucun changement au survol du segment non choisi (capture identique au pixel près) ; le segment choisi est une pastille blanche sur rail gris.",
 {"nonChoisiRepos":{"couleur":"rgba(0,0,0,0.5)","fond":"transparent"},"nonChoisiSurvol":{"couleur":"rgba(0,0,0,0.5)","fond":"transparent"},"differencePixelsSurvol":0},"notion-onglets-survol-1440.webp")
Q4="4. Grilles d'icônes d'apps ou d'intégrations à 375 px"
a(Q4,"raycast.com","https://www.raycast.com/store",375,"Pas de grille : une extension par rangée, icône 32 px suivie du nom (et d'un bouton Install), dans une carte avec description.",
 {"iconePx":32,"parRangee":1,"nomAffiche":True,"vedettes":"icône 64 px dans une tuile 96 px, une par carte"},"raycast-icones-375.webp")
a(Q4,"linear.app","https://linear.app/integrations",375,"Pas de grille : une intégration par carte, icône 40 px à gauche du nom et de l'éditeur (« By Linear »), description dessous ; 72 icônes de même taille.",
 {"iconePx":40,"parRangee":1,"nomAffiche":True,"icones":72},"linear-icones-375.webp")
a(Q4,"notion.com","https://www.notion.com/fr/integrations",375,"Une intégration par rangée, icône 48 px dans une tuile grise 88 px ; le nom est dans le DOM mais écrasé à 0 px de large par la mise en page, donc invisible à 375 (61 px à 1440).",
 {"iconePx":48,"tuilePx":88,"parRangee":1,"nomAffiche":False,"largeurNom375":0,"largeurNom1440":61},"notion-icones-375.webp")
a(Q4,"apple.com","https://www.apple.com/fr/apps/",375,"Pas de grille : carrousel horizontal de cartes de 280 px (une carte et le bord de la suivante visibles), icône 56 px suivie du nom de l'app.",
 {"iconePx":56,"parRangee":"1 carte (+ amorce de la suivante)","nomAffiche":True,"largeurCarte":280},"apple-icones-375.webp")
Q5="5. Page avec sommaire latéral : alignement du h1"
a(Q5,"support.apple.com","https://support.apple.com/fr-fr/guide/mac-help/mchlp1066/mac",1440,"Pas de sommaire latéral permanent (la table des matières s'ouvre depuis un lien au-dessus du titre) ; h1 et texte alignés à gauche sur la même colonne de 817 px, elle-même centrée dans la page.",
 {"h1":{"x":312,"droite":1129,"textAlign":"left","fontSize":"40px"},"texte":{"x":312,"droite":1129},"sommaire":"lien « Table des matières » à x=312, fenêtre modale","centreColonne":720.5},"apple-sommaire-1440.webp")
a(Q5,"linear.app/docs","https://linear.app/docs/conceptual-model",1440,"Le h1 est aligné à gauche sur la colonne de texte (x=372), pas centré sur la page ; sommaire de navigation à gauche (0–280) et sommaire de la page à droite (1098–1348).",
 {"h1":{"x":372,"textAlign":"start","fontSize":"32px"},"texte":{"x":372,"droite":1022,"largeur":650},"sommaireGauche":{"x":0,"droite":280},"sommaireDroite":{"x":1098,"droite":1348}},"linear-sommaire-1440.webp")
a(Q5,"manual.raycast.com","https://manual.raycast.com/snippets",1440,"Le h1 est aligné à gauche sur la colonne de texte (x=335), à 75 px du sommaire latéral (0–260).",
 {"h1":{"x":335,"textAlign":"start","fontSize":"36px"},"texte":{"x":335,"droite":1115,"largeur":780},"sommaire":{"x":0,"droite":260,"liens":94}},"raycast-sommaire-1440.webp")
Q6="6. Listes FAQ / questions dépliables"
a(Q6,"raycast.com","https://www.raycast.com/pricing",1440,"Questions séparées par un filet 1 px sous chaque item (rendu ≈ blanc 10 % sur fond noir), sans espace ni carte entre items ; items de 103 px.",
 {"separation":"border-bottom 1px","ecartEntreItems":0,"hauteurItem":103,"largeur":700,"fond":"transparent","rayon":0},"raycast-faq-1440.webp")
a(Q6,"notion.com","https://www.notion.com/fr/pricing",1440,"Éléments <details> séparés par un filet 1 px noir 10 % en bas, sans espace entre eux ; items de 57 px.",
 {"separation":"border-bottom 1px rgba(0,0,0,0.1)","ecartEntreItems":0,"hauteurItem":57,"largeur":800,"element":"details/summary"},"notion-faq-1440.webp")
a(Q6,"apple.com","https://www.apple.com/fr/apple-one/",1440,"Questions en liste, séparées par un filet 1 px blanc 20 % sous chaque item, sans carte ni espace ; icône ⊕ à droite.",
 {"separation":"border-bottom 1px rgba(255,255,255,0.2)","ecartEntreItems":0,"hauteurItem":"76 (111 sur deux lignes)","largeur":654},"apple-faq-1440.webp")
a(Q6,"obsidian.md","https://obsidian.md/pricing",1440,"Questions séparées par un filet 1 px gris #262626 en bas, sans espace ni carte ; items de 77 px.",
 {"separation":"border-bottom 1px rgb(38,38,38)","ecartEntreItems":0,"hauteurItem":77,"largeur":672},"obsidian-faq-1440.webp")
a(Q6,"tailscale.com","https://tailscale.com/pricing",1440,"Éléments <details> séparés par un filet 1 px #EEEBEA en haut (et en bas du dernier), sans espace ; items de 49 px.",
 {"separation":"border-top 1px rgb(238,235,234)","ecartEntreItems":0,"hauteurItem":49,"largeur":638,"element":"details/summary"},"tailscale-faq-1440.webp")
a(Q6,"culturedcode.com/things","https://culturedcode.com/things/support/",1440,"Aucune liste de questions dépliables trouvée sur la page d'assistance de Things.",{"declencheursTrouves":0},None)
Q7="7. Journal des versions : images"
a(Q7,"linear.app","https://linear.app/changelog",1440,"Toutes les images à la même largeur affichée (624 px, une seule colonne), natives de 2400 à 3904 px (×4 à ×6) ; ratios proches de 16:9 à 3:2 ; mises en scène recadrées sur la nouveauté (objet sur fond sombre), pas de fenêtres entières.",
 {"largeurAffichee":624,"largeursNaturelles":[3904,3600,3600,2400,3600,3600],"rapport":"×3,8 à ×6,3","ratios":["2,22","1,71","1,67","1,67","1,73","1,80"],"videos":"622x350 (1920x1080)"},"linear-changelog-1-1440.webp")
a(Q7,"raycast.com","https://www.raycast.com/changelog",1440,"Largeur fixe 760 px ; chaque version ouvre sur une bannière 1720×630 identique de format, puis des captures recadrées sur la nouveauté (ex. menu de la barre des menus avec un bout de bureau, 1250×998), pas des fenêtres entières.",
 {"largeurAffichee":760,"banniereNaturelle":"1720x630 (×2,26)","captureNaturelle":"1250x998 (×1,64)","bannieresMemeFormat":"10 sur 10"},"raycast-changelog-2-1440.webp")
a(Q7,"notion.com","https://www.notion.com/fr/releases",1440,"Largeur fixe 667 px pour images et vidéos ; ratios alternant 16:9 et 4:3 ; natives de 960 à 3840 px ; illustrations et vues recadrées sur la fonction plutôt que l'app entière.",
 {"largeurAffichee":667,"largeursNaturelles":[1280,2400,1200,960,1200,1200,3840,2400],"ratios":["16:9","4:3","1,82"],"videos":"667x417 (1440x1080)"},"notion-changelog-1-1440.webp")
Q8="8. Mode sombre (prefers-color-scheme)"
q8=json.load(open('q8.json'))
names={"brew":"brew.sh","rustup":"rustup.rs","raycast":"raycast.com","things":"culturedcode.com/things","apple":"apple.com","applesupport":"support.apple.com","linear":"linear.app","notion":"notion.com","obsidian":"obsidian.md","tailscale":"tailscale.com"}
for o in q8:
  l,d=o['light'],o['dark'];lum=o['diffPixels'].split()
  if o['change']: obs=f"Suit prefers-color-scheme : fond {l['fondBody']} en clair, {d['fondBody']} en sombre."
  else:
    theme="sombre" if int(lum[0])<80 else "clair"
    obs=f"Ne suit pas prefers-color-scheme : page identique dans les deux modes, toujours {theme} (fond {l['fondBody'] if l['fondBody']!='transparent' else l['fondCentre']})."
  a(Q8,names[o['site']],o['url'],1440,obs,{"suit":o['change'],"luminanceMoyenneClair":int(lum[0]),"luminanceMoyenneSombre":int(lum[1]),"fondClair":l['fondBody'],"fondSombre":d['fondBody'],"texteClair":l['couleurTexte'],"texteSombre":d['couleurTexte'],"colorScheme":l['colorScheme'],"reglesMediaDark":l['reglesDark']},o['capture'])
Q9="9. Typographie française"
q9=json.load(open('q9.json'))
nm={"apple":"apple.com","applesupport":"support.apple.com","applesupport-accueil":"support.apple.com","notion":"notion.com","notion-tarifs":"notion.com"}
for o in q9:
  av=o['avant'];nb=sum(v['U00A0'] for v in av.values());nf=sum(v['U202F'] for v in av.values());sp=sum(v['espace'] for v in av.values())
  g=f"{o['guillemetsFrancais']} guillemet(s) « » avec espace insécable U+00A0 à l'intérieur" if o['guillemetsFrancais'] else "aucun guillemet"
  obs=f"{o['apostropheCourbe']} apostrophes courbes ’ contre {o['apostropheDroite']} droites ; {nb} espaces insécables U+00A0 avant : ? !, {nf} fines U+202F, {sp} espaces simples ; {g}."
  a(Q9,nm[o['site']],o['url'],1440,obs,{"caracteresVisibles":o['caracteres'],"apostropheCourbe":o['apostropheCourbe'],"apostropheDroite":o['apostropheDroite'],"avantPonctuation":av,"guillemetsFrancais":o['guillemetsFrancais'],"apresGuillemetOuvrant":o['apresOuvrant'],"guillemetsAnglais":o['guillemetsAnglaisCourbes'],"guillemetsDroits":o['guillemetsDroits']},None)
Q10="10. Page confidentialité / données"
a(Q10,"apple.com","https://www.apple.com/fr/privacy/",1440,"Page vitrine, pas un texte juridique : 7 intertitres h2 très grands (72 px) et 17 h3, en blocs visuels par app ou fonction ; 1 tableau.",
 {"h2":7,"h3":17,"h2Taille":"72px","tableaux":1,"listes":5,"mots":762,"sommaire":False},"apple-confidentialite-1440.webp")
a(Q10,"apple.com (politique)","https://www.apple.com/fr/legal/privacy/fr-ww/",1440,"Politique en 12 intertitres h2 (32 px), dont le premier posé en question (« Que sont les données personnelles chez Apple ? »), sans tableau ni sommaire.",
 {"h2":12,"h3":1,"h2Taille":"32px","tableaux":0,"listes":1,"mots":509,"sommaire":False,"intertitres":["Que sont les données personnelles chez Apple ?","Vos droits en matière de confidentialité chez Apple","Données personnelles qu’Apple collecte auprès de vous","…"]},"apple-politique-confidentialite-1440.webp")
a(Q10,"raycast.com","https://www.raycast.com/privacy",1440,"Texte juridique de 3 866 mots en 12 sections numérotées (h2 24 px, « 1. Personal Data we collect »…) et 4 h3, avec 4 listes, sans tableau ni sommaire.",
 {"h2":13,"h3":4,"h2Taille":"24px","numerotees":True,"tableaux":0,"listes":4,"mots":3866,"sommaire":False},"raycast-confidentialite-1440.webp")
a(Q10,"linear.app","https://linear.app/privacy",1440,"Texte juridique de 3 644 mots en 10 h2 (32 px), 2 h3 et 17 h4, très découpé en listes (40), avec un sommaire de page ; pas de tableau.",
 {"h2":10,"h3":2,"h4":17,"h2Taille":"32px","tableaux":0,"listes":40,"mots":3644,"sommaire":True},"linear-confidentialite-1440.webp")
a(Q10,"notion.com","https://www.notion.com/fr/notion/privacy",1440,"L'adresse renvoie vers la page de connexion de Notion : page non observable sans compte.",{"accessible":False},None)
json.dump(R,open('/home/user/callrecorder-app/design/recos/graphisme-site/donnees/references.json','w'),ensure_ascii=False,indent=1)
print(len(R))
