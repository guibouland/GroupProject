# Pollution en Occitanie

Le site internet de ce projet est disponible à l'URL suivante: [https://guibouland.github.io/GroupProject](https://guibouland.github.io/GroupProject/).

## Description du projet

Le projet consiste à construire un site web en utilisant `Quarto` et `Github` dans le but d'étudier la pollution en Occitanie au cours des dernières années. Pour cela nous utilisons des jeux de données de pollution de [Atmo Occitanie](https://data-atmo-occitanie.opendata.arcgis.com/pages/liste-des-flux) et des données météorologiques de [SYNOP](https://public.opendatasoft.com/explore/dataset/donnees-synop-essentielles-omm/api/?sort=date).

## Prérequis et dépendances

Pour utiliser correctement notre projet, nous vous invitons à créer un environnement virtuel contenant les dépendances présentes dans le fichier `requirements.txt`. Il contient les librairies python que nous avons utilisées :  

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

* Visualisation géographique de la pollution au cours de cette année avec l'utilisation de `folium` et de cartes de températures. \
Utilisation de `geopandas` pour décrire les départements à partir d'un fichier `geojson` et de `pandas` pour manipuler les dataframes. Pour légender la carte, l'utilisation de `branca` fut nécessaire;

* Évolution départementale qui, sur plusieurs périodes, analyse la pollution à l'échelle départementale pour les 5 polluants suivants: NO, NOX, O3, PM10, PM2. Etudes des départements séparées, une analyse intra-départementale, et une autre inter-départementale. Analyse uniquement sur 10 des 13 départements en Occitanie par manque de données. Dans les graphiques restants, pour chaque valeur manquante, la valeur 0 est associée.
Téléchargement des 2 bases de données sur le dépôt github afin d'éviter d'utiliser une commande qui les appelle à chaque fois. La première correspond aux moyennes mensuelles des quantités de chaque polluant sur l'année actuelle et la seconde aux moyennes annuelles des quantités sur les 5 dernières années.
Chaque graphique regroupe l'évolution d'un polluant pour une base de données choisie. Le module `express` de `plotly` est utilisé pour générer les points, et le module `graph_objects` de `plotly` permet d'ajouter les traces qui relient les points, pour obtenir les graphiques;

* Comparatif entre villes de différentes populations au cours de cette année, en utilisant `pandas` pour manipuler ce dataframe. Avec le nombre de données disponibles dans certaines grandes villes telles que Montpellier et Toulouse, nous avons aussi réalisé un comparatif entre stations de prélèvements de ces villes, le tout présenté sous forme de graphe en utilisant le module `graph_objects` de `plotly`, permettant un minimum d'interactivité grâce à des groupes de légendes (par polluants) cliquables;

* Mise en évidence de l'influence de facteurs météorologiques sur la concentration de pollution via l'utilisation de `pandas` pour la manipulation des dataframes ainsi que de `graph_objects` et `express` de `plotly` pour un affichage interactif de graphes à coordonnées cartésiennes comme polaires. Un sous-module `meteo` de `modules` est créé spécifiquement pour la mise en page et l'ajout de courbes sur les graphes.

## Etude du temps et de la mémoire

* A l'aide du package `memory-profiler`, il est possible de surveiller la consommation en temps et en mémoire d'une fonction python. Cependant, il n'est pas possible de vérifier de tels critères sur des fichiers `Quarto`.   
Les tests des fichiers `carte.py` et `meteo.py` (avec la commande `mprof run`) donnent ainsi:  

|   carte    |   meteo    |
|:-:    |:-:    |
|  ![carte.py](image/../images/cartemem.png?raw=true "carte.py")     |   ![meteo.py](image/../images/meteomem.png?raw=true "meteo.py")    |

L'utilisation de la mémoire est de l'ordre de 50 mébioctects (environ 50 Mo) par fichier python ce qui reste convenable.  

* Avec la fonction `time()` il est possible de determiner le temps necessaire pour chaque cellules python d'un fichier quarto.  

|fichier quarto| Execution time|
|:-:    |:-:    |
|carte | 0.21710 s|
|départements |0.50733 s (par départements) * 13 = 6.59529 s|  
|villes |0.09505 s + 0.17805 s + 0.28116 s = 0.55426 s|  
|météo|0.31670 s + 0.14615 s + 0.13853 s = 0,60138 s| 

Pour l'efficacité temporelle, la partie départementale est la plus longue. Tandis que les autres s'effectuent en moins d'une seconde, cette partie du site prend longtemps à s'afficher.
Pour remedier à cela, des outils comme `dash` ou `Tkinter` ont été abordés mais abandonnés car incompatibles avec Github. Le choix d'importer directement les bases de données au lieu de les appeler avec `requests` est aussi un parti pris pour améliorer la vitesse d'execution.  
Une optique d'amélioration serait de plus dépendre de fonctions python dans les `.qmd`.


## Licence

Nous avons opté pour une licence [MIT](LICENSE), octroyant à tout le monde les droits sur notre projet, avec très peu de contraintes.

## Contributeurs

Ce projet a été réalisé par 4 élèves de l'Université de Montpellier:

* [DIAS Pierre](https://github.com/pierre-ed-ds)
* [FESTOR Quentin](https://github.com/Qufst)
* [LAMURE Maxence](https://github.com/MaxenceLamure)
* [BOULAND Guillaume](https://github.com/guibouland)
