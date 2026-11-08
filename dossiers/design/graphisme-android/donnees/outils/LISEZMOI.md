# Outils du relevé

Rien ici ne change le code de l'app. Pour refaire les mesures :

1. Copier `phone/android` hors du dépôt, appliquer `patch_banc.py` à la copie de `BancTest.kt`, y ajouter les fichiers de `banc/`.
2. Dans la copie : `phone/android/gradlew testDebugUnitTest --tests '*Releve*' --tests '*BancTest*'`. Les relevés JSON sortent dans `app/build/releve/<variante>/`, les images dans `app/build/banc/<variante>/`.
3. `python3 inventaire.py` (lecture statique du code), `python3 mesures.py` (contrastes, cibles, sémantique), `python3 preuves.py` (captures annotées).
4. `cd dossier && python3 build.py` refait les pages HTML.

Les chemins en tête des scripts pointent vers la copie (`/tmp/claude-0/releve`) : les adapter.
