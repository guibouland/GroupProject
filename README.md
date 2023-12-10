# Pollution en Occitanie

Le site internet de ce projet est disponible à l'URL suivante: [https://guibouland.github.io/GroupProject](https://guibouland.github.io/GroupProject/).

## Description du projet

Le projet consiste à construire un site web en utilisant `Quarto` et `Github` ayant pour but d'enquêter sur la pollution en Occitanie au cours des dernières années. Pour cela nous utilisons des jeux de données de pollution de [Atmo Occitanie](https://data-atmo-occitanie.opendata.arcgis.com/pages/liste-des-flux) et des données météorologiques de [SYNOP](https://public.opendatasoft.com/explore/dataset/donnees-synop-essentielles-omm/api/?sort=date). 

## Pré-requis et dépendances

Pour utiliser correctmeent notre projet, nous vous invitons à créer un environnement virtuel contenant les dépendances présentes dans le fichier `requirements.txt`. Il contient les librairies python que nous avons utilisées :  

* pandas
* geopandas
* folium
* branca
* numpy
* seaborn
* plotly

Cependant, pour une visualisation simple de notre site internet, aucun télechargement n'est nécessaire au bon fonctionnement de celui-ci.

## Méthodologie

Le site se divise en 4 parties:

* Visualisation géographique de la pollution au cours de cette année avec l'utilisation de `folium` et de cartes de chaleurs. \
Utilisation de `geopandas` pour décrire les départements à partir d'un fichier `geojson` et de `pandas` pour manipuler les dataframes. Pour légender la carte, l'utilisation de `branca` fut nécessaire.

* Évolution départementale qui, sur plusieurs périodes, analyse la pollution à l'échelle départementale pour les 5 polluants suivants: NO, NOX, O3, PM10, PM2. Etudes des départements séparées, une analyse intra-départementale, et une autre inter-départements. Analyse uniquement sur 10 des 13 départements en Occitanie par manque de données. Dans les graphiques restants, pour chaque valeur manquante la valeur 0 est associée. 
Téléchargement des 2 bases de données sur le dépôt github afin d'éviter d'utiliser une commande qui les appelle à chaque fois. La première correspond aux moyennes mensuelles des quantités de chaque polluant sur l'année actuelle. La seconde correspond aux moyennes annuelles des quantités sur les 5 dernières années.
Chaque graphique regroupe l'évolution d'un polluant pour une base de données choisis. Le module 'express' de 'plotly' utilisé pour générer les points, et le module 'graph_objects' de 'plotly' afin d'ajouter les traces qui relient les points, pour obtenir les graphiques.

* Comparatif entre villes de différentes populations au cours de cette année, en utilisant `pandas` pour manipuler ce dataframe. Avec le nombre de données disponibles dans certaines grandes villes telles que Montpellier et Toulouse, nous avons aussi réalisé un comparatif entre stations de prélèvements de ces villes, le tout présenté sous forme de graphe en utilisant le module `graph_objects` de `plotly`, permettant un minimum d'interactivité grâce à des groupes de légendes (par polluants) cliquables;

* Mise en évidence de l'influence de facteurs météorologiques sur la concentration de pollution via l'utilisation de `pandas` pour la manipulation des data frames ainsi que de `graph_objects` et `express` de `plotly` pour un affichage interactif de graphes à coordonnées cartésiennes comme polaires. Un sous-module `meteo` de `modules` est créé spécifiquement pour la mise en page et l'ajout de courbes sur les graphes.

## Licence

Nous avons opté pour une licence [MIT](LICENSE), octroyant à tout le monde les droits sur notre projet, avec très peu de contraintes.

## Contributeurs

Ce projet a été réalisé par 4 élèves à l'Université de Montpellier:

* [DIAS Pierre](https://github.com/pierre-ed-ds)
* [FESTOR Quentin](https://github.com/Qufst)
* [LAMURE Maxence](https://github.com/MaxenceLamure)
* [BOULAND Guillaume](https://github.com/guibouland)