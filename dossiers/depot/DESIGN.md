# Design

Ce qui fait que Callrecorder se ressemble d'un écran à l'autre : les principes, les valeurs et les composants de l'app, du site et du téléphone. Ce document décrit ce qui existe (relevé du 2026-11-05, vérifié contre le code le 2026-11-06). Il suit le code : si une valeur change, on change la ligne ici dans le même commit.

Avant d'écrire une vue, on relit ce document ; avant d'ajouter une valeur, on cherche si son rôle en a déjà une. **Une seule valeur par rôle**, jamais un chiffre recopié d'un fichier à l'autre.

## Principes

- **Le plus simple d'abord, creusable ensuite.** L'interface dit quelle conversation et qui a dit quoi. Le détail se trouve dans l'app, derrière un seul geste cohérent (un « … », un survol, un repli). L'agent, par le MCP, en sait encore plus. Pas de « (?) » semés partout.
- **Montrer le final, garder le reste sur le disque.** Une seule transcription affichée, jamais la liste des versions ni les essais.
- **Zéro bouton inutile.** Un automatisme vaut mieux qu'un bouton, et un bouton vaut mieux qu'une étape de configuration.
- **Pas de filets.** On sépare par l'espacement, le regroupement et les fonds : un bloc se lit comme une masse. Seuls les menus gardent leurs séparateurs natifs. Deux exceptions voulues : le liseré d'une vignette, sans lequel une capture claire perd ses bords sur un fond clair, et le filet d'un silence de 15 secondes ou plus dans la transcription, qui coupe le fil comme un changement de jour dans une messagerie.
- **Une app du système.** Polices, couleurs de texte, couleur d'accent, listes et barres d'outils viennent de macOS, et les comportements imitent ceux de Finder, Calendrier ou Photos. On ne dessine que ce que macOS ne donne pas.
- **Un texte qui explique un bloc avoue souvent une interface ratée.** On améliore l'interface avant d'écrire.

## App Mac

Tout est dans `Sources/CallRecorder`. Le minimum est macOS 15 ; le verre et les effets de bord de défilement sont réservés à macOS 26, avec un repli.

### Texte

| Rôle | Valeur |
|---|---|
| Lecture : répliques, notes, transcription en direct | `Reading.font`, 14 pt, interligne 5 |
| Interface courante | `.callout` |
| Libellé, nom, titre de bloc | `.callout.weight(.semibold)` |
| Information secondaire | `.caption` |
| Heures, durées, nombres | `.monospacedDigit()` sur le style voisin |
| Grand chiffre d'une jauge | `StorageBar.figure`, `.title` semi-gras |

La police est celle du système. Les couleurs de texte sont `.primary`, `.secondary` et `.tertiary`.

### Couleurs

Les fonds neutres sont tous `Color.primary` en opacité, pour suivre le clair et le sombre sans rien définir deux fois.

| Rôle | Valeur | Opacité |
|---|---|---|
| Carte | `Card.fill` | 0,05 |
| Vignette sans capture | `Thumb.fill` | 0,05 |
| Survol | `Hover.fill` | 0,06 |
| Pastille au repos : filtre, recherche, rond derrière une icône | `Chip.fill` | 0,07 |
| Carte survolée | `Card.hover` | 0,08 |
| Liseré d'une vignette | `Thumb.edge` | 0,10 |
| Appui | `Hover.pressed` | 0,11 |
| Ce qui est choisi | `Chosen.fill` | 0,12 |
| Part d'une jauge | `StorageBar.part` | 0,18 |
| Part choisie d'une jauge | `StorageBar.chosen` | 0,42 |

| Rôle | Valeur |
|---|---|
| Accent : ligne choisie, lecture en cours, progression, ce qu'un geste rendrait | `Color.accentColor`, celui du système |
| En cours, REC | `Palette.live` |
| Attention | `Palette.warning` |
| Fait, prêt | `Palette.success` |
| « Moi » | `TranscriptReaderView.me`, bleu |
| La personne en face | `TranscriptReaderView.them`, orange |
| Voix d'une réunion en salle | `voices` : vert, violet, rose, sarcelle, indigo |
| Mots trouvés dans une réplique | `NSColor.findHighlightColor`, le texte en noir |
| L'occurrence où l'on en est, parmi eux | `NSColor.systemOrange`, le texte en noir |

Le bleu et l'orange sont réservés à « Moi » et à la personne en face, et se distinguent aussi par leur clarté. Il n'y a pas un seul bleu partout, et c'est voulu : l'accent de l'app reste celui du système, « Moi » a un bleu plus soutenu pour se lire à 13 points (`#0060DF`), et le site garde le sien (`#0064d2`). Les couleurs de `Palette` servent au texte : elles tiennent 4,5:1 en petit sur fond clair, davantage avec « Augmenter le contraste », et reprennent les couleurs du système sur fond sombre.

### Espacements et formes

Les espacements n'ont pas de nom, mais une échelle : **4, 6, 8, 10, 12, 16, 20 et 24**, celle que le code emploie déjà le plus ; 12 est le plus fréquent. Tout nouvel espacement la suit. Les valeurs isolées (1, 3, 5, 7, 11, 28) s'y ramènent quand on retouche leur vue.

| Rôle | Valeur |
|---|---|
| Carte | rayon `Card.radius`, 12 |
| Ligne ou bouton à fond arrondi | rayon `Row.radius`, 8 |
| Vignette | rayon `Thumb.radius`, 5 |
| Pastille flottante, recherche | `Capsule` |
| Icône de barre d'outils | `BarIconSize.font`, 18 |
| Bouton rond | `BarIconSize.round`, 36 |
| Cartouche d'une icône sur le panneau de la colonne | `BarIconSize.cartouche`, 36×28 |
| Bouton ⋯ | `MoreButton.size`, 24 |
| Vignettes en 16:10 | `Thumb.row` 48×30, `Thumb.strip` 84×52, `Thumb.transcript` 160×100 |
| Colonne de lecture | `TranscriptReaderView.readingWidth`, texte à environ 720 pt |
| Bord gauche du titre, du lecteur et des avatars | `TranscriptReaderView.inset`, 20 |

### Verre

Le verre est réservé à ce qui flotte au-dessus du contenu : boutons de la barre d'outils, lecteur, actions d'un passage. On ne pose pas de verre sur du verre : un bouton de la colonne reste sans contour sur le panneau, et ne prend du verre que lorsqu'il flotte sur l'appel. Avant macOS 26, le repli est `.regularMaterial`.

### Mouvement

| Rôle | Valeur |
|---|---|
| Survol et appui | `Hover.fade`, 0,12 s, `easeOut` |
| Animation générale | `Motion.or(…)` |
| Glissement | `Motion.slide(edge)` |
| Grossissement | `Motion.pop` |

Toute animation passe par `Motion`, qui respecte « Réduire les animations » : le mouvement devient un fondu, et plus rien ne pulse.

### Composants

| Composant | Où | Usage |
|---|---|---|
| `.windowBar(…)` | `WindowBar.swift` | Le haut d'une page : retour, logo, titre, actions |
| `ScrollEdge` | `WindowBar.swift` | Le flou de ce qui défile sous la barre |
| `CircleGlass` | `WindowBar.swift` | Bouton rond de barre d'outils |
| `.buttonStyle(.hover(radius))` | `Hover.swift` | Ligne ou bouton sans bordure, à fond arrondi |
| `.buttonStyle(.hoverCircle)` | `Hover.swift` | Icône seule, un rond au survol |
| `.buttonStyle(.dim)` | `Hover.swift` | Bouton déjà coloré, qui fonce au survol |
| `.buttonStyle(.thumb(radius))` | `Hover.swift` | Vignette de capture, liseré au survol |
| `HoverPlate` | `Hover.swift` | Fond de survol d'une ligne, seul à se redessiner |
| `.readingCard(…)` | `TranscriptReader.swift` | Carte de la colonne de lecture, grise ou en verre |
| `FloatingGlass` | `TranscriptReader.swift` | Pastille flottant sur le texte |
| `PastilleController` | `Pastille.swift` | Pastille volante d'un enregistrement : point rouge, chrono, Capturer, Arrêter, hauteur 40, par-dessus tous les bureaux. Se déplace, garde sa place, ne prend ni le clavier ni le premier plan, reste hors des partages d'écran. Masquable dans les Réglages |
| `StoragePage` | `StoragePages.swift` | Espace occupé : une page, la jauge de l'audio, ses parts en capsules, les gestes en dessous |
| `TranscriptSkeleton` | `TranscriptReader.swift` | Répliques en gris pendant la transcription |
| `.problemAlert(…)` | `Accessibility.swift` | Alerte à un seul bouton, qui informe |

`BarIcon` et `PillButton` (`TranscriptReader.swift`), `PanelIcon` et `HoverCapsule` (`ColumnTools.swift`) existent aussi, mais sont privés à leur fichier.

### Listes

Une liste est en `.listStyle(.sidebar)`, avec `.listRowSeparator(.hidden)`.

## Site

La source du site est le dépôt public `gildasfremont/callrecorder`, qu'on modifie directement ; le dossier `site/` de ce dépôt-ci est une copie en retard. Tout est dans son `style.css`, en thème clair uniquement : l'interface d'un utilitaire macOS sur un fond bleu très pâle.

| Variable | Valeur | Rôle |
|---|---|---|
| `--window` | `#edf2f8` | Fond de page |
| `--group` | `#ffffff` | Groupes |
| `--text` | `#142338` | Titres, texte fort (le bleu nuit de la marque) |
| `--body` | `#2c3a50` | Texte courant |
| `--secondary` | `#566175` | Texte secondaire |
| `--accent` | `#0064d2` | Liens, bouton principal |
| `--border` | `rgba(20,40,80,.14)` | Contours |
| `--separator` | `#d9e2ee` | Séparateur des lignes de groupe |
| `--mono` | police à chasse fixe du système | Code, noms de fichiers |
| `--display` | Host Grotesk | Titres, en graisse moyenne |

Le texte courant est dans la police du système, en 17 px, interligne 1,55. La largeur est `.wrap` (1080 px) ou `.col` (760 px), avec une gouttière de 16 px. Le point de rupture habituel est 640 px. Les boutons sont `.button`, `.button.default`, `.button.large` et `.button.hero`. Le site respecte `prefers-reduced-motion`.

**Images** : captures en WebP sans perte (`cwebp -quiet -lossless -z 9`), illustrations en WebP (`cwebp -q 92 -alpha_q 100`), aperçus de partage en JPEG 1200×630. La vignette d'une version montre sa nouveauté, et n'est jamais écrasée (`img/versions/`).

## Captures

Partout où l'app est montrée (site, journal des versions, guides, maquettes), une capture garde la forme et la matière de ce qu'elle montre.

- **La forme** : l'image porte le contour de l'objet, coins transparents compris. Pas de cadre, de bordure, d'arrondi imposé ni de fond rectangulaire autour. L'ombre suit ce contour (`drop-shadow`), jamais `box-shadow`. Une carte de Réglages se détoure sur la carte (`scripts/detoure-carte.py`). Seule une image coupée en plein contenu reste un rectangle.
- **La matière** : le verre et le givre se photographient par-dessus un vrai contenu, puisque c'est ce qui transparaît qui les rend visibles. Pris sur rien, ils sortent en gris opaque. `PASTILLE_FOND=<image>:<x>:<y>` avec `snapshot-pastille` donne la vraie matière de macOS, `scripts/decoupe.py` la réunit au contour.
- **La netteté** : un petit objet s'affiche à sa taille, en résolution double, jamais agrandi. Son ombre reste à son échelle.
- **Le contrôle** : `scripts/controle-captures.py <site>` refuse une image à contour encadrée en rectangle.

## Téléphone

L'app Android (`phone/android`) ressemble à l'app Mac en restant une app Android : la police du téléphone (Roboto), le retour, les cibles d'au moins 48 dp. Ses valeurs sont dans `Look.kt` ; les pièces communes dans `Screen.kt`, et chaque écran dans son fichier, qui n'y fixe que ses tailles de texte. Il n'y a pas d'app iPhone.

- **Fond et texte** : fond `#F5F5F5` (`#1E1E1E` en sombre), texte `#1D1D1F`, et tout le reste en opacités du texte, comme sur le Mac : carte 0,05, bouton 0,07, toucher 0,12, secondaire 0,6, titre de groupe 0,56. Accent `#0064D2`, avertissement `#A0470A`, enregistrement `#C41E14`.
- **Formes** : carte rayon 12, ligne et vignette rayon 8, pastille en capsule ; pas de filets.
- **Accueil** : le panneau de la barre des menus du Mac, sans bandeau d'état. En haut, la barre de la fenêtre Conversations : Liste ou Calendrier dans une capsule, Rechercher à droite. La liste par jour, une vignette de 44 dp devant chaque conversation, qui dit ce qu'elle était, comme sur le Mac : le logo de l'app d'un appel (WhatsApp, Signal, Telegram, Meet), d'une couleur, à celle de sa marque ; un combiné pour un appel du réseau mobile ; deux personnes, au trait, pour une réunion ; le micro pour le reste. Avant le texte du Mac, le téléphone le tire de son propre enregistrement. La même vignette, en 36 dp, dans l'en-tête d'une conversation, et devant chaque résultat de recherche (`Screen.kindIcon`). Ce qui enregistre est dans la liste, en rouge (« ● En cours ») ; l'écoute, en tête, en bleu (Journal, « ● Écoute depuis 08:12 »). En pied, des lignes de toute la largeur, une icône devant : Enregistrer une réunion et Réglages, ou Arrêter l'enregistrement (rouge) et Prendre une photo.
- **Pastille volante** (`Pastille.kt`) : pendant un enregistrement, hors de l'app et de l'écran verrouillé, Prendre une photo et Arrêter en icônes seules, sur une capsule `Look.floating`, deux cibles de 48 dp. Glisser la déplace, toucher agit. Une fenêtre d'accessibilité : elle demande le service des appels (Réglages › Accessibilité). Pendant un appel enregistré, elle tient aussi le micro ; là où elle ne se montre pas (écran verrouillé, app ouverte), un point rouge de 12 dp, en haut à droite, la remplace.
- **Une conversation** : un seul lecteur en carte, tant que le son léger est là, puis les répliques, un rond à initiales devant (accent pour Moi, avertissement pour les autres). En bas, la barre flottante, seul « verre » de l'écran : Rechercher, Copier, Télécharger, Détails. Supprimer est dans le menu ⋯.
- **Réglages** : des groupes en masses, un titre de groupe au-dessus. Ce qui empêche quelque chose est un encadré couleur avertissement, avec son bouton.
- **Mise en route** : une seule étape au centre, l'icône ronde (64 dp), une phrase, un bouton plein.
- **Ce qui reste d'Android** : les boîtes de dialogue (autorisations, Supprimer, Détails, « Relier ce téléphone à … ? » pour le code d'un autre Mac) et la page Accessibilité.
- **Notifications** : Android les dessine ; l'app n'en choisit que la petite icône (le micro de l'icône, en silhouette, `micro_notif.xml`), l'accent `#0064D2`, les textes et les boutons. Elle ne parle que quand l'app enregistre : Écoute, immobile ; Enregistre, avec une barre qui file sous le texte, jamais de rouge. Au repos, Prêt, réduite au minimum (Android l'exige). Le reste est une action, montrée quand un contexte la rend nécessaire, et qui dit pourquoi maintenant. Jamais le déclenchement : il se voit et se change dans les Réglages.
- **Icône de l'app** : une icône adaptative (`mipmap-anydpi-v26/ic_launcher.xml`) : le micro, petit, sur un fond blanc, calculé par `scripts/icone.swift`. Réduit les yeux mi-clos : le mot de la plaque, illisible à cette taille, n'y est plus qu'une bande à peine plus claire, et pas de silhouette pour les icônes à thème, comme Netflix ou Alan : l'icône garde sa matière.

## Marque

[marque/README.md](marque/README.md) fait référence : le cartouche par défaut, l'icône micro dans l'app et là où la place manque, une silhouette monochrome quand le système n'accepte qu'une teinte. Dans le texte, on écrit « Callrecorder ». « CallRecorder » reste aux noms techniques.

## Textes

[TEXTES.md](TEXTES.md) dit comment l'app parle : les principes, le vocabulaire, la forme de chaque élément. On le relit avant d'écrire un mot visible.

## Écarts connus

- **Des tailles de texte et des espacements en dur.** Environ 31 lignes fixent une taille de police à la main, et les `padding` hors échelle restent à ramener. On les corrige en retouchant chaque vue : une reprise d'un seul coup entrerait en conflit avec les sujets en cours.
- **Des boutons d'icône en double** : `BarIcon` et `PanelIcon` dessinent le même carré de 36 points, chacun dans son fichier.
- **Des filets sur le site** : `.row + .row` et `.claude .bar`, ce dernier imitant la fenêtre de Claude.
- **Des couleurs en dur dans le CSS**, hors variables : les dégradés et ombres de `.button`, par exemple.
- **Android sans valeurs partagées avec le Mac** : `Look.kt` recopie les couleurs du Mac au lieu de les lire d'une source commune.
- **Les noms du code** (`CallsWindow`, `CallsWindowController`) disent encore « Appels » ; la fenêtre, elle, s'appelle « Conversations ».
