# ens-north-wind — Prévisions Vent à l'ENS

Tableau de vigilance pour les vents de secteur Nord à l'École normale supérieure. Le site aide les équipes concernées à repérer les créneaux pouvant nécessiter la préparation ou la suspension d'expériences sensibles.

**Site en ligne :** <https://fredt34.github.io/ens-north-wind/>  
**Page publiée :** `docs/index.html`

## Fonctionnement

La page est une application HTML/CSS/JavaScript autonome, sans framework ni étape de compilation. Au chargement, elle interroge l'API publique [Open-Meteo](https://open-meteo.com/) pour afficher les prévisions horaires de vent à 80 m sur 10 jours pour le site configuré.

Chaque ligne correspond à une journée et présente :

- une courbe de vitesse du vent ;
- une flèche par heure indiquant la direction **vers laquelle** souffle le vent ;
- le niveau de risque par fond coloré ;
- une infobulle au survol de la courbe ou d'une flèche, avec heure, vitesse, direction et niveau de risque ;
- un repère sur l'heure courante et la journée courante ;
- un bandeau indiquant le premier créneau Critique à venir ou, en l'absence de Critique, le premier créneau Alerte.

Le bandeau affiche uniquement le premier créneau correspondant. D'autres créneaux critiques restent visibles dans les lignes horaires mais ne sont pas énumérés dans cet avertissement.

Les jours à vitesse modérée utilisent une échelle de courbe plafonnée à 45 km/h. Pour les jours plus venteux, l'échelle s'étend automatiquement avec une marge, par paliers de 10 km/h.

## Niveaux de risque

Le secteur Nord comprend les directions météo de **292,5° à 67,5°**, en traversant le Nord (0°/360°).

| Niveau | Condition dans le secteur Nord | Signal visuel |
| --- | --- | --- |
| Neutre | Hors secteur Nord ou vitesse < 25 km/h | Petite flèche, fond sombre |
| Vigilance | 25 à < 40 km/h | Flèche moyenne, fond ambre |
| Alerte | 40 à < 60 km/h pendant moins de 4 h consécutives | Grande flèche, fond rouge |
| Critique | **High Wind** : ≥ 60 km/h, même pendant une seule heure ; ou 40 à < 60 km/h pendant au moins 4 h consécutives | Flèche `↠`, fond rouge et liseré pulsé |

Les niveaux **Alerte** et **Critique** partagent volontairement la même couleur rouge ; leur glyphe et l'emphase du niveau critique permettent de les distinguer.

## Configuration

Toute la configuration métier et de démonstration est regroupée dans `CONFIG`, au début de `docs/index.html` :

- URL Open-Meteo et coordonnées du site ;
- limites angulaires du "secteur Nord" ;
- seuils de vitesse, seuil High Wind et durée critique ;
- styles de flèche par niveau ;
- échelle de base de la courbe (`chartMaxSpeedKmh`) ;
- vitesses et directions de la ligne d'exemple.

Les risques de la ligne d'exemple sont calculés à partir de ses vitesses et directions avec la même logique que les données réelles ; ils ne sont pas maintenus séparément.

### Simulation du bandeau d'alerte

Pour utiliser la ligne `Exemple` comme source du bandeau d'alerte pendant un test, exécuter dans la console du navigateur :

```js
setAlertSimulation(true)
```

La page se recharge et affiche le créneau issu de la ligne d'exemple. Pour revenir aux prévisions réelles :

```js
setAlertSimulation(false)
```

## Développement et publication

Aucune installation n'est nécessaire. Ouvrir `docs/index.html` dans un navigateur suffit pour travailler localement ; une connexion Internet est nécessaire pour récupérer les données Open-Meteo.

GitHub Pages publie le contenu de `docs/` depuis la branche `main`.

## Stack

- HTML, CSS et JavaScript vanilla ;
- API Open-Meteo, sans clé ;
- GitHub Pages pour l'hébergement.