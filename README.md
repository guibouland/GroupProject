# Projet Groupe Pollution en Occitanie groupe 4

## Environnement

Pour ce projet, nous allons avoir besoin d'un environnement contenant:

- Python
- Pandas
- Plotly
- Pytest
- Pooch
- Dash

## Objectif

L'objectif est de créer un site contenant une carte interactive permettant de voir la pollution en Occitannie à une période donnée. Cette carte devra être lisible et facilement interprétable.\
Les données sont extraites du site [Atmo Occitanie](https://data-atmo-occitanie.opendata.arcgis.com/pages/liste-des-flux) et concerneront la pollution de l'air, notamment les particules en suspension, les particules fines et le dioxyde d'azote.

## Utilisation des environnements et choix des bases de données

L'objectif est de représenter l'évolution de différents types de polluants en Occitanie durant 3 périodes différentes.

Par exemple, on s'intéresse à l'évolution des polluants durant les 5 dernières années. Pour cela on utilise une base de données comportant uniquement la valeur moyenne de l'année de chaque polluant pour plusieurs de villes, réparties équitablement dans chaque département en Occitanie.

Pour modéliser cela, on va utiliser pour commencer la bibliothèque Pandas afin d'ouvrir la base de données qui est un fichier csv avec la commande panda.read_csv("chemin/de/la/base/de/donnée.csv").
Ensuite on utilise l'environnement plotly afin de créer de beaux graphiques. On choisit de modéliser l'évolution moyenne annuelle des différents types de polluants au cours des 5 dernières années par département dans plusieurs villes.
Enfin, afin de rendre le site interactif on utilise l'environnement dash qui va nous permettre de créer un fichier html regroupant nos graphiques et de sélectionner le département que l'on veut afficher.

## Site Web

Le site internet de ce projet est disponible à l'URL suivante: [https://guibouland.github.io/GroupProject](https://guibouland.github.io/GroupProject/).

## Auteurs

Ce projet a été réalisé par Guillaume Bouland, Pierre Dias, Maxence Lamure et Quentin Festor.
