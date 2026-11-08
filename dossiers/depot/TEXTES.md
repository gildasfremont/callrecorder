# Textes

Comment Callrecorder parle, dans l'app, sur le téléphone et sur le site. Ce document suit [DESIGN.md](DESIGN.md) : on le relit avant d'écrire un mot visible.

Callrecorder fonctionne en arrière-plan et garde ce que les gens se disent. La personne qui lit un texte de l'app est donc occupée à autre chose, et elle nous confie quelque chose de sérieux. Tout ce qui suit en découle.

## D'abord, ne pas écrire

Avant d'ajouter un texte, dans cet ordre :

1. L'interface peut-elle le dire à sa place ? Si oui, on corrige l'interface.
2. Un label suffit-il ? Si oui, on s'arrête là.
3. Sinon, une phrase, celle qui change ce que la personne va faire ou penser.

## Les principes

### 1. L'attention est ce qu'on protège

Chaque mot coûte de l'attention à quelqu'un qui pensait à autre chose, et il fait concurrence à l'information utile. Les gens balaient une interface plus qu'ils ne la lisent : un texte long n'est pas mal lu, il n'est pas lu.

- Un texte doit gagner sa place : si on l'enlève, que perd la personne ?
- On écrit, puis on retire la moitié des mots, puis on recommence.
- On ne dit pas deux fois la même chose dans une vue : le titre, le label et le bouton ne se répètent pas.
- Un sous-titre n'est pas une place à remplir. S'il y en a un, il liste les objets de la page ou donne la seule information absente de la vue.

### 2. L'interface parle avant le texte

Une porte qui a besoin d'une pancarte est une porte ratée. Un texte qui explique un bloc signale un problème de conception : soit l'interface n'est pas bonne et il faut l'améliorer, soit le texte ne sert pas.

- Pas de méta-titre (« Comment ça marche »), pas de phrase qui annonce ce qui suit, pas de légende d'une évidence.
- Pas d'explication d'un bouton dont le label est clair. Une action qui compte se lit sur le contrôle lui-même.

### 3. On parle depuis la situation de la personne, pas depuis la machine

La personne se demande ce que ça change pour elle et ce qu'elle doit faire. Elle ne se demande pas comment nous avons construit l'app. Le code a ses mots (piste, MCP, frames, timbre), elle a les siens.

**Le mécanisme se tait, la conséquence se dit.** C'est la règle qui tranche les cas difficiles :

- « ce Mac, s'il est libre et joignable, ouvre son micro aussi » décrit un mécanisme : on l'enlève.
- « Le débogage sans fil reste allumé sur le téléphone » est une conséquence pour la personne : on la garde, même si tout le reste part.
- Le même raisonnement vaut pour ce qui quitte le Mac, ce qui est gardé, ce qui est effacé et ce qui consomme la batterie. Une action qui a des conséquences pour la personne ne se fait jamais sans le lui dire.

### 4. Le texte engage

Callrecorder est une mémoire : on la croit ou on ne s'en sert pas. Un petit texte faux abîme la confiance dans tout le reste.

- L'état affiché est celui du moment. Une notification ne dit pas « Votre réunion commence » si ce n'est pas le cas, et un bandeau ne dit pas « bientôt » pendant une heure.
- Pas de promesse plus large que le fait. On préfère « L'audio reste sur ce Mac » à « Rien ne quitte ce Mac » si une transcription peut partir. La transparence passe avant la formule rassurante.
- Une phrase sans sens est un bug (« Forme d'ombre ») et se traite comme tel.
- On écrit des faits précis, avec un nombre ou une date, plutôt qu'un adjectif.

### 5. L'incertitude reste en dessous, sauf si elle change une décision

Montrer un degré de confiance n'a de valeur que s'il modifie ce que la personne va faire. Un pourcentage sans contexte n'aide pas, et il peut faire douter de ce qui est juste.

- La transcription affiche « Marie », pas « Voix 2, probablement Marie ».
- Le degré de confiance, la preuve et la provenance vont au détail et au MCP.
- Quand le doute impose un choix, l'interface montre le choix (« Qui est cette voix ? »), pas un score.

### 6. Le plus simple d'abord, le détail à un geste

Ce qui s'affiche d'abord dit ce qui compte. Le reste existe, derrière un seul passage, et rarement plus de deux niveaux. Le texte suit ces trois niveaux : l'interface (quelle conversation, qui a dit quoi), le détail dans l'app (comment, par quel micro), l'agent (tout).

- Le label du passage annonce ce qu'on y trouve.
- Une explication qu'on ne se résout pas à supprimer se déplace au niveau du dessous.

### 7. Un adulte parle à un adulte

L'app écoute des conversations : elle ne plaisante pas, ne vend pas et n'inquiète pas. Le sérieux est calme, il n'est pas froid.

- Pas de bavardage amical, de formule accrocheuse ou d'effet de manche (« Comme ça, … »).
- Pas de mot qui fait peur quand un mot neutre existe.
- Le ton suit la situation : direct pour un problème, plus léger pour une tâche accomplie, comme les autorisations de la semaine renouvelées. La satisfaction vient du fait, pas d'une exclamation.

### 8. Un mot, un sens, partout

Un même objet porte le même nom dans l'app, sur le téléphone, sur le site et dans la consigne MCP. Changer de mot fait croire à un autre objet.

## Vocabulaire

| On écrit | Pour | Jamais |
|---|---|---|
| Conversation | Le terme général : appels, réunions, notes | Enregistrement, quand on parle du contenu |
| Appel | Un vrai appel, et rien d'autre | Appel pour une réunion ou une note |
| Interlocuteurs | Les personnes des conversations | Contacts, réservé à la source (Contacts du Mac) |
| Agents | Les assistants IA | Claude comme chapeau |
| Callrecorder | Le nom dans une phrase | CallRecorder, réservé aux noms techniques |
| Enregistrement : Manuel, Événements du calendrier, Tout le temps | Le réglage qui dit quand le téléphone enregistre seul (décidé par Gildas le 2026-11-06) | « Aux rendez-vous », « À la main », « Déclenchement » |

Sur le site, on parle de mémoire plutôt que d'enregistrement : « Souvenez-vous de tout », le titre court choisi par Gildas le 2026-11-03.

Un mot nouveau s'ajoute à ce tableau avant d'entrer dans l'interface, avec la décision de Gildas.

## Écrire en français

- **Vouvoiement**, jamais de tutoiement.
- **Ni « on » ni « nous »** dans l'interface : on ne sait pas qui parle. On nomme celui qui agit (« Android demande ce geste ») ou on dit le fait (« Impossible d'enregistrer la modification »).
- **Sujet et verbe, voix active.** Une phrase, une idée. Si elle demande un point-virgule ou une parenthèse, ce sont deux idées, et la seconde n'est peut-être pas nécessaire.
- **L'essentiel en premier** dans la phrase et dans la vue.
- **Du concret** : le français glisse vite vers l'abstrait, on revient à l'objet et au geste.
- **Peu de possessifs** : « Favoris » plutôt que « Vos favoris ».
- **« Pour » ou « pour que »** seulement si la raison change la décision de la personne. La phrase complète est la forme d'un texte, pas une obligation d'en écrire un.
- **Le bon geste selon l'appareil** : cliquer sur le Mac, toucher sur le téléphone.
- **Ponctuation** : pas de point final à un label, guillemets français « », pas de label de la forme « État : explication ».

## Par élément

| Élément | Forme | Exemple |
|---|---|---|
| Titre de page ou de groupe | Le nom de l'objet | Téléphones |
| Titre d'une page du site ou d'un parcours guidé | L'information elle-même | À l'installation, macOS bloque CallRecorder |
| Label de ligne | Quelques mots qui se suffisent | Notification après chaque appel |
| Bouton, entrée de menu | Un verbe à l'infinitif et son objet | Ajouter un téléphone |
| Détail d'une ligne | Rien. Sinon, une conséquence en une phrase | Le débogage sans fil reste allumé sur le téléphone. |
| Sous-titre de page | Rien. Sinon, la liste des objets | Agents, Google, Mac |
| Infobulle | Ce que fait le contrôle, en un groupe de mots | Rechercher dans la transcription |
| État, badge | Un mot ou deux, vrais à cet instant | Pas encore transcrite |
| Instruction de parcours | Une action par ligne, sans commentaire | Copiez la commande dans le Terminal. |
| Notification | Le fait, puis l'action si elle est attendue | Votre téléphone est prêt |
| Erreur | Ce qui s'est passé, puis quoi faire, sans code ni nom technique | Rien n'a été enregistré : aucun son n'est arrivé. |
| État vide | Ce qui manque et, s'il existe, le geste pour le remplir | Aucun téléphone relié |
| Confirmation | La conséquence, et un bouton qui reprend le verbe | Réunir 3 enregistrements en une conversation ? |

**Le site** peut donner envie, en disant le bénéfice direct plutôt que le procédé (« oubliez d'enregistrer »). Il reste soumis aux principes 4 et 7 : rien d'exagéré, pas d'effet de manche, et des exemples de métiers ordinaires, pas de startups.

**La consigne MCP** s'adresse à des agents. Elle peut tout dire, puisque le principe 1 ne protège pas leur attention de la même façon, mais elle garde le vocabulaire.

## Avant de livrer

1. Masquer tout texte secondaire de la vue : se comprend-elle encore ? Sinon, on corrige l'interface.
2. Pour chaque texte restant : si on l'enlève, que perd la personne ?
3. Y a-t-il un mot du code ? Un mécanisme qui n'est pas une conséquence ?
4. Est-ce vrai à cet instant, dans chaque branche et chaque canal ? Si la fonction change, qui relit ce texte ?
5. Lire à voix haute : une personne calme parlerait-elle ainsi à quelqu'un qu'elle respecte ?

## Sur quoi ça s'appuie

Les principes viennent des retours de Gildas (22 octobre au 5 novembre 2026), confrontés à ces lectures :

- [Apple, Writing](https://developer.apple.com/design/human-interface-guidelines/writing) : chaque mot doit être nécessaire, le ton suit la situation, pas de « nous », labels à verbe, pas de label trop malin.
- [NN/g, dix heuristiques](https://www.nngroup.com/articles/ten-usability-heuristics/) : statut visible, aucune conséquence sans en informer, langage de l'utilisateur, minimalisme, l'idéal sans aide.
- [NN/g, divulgation progressive](https://www.nngroup.com/articles/progressive-disclosure/) : le premier niveau dit ce qui compte, deux niveaux au plus, un passage bien nommé.
- [Microsoft, User Interface Text](https://learn.microsoft.com/en-us/windows/win32/uxguide/text-ui) : le texte est balayé, on ne se répète pas, l'important va sur le contrôle. Guide de l'époque de Windows 7, dont les principes tiennent.
- [Amber Case, Calm Technology](https://www.caseorganic.com/post/principles-of-calm-technology) : le moins d'attention possible, informer sans sortir la personne de ce qu'elle fait.
- [Google PAIR, Explainability + Trust](https://pair.withgoogle.com/chapter/explainability-trust/) : montrer une confiance seulement si elle change la décision, se méfier des pourcentages.
- [Coding Horror, Happy Talk Must Die](https://blog.codinghorror.com/happy-talk-must-die/), sur le bavardage selon Steve Krug.
- [Canada, Avant de rédiger](https://www.canada.ca/fr/emploi-developpement-social/programmes/directives-reglements-canadien-accessibilite/langage/avant-redaction.html) : langue courante, l'essentiel d'abord, le concret en français.
- [UX Passion, modèles d'implémentation et mentaux](https://uxpassion.com/blog/implementation-mental-representation-models-ux-user-experience) : l'écart entre ce que le code fait et ce que la personne se représente.
- Don Norman, *The Design of Everyday Things*, et Steve Krug, *Don't Make Me Think*, lus à travers des résumés, pas dans le texte ([résumé de Norman](https://uxdesign.cc/how-do-we-still-get-this-wrong-norman-doors-089363d4f1ef)).
