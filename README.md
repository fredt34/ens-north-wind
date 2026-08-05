# ens-north-wind — Prévisions Vent à l'ENS

Site statique (GitHub Pages) qui affiche les prévisions de vent des 10 prochains jours pour un site de l'ENS, avec un focus particulier sur les **vents de secteur Nord**.

**Site en ligne** : https://fredt34.github.io/ens-north-wind/
**Source publiée** : `docs/index.html` (branche `main`)

## 1. Pourquoi ce projet existe

Le vent de secteur Nord a des **impacts négatifs sur des expériences en laboratoire**. Ce site sert d'outil de vigilance opérationnelle : il permet aux équipes des labos concernés d'anticiper les créneaux à risque et de **préparer, si besoin, la suspension d'expériences sensibles**.

Ce n'est donc pas un site "météo loisir" — la priorité produit est la **lisibilité du risque en un coup d'œil**, pas l'esthétique pure. Toute évolution de design doit d'abord servir cet objectif (voir §4).

## 2. Fonctionnement actuel (v1)

- Page HTML/CSS/JS unique (`docs/index.html`), sans framework ni build step.
- Données : [Open-Meteo](https://api.open-meteo.com/v1/forecast?latitude=48.862725&longitude=2.287592&hourly=wind_speed_80m,wind_direction_80m,temperature_80m&timezone=auto&forecast_days=10) — vitesse, direction et température du vent à 80 m, prévisions horaires sur 10 jours, coordonnées fixes dans l'URL (48.862725, 2.287592).
- Le fetch et le rendu se font **côté client**, au chargement de la page (pas de contenu visible dans le HTML statique avant exécution du JS).
- Affichage : une grille par jour, une case par heure, avec :
  - une flèche (glyphe `➨`) indiquant la direction vers laquelle souffle le vent,
  - une couleur de flèche selon la température,
  - un fond blanc sur les cases où le vent est de secteur Nord.

### Conventions importantes à connaître

- **Secteur Nord** = direction météo (d'où vient le vent) comprise entre **292.5° et 67.5°** (plage qui traverse 0°/360°).
- **Rotation de la flèche** : le glyphe `➨` pointe par défaut vers l'Est (0° = droite). La direction météo (`direction`) indique *d'où vient* le vent ; pour afficher *vers où il souffle*, on ajoute 180°, puis on retranche 90° pour compenser l'orientation par défaut du glyphe. D'où la formule utilisée dans le code : `rotation = (direction + 90) % 360`. Ne pas "corriger" cette formule sans revérifier ce raisonnement.
- **Couleur par température** : table de paliers `min/max` parcourue avec `.find()` (le premier match gagne).

### Bug connu à corriger

La table de couleurs de température a un **trou entre -3°C et 0°C** (les paliers `{-5,-3}` et `{0,2}` ne sont pas contigus) : une température arrondie à -2°C ou -1°C ne matche aucun palier et retombe sur le fallback `#000000` (flèche noire, quasi invisible sur fond sombre). Il y a aussi un palier mort (`{min:1, max:2}`, jamais atteint car couvert par `{min:0, max:2}` qui le précède). À corriger en rendant les paliers contigus et en supprimant le doublon.

## 3. Direction retenue pour la v2

Décisions actées avec l'utilisateur (à date de ce README) :

1. **Abandon du thème "funky/ludique"** initialement envisagé : le site doit rester un outil d'alerte, pas un produit grand public. Les couleurs et l'ambiance visuelle doivent communiquer un **niveau de risque**, pas une émotion positive.
2. **Mise en page façon "meteogramme" (style Yr.no)**, en remplacement de la grille de cases par jour actuelle :
   - **7 jours affichés, empilés en lignes** (au lieu de 10 en grille).
   - Pour chaque jour : une **courbe de vitesse du vent** (aire dégradée) sur 24h, avec en dessous une **ligne de flèches de direction**, alignées heure par heure.
   - Axe des heures commun, fixé en haut (`sticky`) pendant le scroll horizontal ; colonne des jours fixée à gauche (`sticky`).
   - Repère visuel sur l'heure/le jour courants.
3. **Taille de la flèche ∝ vitesse du vent** (échelle non linéaire acceptable, avec un min/max pour rester lisible).
4. **Fond = niveau de risque, pas la température.** 4 niveaux, calculés à partir de (secteur Nord ? vitesse) :
   - `0` neutre — pas de vent Nord
   - `1` vigilance — Nord, vitesse faible
   - `2` alerte — Nord, vitesse proche du seuil critique
   - `3` critique — Nord + vitesse au-dessus du seuil → suspension probable
   - Palette retenue (**option B, mono-teinte rouge par intensité**, choisie pour rester lisible en daltonisme, l'info étant portée par la luminosité plutôt que la teinte) :

     | Niveau | Couleur |
     |---|---|
     | Neutre | `#141d2e` |
     | Vigilance | `#5c2a2a` |
     | Alerte | `#8f2f2f` |
     | Critique | `#c92f2f` (+ liseré pulsé, respecte `prefers-reduced-motion`) |

   - Les seuils de vitesse exacts (km/h) séparant vigilance/alerte/critique **restent à définir avec les labos concernés** — dans les maquettes actuels ce sont des valeurs provisoires (15 et 30 km/h).
5. **La courbe de vitesse hérite aussi du code couleur du risque** (dégradé le long du tracé, calculé heure par heure), et le **fond de chaque ligne-jour** reçoit une légère teinte rouge basée sur le risque maximal atteint ce jour-là — pour repérer un jour à risque avant même de lire le détail des heures.
6. Un **bandeau d'alerte** en haut de page annonce le prochain créneau critique en langage clair (ex. "jeudi 14h–18h — préparer la suspension").

### Maquettes de référence

Des maquettes HTML autonomes (données fictives, aucune dépendance) ont été produites pour valider ces directions. Si elles ne sont pas déjà versionnées dans le repo, il est recommandé de les ajouter (ex. sous `design/` ou `docs/mockups/`) pour garder une trace :
- une première version en grille (case par jour × heure), abandonnée au profit du style meteogramme,
- la version meteogramme actuelle (courbes + flèches, dégradé de couleur par risque, fond de ligne teinté).

## 4. Pour une IA (ou un humain) qui reprend ce projet

Priorités, dans l'ordre :

1. **Ne jamais perdre de vue l'objectif métier** : signaler tôt et clairement les créneaux de vent Nord susceptibles d'imposer une suspension d'expérience. Toute feature qui n'améliore pas cet objectif est secondaire.
2. **Corriger le bug de couleur de température** (§2) avant ou pendant la refonte, même si la température devient une info secondaire en v2.
3. **Implémenter le layout meteogramme** (§3.2) en remplacement de la grille actuelle, en réutilisant :
   - la logique de fetch Open-Meteo existante,
   - la définition du secteur Nord (292.5°–67.5°),
   - la formule de rotation des flèches (`direction + 90`),
   - en ajoutant : calcul du niveau de risque par heure, dégradé de couleur sur la courbe, teinte de fond par jour, bandeau d'alerte dynamique (calculé à partir des données, pas codé en dur comme dans les maquettes).
4. **Ajouter un état de chargement** (actuellement écran vide pendant le fetch) et **un fallback** en cas d'échec réseau (ex. cache `localStorage` des dernières données valides).
5. **Rendre les infos au tap accessibles sur mobile** : le `title` HTML ne s'affiche pas au tap ; prévoir un affichage permanent ou déclenché au clic pour le détail heure par heure (vitesse, direction, éventuellement température).
6. **Ne pas réintroduire d'esthétique "ludique"** (animations façon comic, glow doré, médailles, etc.) : toute proposition visuelle doit être passée au filtre "est-ce que ça aide à repérer un risque plus vite, ou est-ce que ça décore ?".
7. Les seuils de vitesse définissant vigilance/alerte/critique sont **paramétrables et à valider** avec les utilisateurs finaux (labos) — ne pas les figer en dur sans les rendre facilement modifiables (constante en tête de fichier a minima).

## 5. Stack

- HTML/CSS/JS vanilla, aucun build step, aucune dépendance externe.
- Hébergement : GitHub Pages, servi depuis `docs/` sur `main`.
- Source de données : API publique Open-Meteo (pas de clé requise).