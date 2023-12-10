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

* Évolution départementale qui, sur plusieurs périodes, analyse la pollution à l'échelle départementale;
* Comparatif entre villes de différentes populations au cours de cette année, en utilisant `pandas` pour manipuler ce dataframe. Avec le nombre de données disponibles dans certaines grandes villes telles que Montpellier et Toulouse, nous avons aussi réalisé un comparatif entre stations de prélèvements de ces villes, le tout présenté sous forme de graphe en utilisant le module `graph_objects` de `plotly`, permettant un minimum d'interactivité grâce à des groupes de légendes (par polluants) cliquables;
* Lien météorologique.

## Licence

Nous avons opté pour une licence [MIT](LICENSE), octroyant à tout le monde les droits sur notre projet, avec très peu de contraintes.

## Contributeurs

Ce projet a été réalisé par 4 élèves à l'Université de Montpellier:

* [DIAS Pierre](https://github.com/pierre-ed-ds)
* [FESTOR Quentin](https://github.com/Qufst)
* [LAMURE Maxence](https://github.com/MaxenceLamure)
* [BOULAND Guillaume](https://github.com/guibouland)