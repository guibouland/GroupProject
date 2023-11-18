# %%
from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px
import seaborn as sns

# On applique une palette de couleur "colorblind"
sns.set_palette("colorblind")
# %% LOADING DATA

# On charge le csv dasn un dataframe pandas
df = pd.read_csv("../bases_de_donnees/Mesure_mensuelle_annee.csv")

# On supprime les lignes qui ne comprtent aucunes valeurs
df = df.dropna()

# On convertie la colonne "date_debut" en format datetime
df["date_debut"] = pd.to_datetime(df["date_debut"], format="%Y/%m/%d %H:%M:%S+%f")

# On crée une nouvelle colonne "mois-annee" au format datetime
df["mois_annee"] = df["date_debut"].dt.strftime("%Y/%m")

# %% OCCURENCES DES VILLES

# Extraction de la colonne des villes
villes = df["nom_com"]

# On regarde les occurences des villes pour faire un choix
occ_villes = villes.value_counts()

# Affichage de la liste des villes uniques
print(occ_villes)

# %% AIDE AU CHOIX DES VILLES ET STATIONS
"""
Permet de voir les différentes stations puis celles qui ont été supprimées pendant le dorpna()

df_copie = df.copy()
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

app.layout = html.Div(
    [
        html.H1("Différences intra-villes"),
        # Sélection de la ville
        dcc.Dropdown(
            id="ville",
            options=[
                {"label": "Toulouse", "value": "TOULOUSE"},
                {"label": "Montpellier", "value": "MONTPELLIER"},
            ],
            value="TOULOUSE",
        ),
        # Sélection du polluant
        dcc.Dropdown(
            id="polluant",
            options=[
                {"label": "NO", "value": "NO"},
                {"label": "NO2", "value": "NO2"},
                {"label": "NOX", "value": "NOX"},
                {"label": "O3", "value": "O3"},
                {"label": "PM10", "value": "PM10"},
                {"label": "PM2.5", "value": "PM2.5"},
            ],
            value="NO",
        ),
        # Graphique
        dcc.Graph(id="graph"),
    ]
)


# Update graphe en fonction de la sélection
@app.callback(
    Output("graph", "figure"), Input("ville", "value"), Input("polluant", "value")
)
def update(select_ville, select_poll):
    data = df[(df["nom_com"] == select_ville) & (df["nom_poll"] == select_poll)]
    data = data.sort_values(by="mois_annee")

    # Plot
    fig = px.line(
        data,
        x="mois_annee",
        y="valeur",
        color="nom_station",
        markers=True,
        labels={"nom_station": "Station", "mois_annee": "Date", "valeur": "Valeur"},
    )

    fig.update_layout(
        title=f"Différences de mesure pour {select_poll} à {select_ville}",
        xaxis_title="Date",
        yaxis_title=f"Valeur de {select_poll} (µg/m³)",
    )

    # Ajuster axe ordonnées
    fig.update_yaxes(range=[0, data["valeur"].max() + 5])

    return fig


if __name__ == "__main__":
    app.run(debug=True)
