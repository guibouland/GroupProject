
---
title: "Pollution en Occitanie"
author: "BOULAND Guillaume, DIAS Pierre, FESTOR Quentin, LAMURE Maxence"

---

# Site Web

Le site internet de ce projet est disponible à l'URL suivante: [https://guibouland.github.io/GroupProject](https://guibouland.github.io/GroupProject/).

## Description du projet

Le projet consiste à construire un site web en utilisant `Quarto` et `Github` ayant pour but d'enquêter sur la pollution en Occitanie au cours des dernières années. Pour cela nous utilisons des jeux de données de pollution de [Atmo Occitanie](https://data-atmo-occitanie.opendata.arcgis.com/pages/liste-des-flux) et des données météorologiques de [SYNOP](https://public.opendatasoft.com/explore/dataset/donnees-synop-essentielles-omm/api/?sort=date). 

## Méthodologie

Le site se divise en 4 parties:

* Visualisation géographique de la pollution au cours de cette année avec l'utilisation de `folium` et de cartes de chaleurs. \
Utilisation de `geopandas` pour décrire les départements à partir d'un fichier `geojson` et de `pandas` pour manipuler les dataframes. Pour légender la carte, l'utilisation de `branca` fut nécessaire.

* Evolution départementale qui, sur plusieurs périodes, analyse la pollution à l'échelle departementale;
* Comparatif entre villes;
* Lien météorologique.

## Licence

MIT

