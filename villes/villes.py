# %%
from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px
import seaborn as sns

sns.set_palette("colorblind")
# %% LOADING DATA

# Charger le fichier CSV dans un DataFrame
df = pd.read_csv("Mesure_mensuelle_annee.csv")
df_copie = df.copy()
df = df.dropna()

# %% OCCURENCES DES VILLES

# Extraire la colonne des villes
villes = df["nom_com"]

# On regarde les occurences des villes pour faire un choix
occ_villes = villes.value_counts()

# Afficher la liste des villes uniques
# print(occ_villes)

# %% AIDE AU CHOIX DES VILLES ET STATIONS
"""
Permet de voir les différentes stations puis celles qui ont été supprimées pendant le dorpna()


villes_choisies = [
    "TOULOUSE",
    "MONTPELLIER",
    "TARBES",
    "MONTAUBAN",
    "PEYRUSSE-VIEILLE",
    "ARGELES-GAZOST",
]

# Boucle pour itérer sur chaque ville
for ville in villes_choisies:
    df_ville = df[df["nom_com"] == ville]
    occurrences_stations = df_ville["nom_station"].value_counts()
    print(f"Occurrences des stations pour la ville {ville} :")
    print(occurrences_stations)
    print("\n" + "=" * 30 + "\n")

df_filtre = df_copie[df_copie["nom_com"].isin(villes_choisies)]

# Supprimer les lignes avec des valeurs manquantes dans le DataFrame filtré
df_filtre = df_filtre.dropna()

# Les lignes supprimées se trouvent dans df_copie, qui contient toutes les lignes du fichier d'origine
lignes_supprimees = df_copie.loc[~df_copie.index.isin(df_filtre.index)]
lignes_supprimees.to_csv("lignes_supprimees.csv", index=False)

df2 = pd.read_csv("lignes_supprimees.csv")
villes_choisies = [
    "TOULOUSE",
    "MONTPELLIER",
    "TARBES",
    "MONTAUBAN",
    "PEYRUSSE-VIEILLE",
    "ARGELES-GAZOST",
]

# Boucle pour itérer sur chaque ville
for ville in villes_choisies:
    df2_ville = df2[df2["nom_com"] == ville]
    occurrences_stations = df2_ville["nom_station"].value_counts()
    print(f"Occurrences des stations pour la ville {ville} :")
    print(occurrences_stations)
    print("\n" + "=" * 30 + "\n")
"""

# %%
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Différences intra-villes"),

    
]

