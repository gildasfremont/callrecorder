# Callrecorder · site

Site statique publié par GitHub Pages depuis la branche `main`.

## Mise en production

Gildas a donné une autorisation permanente : pour ce site, Claude est autonome.
Après une modification, pousser la branche de travail, ouvrir la pull request et
la fusionner dans `main` sans demander confirmation. La mise en ligne suit toute
seule.

## Ce que Gildas a tranché ne revient pas

Un texte ou un titre changé exprès ne revient pas à son ancienne forme sans que Gildas le demande. Le 6 novembre 2026, une relecture a remis le titre long de l'accueil, raccourci par Gildas trois jours plus tôt. Avant de changer un texte, regarder d'où il vient (`git log -S '<texte>'`). Avant de fusionner : `python3 scripts/retours.py`, depuis la branche de travail. S'il signale un retour voulu, le dire dans le message d'un commit : « Revient sur <hash> : <raison> ».

## Les données reçues par le site

Les messages (`note.js`) et les visites (`visite.js`) partent à `callrecorder-notes`, sur Vercel, rangés dans Redis (Upstash). Le journal d'installation et le bilan du jour de l'app vont à `callrecorder-logs`, dans un Blob Vercel privé. Le 9 novembre 2026, Gildas a demandé s'il fallait plutôt se servir de Google Drive :

- **Pour recevoir, non.** Drive n'accepte que des écritures authentifiées : un accès posé dans le site ou dans l'app ouvrirait tout son Drive. L'intermédiaire possible, Apps Script et un Google Sheet, répond toujours 200 (le 429 de `note.js` se perdrait) et ne sait pas compter les visiteurs uniques sans garder leur empreinte. La page Confidentialité promet « Vercel, à Paris ».
- **Pour lire, oui.** Redis et Blob ne se lisent qu'à travers l'app ; dans Drive, Gildas les ouvre sur son téléphone et Claude les lit par le connecteur. La piste : Callrecorder, qui relève déjà messages et visites, en écrit une copie dans un dossier de Drive (à faire dans callrecorder-app).
- **Pour les autres projets** : Drive ou Sheets quand c'est Gildas ou ses machines qui écrivent, peu, et qu'il veut voir ou corriger à la main ; une vraie base quand des inconnus écrivent, qu'on compte, ou qu'on a promis où sont les données.

## Le logo et le nom

Les règles sont dans `DESIGN.md › Logo et nom` du dépôt de l'app (callrecorder-app). Le cartouche se pose par `<span class="marque">callrecorder</span>`, jamais redessiné ailleurs ; une icône est l'un des fichiers de `marque/icone/` de l'app, recopié tel quel ; « Callrecorder » dans le texte. Avant de fusionner, depuis la branche de travail : `python3 ~/callrecord/scripts/marque.py --site .` (s'il dit un écart, le corriger).

## Les captures

Une capture garde la forme et la matière de ce qu'elle montre.

- **La forme** : une fenêtre, une pastille ou une capsule arrive avec son contour dans l'image (coins transparents), et prend la classe `decoupe`. Jamais de cadre, de bordure, d'arrondi imposé ni de fond rectangulaire autour : l'ombre suit le contour (`filter: drop-shadow`), jamais `box-shadow`. Un extrait de Réglages se détoure aussi, sur ses cartes (`scripts/detoure-carte.py`, classes `decoupe extrait`). Seule une image coupée en plein contenu, sans contour à elle, reste un rectangle encadré.
- **La matière** : le verre et le givre se photographient par-dessus un vrai contenu, pour qu'on voie ce qui transparaît. À plat, sur rien, ils deviennent un gris opaque. L'app : `SNAPSHOT_SERVER=1 PASTILLE_FOND=… calls snapshot-pastille`, puis `scripts/decoupe.py` dans callrecorder-app, qui réunit le contour et la matière.
- **La netteté** : un petit objet s'affiche à sa taille, en résolution double, jamais agrandi.
- Vérifier sur la page, sur fond clair et sur fond sombre si la page en a un.

## Les contrôles avant de fusionner

Depuis la branche de travail, en plus de `retours.py` et `marque.py` :

- `python3 scripts/contraste.py` : chaque jeton de texte tient 4,5:1 sur chaque fond, et `--edge` 3:1, en clair et en sombre (S06). Une couleur nouvelle devient un jeton de `:root`, et de son pendant sombre.
- `python3 scripts/images.py --verifie` : chaque `<img>` déclare `width` et `height`, chaque grande image a son `srcset` (S02, S18). Sans `--verifie`, il refait les variantes réduites (`nom-<largeur>w.webp`) après qu'une image a changé.
- `python3 scripts/typo.py` : apostrophes courbes, insécables avant `: ; ? ! › »` (S35, S11).

Le sombre suit le système sur les pages qui déclarent `<meta name="color-scheme" content="light dark">` : toutes, depuis le 10 novembre 2026, pages de version comprises. `dossiers.py` (callrecorder-app) reprend l'en-tête de `versions/index.html` pour chaque page de version qu'il refait (balise `color-scheme`, numéro de cache de `style.css`), et recopie sa propre feuille, `dossiers/commun/version.css`, sur `versions/version.css` : cette feuille se modifie dans l'app, jamais ici seulement, sinon la publication suivante l'efface. Les couleurs d'un schéma (`.dz-schema`) restent écrites en clair dans le dessin ; `versions/version.css` leur donne le jeton qui répond en sombre, une couleur nouvelle dans un schéma s'y ajoute.
