# Callrecorder · site

Site statique publié par GitHub Pages depuis la branche `main`.

## Mise en production

Gildas a donné une autorisation permanente : pour ce site, Claude est autonome.
Après une modification, pousser la branche de travail, ouvrir la pull request et
la fusionner dans `main` sans demander confirmation. La mise en ligne suit toute
seule.

## Ce que Gildas a tranché ne revient pas

Un texte ou un titre changé exprès ne revient pas à son ancienne forme sans que Gildas le demande. Le 6 novembre 2026, une relecture a remis le titre long de l'accueil, raccourci par Gildas trois jours plus tôt. Avant de changer un texte, regarder d'où il vient (`git log -S '<texte>'`). Avant de fusionner : `python3 scripts/retours.py`, depuis la branche de travail. S'il signale un retour voulu, le dire dans le message d'un commit : « Revient sur <hash> : <raison> ».

## Les captures

Une capture garde la forme et la matière de ce qu'elle montre.

- **La forme** : une fenêtre, une pastille ou une capsule arrive avec son contour dans l'image (coins transparents), et prend la classe `decoupe`. Jamais de cadre, de bordure, d'arrondi imposé ni de fond rectangulaire autour : l'ombre suit le contour (`filter: drop-shadow`), jamais `box-shadow`. Un extrait de Réglages se détoure aussi, sur ses cartes (`scripts/detoure-carte.py`, classes `decoupe extrait`). Seule une image coupée en plein contenu, sans contour à elle, reste un rectangle encadré.
- **La matière** : le verre et le givre se photographient par-dessus un vrai contenu, pour qu'on voie ce qui transparaît. À plat, sur rien, ils deviennent un gris opaque. L'app : `SNAPSHOT_SERVER=1 PASTILLE_FOND=… calls snapshot-pastille`, puis `scripts/decoupe.py` dans callrecorder-app, qui réunit le contour et la matière.
- **La netteté** : un petit objet s'affiche à sa taille, en résolution double, jamais agrandi.
- Vérifier sur la page, sur fond clair et sur fond sombre si la page en a un.
