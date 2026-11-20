# Installer Callrecorder, pour l'agent qui aide

Tu es l'agent dans lequel la personne a collé le message du site. Fais le moins d'opérations possible pour elle, et dis-lui clairement ce qui va se passer.

1. **Dis d'abord si tu pourras lire sa mémoire.** Callrecorder la donne aux agents qui tournent sur ce Mac : Claude (l'app), Claude Code, Codex. Dans un navigateur, tu ne le peux pas : dis-lui d'ouvrir ton app, ou l'un de ceux-là.
2. **Vérifie le Mac** : puce Apple (`uname -m` = `arm64`), macOS 15 ou plus récent.
3. **Installe.** Si tu as un shell, lance la ligne toi-même ; sinon, donne-la à coller dans le Terminal (⌘ Espace, « Terminal », Entrée) :

   `curl -fsSL https://github.com/gildasfremont/callrecorder/releases/latest/download/install.sh | zsh`

4. **Passe la main à l'app.** Lancée par toi, l'installation ouvre Callrecorder devant la personne, qui demande le micro, le son des apps, puis l'écran (facultatif). La personne clique sur Autoriser ; pour l'écran, macOS lui demande aussi Touch ID ou son mot de passe, préviens-la. Toi, tu ne touches pas aux réglages de macOS. Collée dans le Terminal, c'est le Terminal qui la guide.
5. **Dis comment te retrouver.** Ton accès arrive au prochain lancement : Claude Code et Codex voient Callrecorder dans une nouvelle conversation, l'app Claude une fois quittée et rouverte. Si tu ne le vois pas, la personne te relie dans Callrecorder, Réglages › Agents. Après son prochain appel, elle peut t'écrire : « Résume ma dernière conversation ».
6. **Un souci ?** Demande le texte de l'erreur (Terminal ou app). Il ne contient que du technique.
