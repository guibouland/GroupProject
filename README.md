# Projet Groupe Pollution en Occitanie groupe 4
## Environnement
Pour ce projet, nous allons avoir besoin d'un environnement contenant:
- Python
- Pandas
- Plotly
- Pytest
- Pooch
- dash

## Objectif
L'objectif est de créer un site contenant une carte interactive permettant de voir la pollution en occitannie à une période donnée. Cette carte devra être lisible et facilement interprétable.\
Les données sont extraites du site [Atmo Occitanie](https://data-atmo-occitanie.opendata.arcgis.com/pages/liste-des-flux) et concerneront la pollution de l'air, notamment les particules en suspension, les particules fines et le dioxyde d'azote.\

## Utilisation des environnements et choix des bases de données
L'objectif est de représenter l'évolution de différents types de polluants en Occitanie durant 3 périodes différents.

Par exemple, on s'intéresse à l'évolution durant les 5 dernières années. Pour cela on utilise une base de donnée comportant uniquement la valeur moyenne de l'année de chaque polluant pour un bon nombres de villes, réparties équitablement dans chaque départements en Occitanie. 

Pour modéliser ça on va utiliser pour commencer la bibliothèque Pandas afin d'ouvrir la base de donnée qui est un fichier csv avec la commande panda.read_csv("chemin/de/la/base/de/donnée.csv").
Ensuite on utilise l'environnement plotly afin de créer de beau graphiques. On choisit de modéliser l'évolution moyenne par an des différents types de polluants au cours des 5 dernières années par département dans certaines villes. 
Enfin afin de rendre le site intéractif on utilise l'environnement dash qui va nous permettre de créer un fichier html regroupant nos graphiques et de sélectionner le département que l'on veut afficher.

## Site Web
Le site internet de ce projet est disponible à l'URL suivante: [https://guibouland.github.io/GroupProject](https://guibouland.github.io/GroupProject/)

