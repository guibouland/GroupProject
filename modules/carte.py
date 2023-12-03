import geopandas as gpd
import pandas as pd
import numpy as np


pd.options.mode.chained_assignment = None

# base de la carte avec les départements
sf = gpd.read_file("departements-version-simplifiee.geojson")
#on ne garde que les departement qui nous interessent
indexNames = sf[
    (sf["code"] != "09")
    & (sf["code"] != "11")
    & (sf["code"] != "12")
    & (sf["code"] != "30")
    & (sf["code"] != "31")
    & (sf["code"] != "32")
    & (sf["code"] != "34")
    & (sf["code"] != "46")
    & (sf["code"] != "48")
    & (sf["code"] != "65")
    & (sf["code"] != "66")
    & (sf["code"] != "81")
    & (sf["code"] != "82")
].index
sf.drop(indexNames, inplace=True)
import folium

#initialisation de la carte avec notre geojson des departements
centre = [43.716671, 2.15]
Occitanie = folium.Map(location=centre, zoom_start=6.5,tiles=None)
folium.GeoJson(
    sf[["nom", "geometry"]],
    name="Départements",
    zoom_on_click=True,
    style_function=lambda feature: {
        "fillColor": "#003322",
        "color": "grey",
        "weight": 2,
        "dashArray": "5, 5",
        "fillOpacity": 0.01,
    },
    tooltip=folium.features.GeoJsonTooltip(
        fields=["nom"],
        aliases=["Département:"],
    ),
).add_to(Occitanie)


# ajout layer pollution
from folium.plugins import HeatMap
from folium.plugins import HeatMapWithTime
from folium.plugins import GroupedLayerControl
import branca.colormap as cm

#légende

color_mapa=cm.LinearColormap(colors=['darkblue','purple','yellow'],
                             caption='intensité de concentration du polluant')

#cadre de la légende
svg_style = '<style>svg#legend {background-color: rgba(255,255,255,0.5);}</style>'

#ajout de la legende à la carte
Occitanie.get_root().header.add_child(folium.Element(svg_style))
color_mapa.add_to(Occitanie)


#manipulation des données
polluant = pd.read_csv(
    "bases_de_donnees/Mesure_mensuelle_annee.csv",
    sep=",",
    na_values="",
    low_memory=False,
)
polluants = polluant.dropna()

#moyenne des polluants sur l'année
polluants = (
    polluants.groupby(["X", "Y", "nom_poll","nom_dept"])["valeur"]
    .mean()
    .reset_index(name="valeur")
)

#gradient de couleurs adapté aux daltoniens, jaune chaud, bleu froid.
grad={
        0: "#0d0887",
        0.1: "#0d0887",
        0.2: "#0d0887",
        0.3: "#0d0887",
        0.4: "#0d0887",
        0.5: "#6a00a8",
        0.6: "#b12a90",
        0.7: "#e16462",
        0.8: "#fca636",
        0.9: "#fcce25",
        1: "#f0f921",
    }

# PM10
PM10 = polluants[(polluants["nom_poll"] == "PM10")]
heatPM10 = PM10[["Y", "X", "valeur"]].copy()
lng = heatPM10["X"].tolist()
lat = heatPM10["Y"].tolist()
val = heatPM10["valeur"].tolist()
pm10 = HeatMap(
    list(zip(lat, lng, val)),
    name="PM10",
    gradient=grad,
    radius=40,
    blur=35,
)
fpm10 = folium.FeatureGroup(name="PM10", show=True)
pm10.add_to(fpm10)

# PM2
PM2 = polluants[(polluants["nom_poll"] == "PM2.5")]
heatPM2 = PM2[["Y", "X", "valeur"]].copy()
lng = heatPM2["X"].tolist()
lat = heatPM2["Y"].tolist()
val = heatPM2["valeur"].tolist()
pm2 = HeatMap(
    list(zip(lat, lng, val)),
    name="PM2.5",
    gradient=grad,
    radius=40,
    blur=35,
)
fpm2 = folium.FeatureGroup(name="PM2", show=False)
pm2.add_to(fpm2)

# NO
NO = polluants[(polluants["nom_poll"] == "NO")]
heatNO = NO[["Y", "X", "valeur"]].copy()
lng = heatNO["X"].tolist()
lat = heatNO["Y"].tolist()
val = heatNO["valeur"].tolist()
no = HeatMap(
    list(zip(lat, lng, val)),
    name="NO",
    gradient=grad,
    radius=40,
    blur=35,
)
fno = folium.FeatureGroup(name="NO", show=False)
no.add_to(fno)

# NO2
NO2 = polluants[(polluants["nom_poll"] == "NO2")]
heatNO2 = NO2[["Y", "X", "valeur"]].copy()
lng = heatNO2["X"].tolist()
lat = heatNO2["Y"].tolist()
val = heatNO2["valeur"].tolist()
no2 = HeatMap(
    list(zip(lat, lng, val)),
    name="NO2",
    gradient=grad,
    radius=40,
    blur=35,
)
fno2 = folium.FeatureGroup(name="NO2", show=False)
no2.add_to(fno2)

# O3
O3 = polluants[(polluants["nom_poll"] == "O3")]

heatO3 = O3[["Y", "X", "valeur"]].copy()
lng = heatO3["X"].tolist()
lat = heatO3["Y"].tolist()
val = heatO3["valeur"].tolist()
o3 = HeatMap(
    list(zip(lat, lng, val)),
    name="O3",
    gradient=grad,
    radius=40,
    blur=35,
)
fo3 = folium.FeatureGroup(name="O3", show=False)
o3.add_to(fo3)

#ajout des Heatmap a la carte (en faisant en sorte qu'elles 
#ne puissent pas se declencher simultanement)
Occitanie.add_child(fpm10)
Occitanie.add_child(fpm2)
Occitanie.add_child(fno)
Occitanie.add_child(fno2)
Occitanie.add_child(fo3)

class Markero(object):
    """Classe pour faire les points folium facilement"""

    def __init__(self, lat, long, texte, popup):
        """créé un point"""
        self.lat = lat
        self.long = long
        self.texte = texte
        self.popup = popup

    def SurCarte(self,carte):
        """Met le point sur la carte"""
        folium.Marker(
        [self.lat, self.long],tooltip=self.texte, popup=self.popup, icon=folium.Icon(icon='glyphicon-th-list',color="darkpurple")
        ).add_to(carte)

#utilisation de la classe Markero pour faire nos points
Toul=Markero(43.6, 1.43333,"Toulouse","""
<p>Toulouse:<br>
500 000 habitants </p>
  """) 


Mtp=Markero(43.62505, 3.862038,"Montpellier","""
<p>Montpellier:<br>
300 000 habitants</p>
  """)

Tarbes=Markero(43.23333, 0.08333,"Tarbes","""
<p>Tarbes:<br>
Plus de 40 000 habitants</p>
  """)

Montauban=Markero(44.01667, 1.35,"Montauban","""
<p>Montauban:<br>
Plus de 60 000 habitants</p>
  """)

Pey=Markero(43.6333, 0.1833,"Peyrusse-Vieille","""
<p>Peyrusse-Vieille:<br>
65 habitants </p>
  """)

Arg=Markero(43.005028, -0.101087,"Argeles-Gazost","""
<p>Argeles-Gazost:<br>
Moins de 3000 habitants</p>
  """)

Perpi=Markero(42.683331,2.88333,"Perpignan","""
<p>Perpignan:<br>
120 000 habitants </p>
""")

#fonction SurCarte de la classe Markero
Toul.SurCarte(Occitanie)
Mtp.SurCarte(Occitanie)
Tarbes.SurCarte(Occitanie)
Montauban.SurCarte(Occitanie)
Pey.SurCarte(Occitanie)
Arg.SurCarte(Occitanie)
Perpi.SurCarte(Occitanie)

#ajout de styles de carte differents
folium.TileLayer("OpenStreetMap", name="Street Map").add_to(Occitanie)
folium.TileLayer("Cartodb dark_matter", name="Sombre").add_to(Occitanie)
folium.TileLayer("CartoDB Positron", name="Clair").add_to(Occitanie)

folium.LayerControl(position= 'topleft',collapsed=True,opacity=0.7).add_to(Occitanie)

GroupedLayerControl(position='bottomleft',
    groups={"Polluants": [fpm10, fpm2, fno, fno2, fo3]},
    collapsed=False
).add_to(Occitanie)

#affichage de la carte
import webbrowser
Occitanie.save("HMOccitanie.html")
webbrowser.open("HMOccitanie.html")
#pour le rendu dans le .py j'ouvre un navigateur afin de voir le rendu 