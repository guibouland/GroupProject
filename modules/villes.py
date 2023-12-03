# %%
from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px
import seaborn as sns

# On applique une palette de couleur "colorblind"
sns.set_palette("colorblind")
# %% LOADING DATA

# On charge le csv dans un dataframe pandas
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

# %%
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns

# Changement d ela palette de couleur pour l'accessibilité
sns.set_palette("colorblind")

# Chargement des données
df = pd.read_csv("../bases_de_donnees/Mesure_mensuelle_annee.csv")

# On supprime les lignes qui ne comprtent aucunes valeurs
df = df.dropna()

# On convertie la colonne "date_debut" en format datetime
df["date_debut"] = pd.to_datetime(df["date_debut"], format="%Y/%m/%d %H:%M:%S+%f")

# On crée une nouvelle colonne "mois-annee" au format datetime
df["mois_annee"] = df["date_debut"].dt.strftime("%Y/%m")
df["mois_annee"] = pd.to_datetime(df["mois_annee"], format="%Y/%m")

# On restraint le dataframe à Montpellier et Toulouse et on le range par ordre croissant de dates
mtp = df[df.nom_com == "MONTPELLIER"]
tou = df[df.nom_com == "TOULOUSE"]

# MONTPELLIER

# On sélectionne les polluants de MONTPELLIER
mtpno = mtp[mtp.nom_poll == "NO"].sort_values(by="date_debut")
mtpno2 = mtp[mtp.nom_poll == "NO2"].sort_values(by="date_debut")
mtpnox = mtp[mtp.nom_poll == "NOX"].sort_values(by="date_debut")
mtppm10 = mtp[mtp.nom_poll == "PM10"].sort_values(by="date_debut")
mtppm2_5 = mtp[mtp.nom_poll == "PM2.5"].sort_values(by="date_debut")
# On ne prend pas O3 par manque de données
mtpo3 = mtp[mtp.nom_poll == "O3"].sort_values(by="date_debut")

# mtp.nom_station.unique()
figmtp = go.Figure()

# NO
figmtp.add_trace(
    go.Scatter(
        x=list(
            mtpno[
                mtpno.nom_station == "Montpellier - Prés d Arènes Urbain"
            ].mois_annee.unique()
        ),
        y=list(mtpno[mtpno.nom_station == "Montpellier - Prés d Arènes Urbain"].valeur),
        legendgroup="groupe 1",
        legendgrouptitle_text="<b>NO</b>",
        name="Prés d'Arènes Urbain",
        mode="lines+markers",
    )
)
figmtp.add_trace(
    go.Scatter(
        x=list(
            mtpno[
                mtpno.nom_station == "Montpellier - Chaptal Urbain"
            ].mois_annee.unique()
        ),
        y=list(mtpno[mtpno.nom_station == "Montpellier - Chaptal Urbain"].valeur),
        legendgroup="groupe 1",
        name="Chaptal Urbain",
        mode="lines+markers",
    )
)
figmtp.add_trace(
    go.Scatter(
        x=list(
            mtpno[mtpno.nom_station == "Montpellier Liberte Trafic"].mois_annee.unique()
        ),
        y=list(mtpno[mtpno.nom_station == "Montpellier Liberte Trafic"].valeur),
        legendgroup="groupe 1",
        name="Liberte Trafic",
        mode="lines+markers",
    )
)

# NO2
figmtp.add_trace(
    go.Scatter(
        x=list(
            mtpno2[
                mtpno2.nom_station == "Montpellier - Prés d Arènes Urbain"
            ].mois_annee.unique()
        ),
        y=list(
            mtpno2[mtpno2.nom_station == "Montpellier - Prés d Arènes Urbain"].valeur
        ),
        legendgroup="groupe 2",
        legendgrouptitle_text="<b>NO2</b>",
        name="Prés d'Arènes Urbain",
        mode="lines+markers",
    )
)
figmtp.add_trace(
    go.Scatter(
        x=list(
            mtpno2[
                mtpno2.nom_station == "Montpellier - Chaptal Urbain"
            ].mois_annee.unique()
        ),
        y=list(mtpno2[mtpno2.nom_station == "Montpellier - Chaptal Urbain"].valeur),
        legendgroup="groupe 2",
        name="Chaptal Urbain",
        mode="lines+markers",
    )
)
figmtp.add_trace(
    go.Scatter(
        x=list(
            mtpno2[
                mtpno2.nom_station == "Montpellier Liberte Trafic"
            ].mois_annee.unique()
        ),
        y=list(mtpno2[mtpno2.nom_station == "Montpellier Liberte Trafic"].valeur),
        legendgroup="groupe 2",
        name="Liberte Trafic",
        mode="lines+markers",
    )
)
figmtp.add_trace(
    go.Scatter(
        x=list(
            mtpno2[
                mtpno2.nom_station == "Montpellier - Saint Denis Trafic"
            ].mois_annee.unique()
        ),
        y=list(mtpno2[mtpno2.nom_station == "Montpellier - Saint Denis Trafic"].valeur),
        legendgroup="groupe 2",
        name="Saint Denis Trafic",
        mode="lines+markers",
    )
)


# NOX
figmtp.add_trace(
    go.Scatter(
        x=list(
            mtpnox[
                mtpnox.nom_station == "Montpellier - Prés d Arènes Urbain"
            ].mois_annee.unique()
        ),
        y=list(
            mtpnox[mtpnox.nom_station == "Montpellier - Prés d Arènes Urbain"].valeur
        ),
        legendgroup="groupe 3",
        legendgrouptitle_text="<b>NOX</b>",
        name="Prés d'Arènes Urbain",
        mode="lines+markers",
    )
)
figmtp.add_trace(
    go.Scatter(
        x=list(
            mtpnox[
                mtpnox.nom_station == "Montpellier - Chaptal Urbain"
            ].mois_annee.unique()
        ),
        y=list(mtpnox[mtpnox.nom_station == "Montpellier - Chaptal Urbain"].valeur),
        legendgroup="groupe 3",
        name="Chaptal Urbain",
        mode="lines+markers",
    )
)
figmtp.add_trace(
    go.Scatter(
        x=list(
            mtpnox[
                mtpnox.nom_station == "Montpellier Liberte Trafic"
            ].mois_annee.unique()
        ),
        y=list(mtpnox[mtpnox.nom_station == "Montpellier Liberte Trafic"].valeur),
        legendgroup="groupe 3",
        name="Liberte Trafic",
        mode="lines+markers",
    )
)


# PM10
figmtp.add_trace(
    go.Scatter(
        x=list(
            mtppm10[
                mtppm10.nom_station == "Montpellier - Prés d Arènes Urbain"
            ].mois_annee.unique()
        ),
        y=list(
            mtppm10[mtppm10.nom_station == "Montpellier - Prés d Arènes Urbain"].valeur
        ),
        legendgroup="groupe 4",
        legendgrouptitle_text="<b>PM10</b>",
        name="Prés d'Arènes Urbain",
        mode="lines+markers",
    )
)
figmtp.add_trace(
    go.Scatter(
        x=list(
            mtppm10[
                mtppm10.nom_station == "Montpellier - Pompignane Trafic"
            ].mois_annee.unique()
        ),
        y=list(
            mtppm10[mtppm10.nom_station == "Montpellier - Pompignane Trafic"].valeur
        ),
        legendgroup="groupe 4",
        name="Pompignane Trafic",
        mode="lines+markers",
    )
)
figmtp.add_trace(
    go.Scatter(
        x=list(
            mtppm10[
                mtppm10.nom_station == "Montpellier Liberte Trafic"
            ].mois_annee.unique()
        ),
        y=list(mtppm10[mtppm10.nom_station == "Montpellier Liberte Trafic"].valeur),
        legendgroup="groupe 4",
        name="Liberte Trafic",
        mode="lines+markers",
    )
)

# PM2.5
figmtp.add_trace(
    go.Scatter(
        x=list(
            mtppm2_5[
                mtppm2_5.nom_station == "Montpellier - Prés d Arènes Urbain"
            ].mois_annee.unique()
        ),
        y=list(
            mtppm2_5[
                mtppm2_5.nom_station == "Montpellier - Prés d Arènes Urbain"
            ].valeur
        ),
        legendgroup="groupe 5",
        legendgrouptitle_text="<b>PM2.5</b>",
        name="Prés d'Arènes Urbain",
        mode="lines+markers",
    )
)
figmtp.add_trace(
    go.Scatter(
        x=list(
            mtppm2_5[
                mtppm2_5.nom_station == "Montpellier - Pompignane Trafic"
            ].mois_annee.unique()
        ),
        y=list(
            mtppm2_5[mtppm2_5.nom_station == "Montpellier - Pompignane Trafic"].valeur
        ),
        legendgroup="groupe 5",
        name="Pompignane Trafic",
        mode="lines+markers",
    )
)
figmtp.add_trace(
    go.Scatter(
        x=list(
            mtppm2_5[
                mtppm2_5.nom_station == "Montpellier Liberte Trafic"
            ].mois_annee.unique()
        ),
        y=list(mtppm2_5[mtppm2_5.nom_station == "Montpellier Liberte Trafic"].valeur),
        legendgroup="groupe 5",
        name="Liberte Trafic",
        mode="lines+markers",
    )
)


figmtp.update_layout(
    title={
        "text": "<b>Différences dans Montpellier</b>",
        "x": 0.5,
        "xanchor": "center",
    },
    xaxis_title="<b>Mois</b>",
    yaxis_title="<b>Concentration (µg.m⁻³)</b>",
    legend=dict(title="<b>Polluants (et stations)</b>"),
    paper_bgcolor="rgba(100,100,100,0)",  # Couleur de contour de graphique
    plot_bgcolor="rgba(100,100,100,0)",  # Couleur du fond du graphique
    font=dict(color="Grey", size=10),
)
figmtp.show()


# TOULOUSE

# On sélectionne les polluants de TOULOUSE
touno = tou[tou.nom_poll == "NO"].sort_values(by="date_debut")
touno2 = tou[tou.nom_poll == "NO2"].sort_values(by="date_debut")
tounox = tou[tou.nom_poll == "NOX"].sort_values(by="date_debut")
touo3 = tou[tou.nom_poll == "O3"].sort_values(by="date_debut")
toupm10 = tou[tou.nom_poll == "PM10"].sort_values(by="date_debut")
toupm2_5 = tou[tou.nom_poll == "PM2.5"].sort_values(by="date_debut")

# tou.nom_station.unique() pour avoir les noms des stations de TOULOUSE
figtou = go.Figure()

# NO
figtou.add_trace(
    go.Scatter(
        x=list(
            touno[touno.nom_station == "Toulouse - Rte Albi Trafic"].mois_annee.unique()
        ),
        y=list(touno[touno.nom_station == "Toulouse - Rte Albi Trafic"].valeur),
        legendgroup="groupe 1",
        legendgrouptitle_text="<b>NO</b>",
        name="Rte Albi Trafic",
        mode="lines+markers",
    )
)
figtou.add_trace(
    go.Scatter(
        x=list(
            touno[touno.nom_station == "Toulouse-Berthelot Urbain"].mois_annee.unique()
        ),
        y=list(touno[touno.nom_station == "Toulouse-Berthelot Urbain"].valeur),
        legendgroup="groupe 1",
        name="Berthelot Urbain",
        mode="lines+markers",
    )
)
figtou.add_trace(
    go.Scatter(
        x=list(
            touno[touno.nom_station == "Toulouse-Jacquier Urbain"].mois_annee.unique()
        ),
        y=list(touno[touno.nom_station == "Toulouse-Jacquier Urbain"].valeur),
        legendgroup="groupe 1",
        name="Jacquier Urbain",
        mode="lines+markers",
    )
)
figtou.add_trace(
    go.Scatter(
        x=list(
            touno[
                touno.nom_station == "Toulouse-Périphérique Trafic"
            ].mois_annee.unique()
        ),
        y=list(touno[touno.nom_station == "Toulouse-Périphérique Trafic"].valeur),
        legendgroup="groupe 1",
        name="Périphérique Trafic",
        mode="lines+markers",
    )
)
figtou.add_trace(
    go.Scatter(
        x=list(
            touno[
                touno.nom_station == "Toulouse - Port de l Embouchure Trafic"
            ].mois_annee.unique()
        ),
        y=list(
            touno[touno.nom_station == "Toulouse - Port de l Embouchure Trafic"].valeur
        ),
        legendgroup="groupe 1",
        name="Port de l'Embouchure Trafic",
        mode="lines+markers",
    )
)
figtou.add_trace(
    go.Scatter(
        x=list(
            touno[
                touno.nom_station == "Toulouse-SETMI Eisenhower Industriel"
            ].mois_annee.unique()
        ),
        y=list(
            touno[touno.nom_station == "Toulouse-SETMI Eisenhower Industriel"].valeur
        ),
        legendgroup="groupe 1",
        name="SETMI Eisenhower Industriel",
        mode="lines+markers",
    )
)


# NO2
figtou.add_trace(
    go.Scatter(
        x=list(
            touno2[
                touno2.nom_station == "Toulouse - Rte Albi Trafic"
            ].mois_annee.unique()
        ),
        y=list(touno2[touno2.nom_station == "Toulouse - Rte Albi Trafic"].valeur),
        legendgroup="groupe 2",
        legendgrouptitle_text="<b>NO2</b>",
        name="Rte Albi Trafic",
        mode="lines+markers",
    )
)
figtou.add_trace(
    go.Scatter(
        x=list(
            touno2[
                touno2.nom_station == "Toulouse-Berthelot Urbain"
            ].mois_annee.unique()
        ),
        y=list(touno2[touno2.nom_station == "Toulouse-Berthelot Urbain"].valeur),
        legendgroup="groupe 2",
        name="Berthelot Urbain",
        mode="lines+markers",
    )
)
figtou.add_trace(
    go.Scatter(
        x=list(
            touno2[touno2.nom_station == "Toulouse-Jacquier Urbain"].mois_annee.unique()
        ),
        y=list(touno2[touno2.nom_station == "Toulouse-Jacquier Urbain"].valeur),
        legendgroup="groupe 2",
        name="Jacquier Urbain",
        mode="lines+markers",
    )
)
figtou.add_trace(
    go.Scatter(
        x=list(
            touno2[
                touno2.nom_station == "Toulouse-Périphérique Trafic"
            ].mois_annee.unique()
        ),
        y=list(touno2[touno2.nom_station == "Toulouse-Périphérique Trafic"].valeur),
        legendgroup="groupe 2",
        name="Périphérique Trafic",
        mode="lines+markers",
    )
)
figtou.add_trace(
    go.Scatter(
        x=list(
            touno2[
                touno2.nom_station == "Toulouse - Port de l Embouchure Trafic"
            ].mois_annee.unique()
        ),
        y=list(
            touno2[
                touno2.nom_station == "Toulouse - Port de l Embouchure Trafic"
            ].valeur
        ),
        legendgroup="groupe 2",
        name="Port de l'Embouchure Trafic",
        mode="lines+markers",
    )
)
figtou.add_trace(
    go.Scatter(
        x=list(
            touno2[
                touno2.nom_station == "Toulouse-SETMI Eisenhower Industriel"
            ].mois_annee.unique()
        ),
        y=list(
            touno2[touno2.nom_station == "Toulouse-SETMI Eisenhower Industriel"].valeur
        ),
        legendgroup="groupe 2",
        name="SETMI Eisenhower Industriel",
        mode="lines+markers",
    )
)


# NOX
figtou.add_trace(
    go.Scatter(
        x=list(
            tounox[
                tounox.nom_station == "Toulouse - Rte Albi Trafic"
            ].mois_annee.unique()
        ),
        y=list(tounox[tounox.nom_station == "Toulouse - Rte Albi Trafic"].valeur),
        legendgroup="groupe 3",
        legendgrouptitle_text="<b>NOX</b>",
        name="Rte Albi Trafic",
        mode="lines+markers",
    )
)
figtou.add_trace(
    go.Scatter(
        x=list(
            tounox[
                tounox.nom_station == "Toulouse-Berthelot Urbain"
            ].mois_annee.unique()
        ),
        y=list(tounox[tounox.nom_station == "Toulouse-Berthelot Urbain"].valeur),
        legendgroup="groupe 3",
        name="Berthelot Urbain",
        mode="lines+markers",
    )
)
figtou.add_trace(
    go.Scatter(
        x=list(
            tounox[tounox.nom_station == "Toulouse-Jacquier Urbain"].mois_annee.unique()
        ),
        y=list(tounox[tounox.nom_station == "Toulouse-Jacquier Urbain"].valeur),
        legendgroup="groupe 3",
        name="Jacquier Urbain",
        mode="lines+markers",
    )
)
figtou.add_trace(
    go.Scatter(
        x=list(
            tounox[
                tounox.nom_station == "Toulouse-Périphérique Trafic"
            ].mois_annee.unique()
        ),
        y=list(tounox[tounox.nom_station == "Toulouse-Périphérique Trafic"].valeur),
        legendgroup="groupe 3",
        name="Périphérique Trafic",
        mode="lines+markers",
    )
)
figtou.add_trace(
    go.Scatter(
        x=list(
            tounox[
                tounox.nom_station == "Toulouse - Port de l Embouchure Trafic"
            ].mois_annee.unique()
        ),
        y=list(
            tounox[
                tounox.nom_station == "Toulouse - Port de l Embouchure Trafic"
            ].valeur
        ),
        legendgroup="groupe 3",
        name="Port de l'Embouchure Trafic",
        mode="lines+markers",
    )
)
figtou.add_trace(
    go.Scatter(
        x=list(
            tounox[
                tounox.nom_station == "Toulouse-SETMI Eisenhower Industriel"
            ].mois_annee.unique()
        ),
        y=list(
            tounox[tounox.nom_station == "Toulouse-SETMI Eisenhower Industriel"].valeur
        ),
        legendgroup="groupe 3",
        name="SETMI Eisenhower Industriel",
        mode="lines+markers",
    )
)


# O3
figtou.add_trace(
    go.Scatter(
        x=list(
            touo3[touo3.nom_station == "Toulouse-Berthelot Urbain"].mois_annee.unique()
        ),
        y=list(touo3[touo3.nom_station == "Toulouse-Berthelot Urbain"].valeur),
        legendgroup="groupe 4",
        legendgrouptitle_text="<b>O3</b>",
        name="Berthelot Urbain",
        mode="lines+markers",
    )
)
figtou.add_trace(
    go.Scatter(
        x=list(
            touo3[touo3.nom_station == "Toulouse-Jacquier Urbain"].mois_annee.unique()
        ),
        y=list(touo3[touo3.nom_station == "Toulouse-Jacquier Urbain"].valeur),
        legendgroup="groupe 4",
        name="Jacquier Urbain",
        mode="lines+markers",
    )
)
figtou.add_trace(
    go.Scatter(
        x=list(touo3[touo3.nom_station == "Station Pedagogique"].mois_annee.unique()),
        y=list(touo3[touo3.nom_station == "Station Pedagogique"].valeur),
        legendgroup="groupe 4",
        name="Station Pedagogique",
        mode="lines+markers",
    )
)


# PM10
figtou.add_trace(
    go.Scatter(
        x=list(
            toupm10[
                toupm10.nom_station == "Toulouse - Rte Albi Trafic"
            ].mois_annee.unique()
        ),
        y=list(toupm10[toupm10.nom_station == "Toulouse - Rte Albi Trafic"].valeur),
        legendgroup="groupe 5",
        legendgrouptitle_text="<b>PM10</b>",
        name="Rte Albi Trafic",
        mode="lines+markers",
    )
)
figtou.add_trace(
    go.Scatter(
        x=list(
            toupm10[
                toupm10.nom_station == "Toulouse-Berthelot Urbain"
            ].mois_annee.unique()
        ),
        y=list(toupm10[toupm10.nom_station == "Toulouse-Berthelot Urbain"].valeur),
        legendgroup="groupe 5",
        name="Berthelot Urbain",
        mode="lines+markers",
    )
)
figtou.add_trace(
    go.Scatter(
        x=list(
            toupm10[
                toupm10.nom_station == "Toulouse-Jacquier Urbain"
            ].mois_annee.unique()
        ),
        y=list(toupm10[toupm10.nom_station == "Toulouse-Jacquier Urbain"].valeur),
        legendgroup="groupe 5",
        name="Jacquier Urbain",
        mode="lines+markers",
    )
)
figtou.add_trace(
    go.Scatter(
        x=list(
            toupm10[
                toupm10.nom_station == "Toulouse-Périphérique Trafic"
            ].mois_annee.unique()
        ),
        y=list(toupm10[toupm10.nom_station == "Toulouse-Périphérique Trafic"].valeur),
        legendgroup="groupe 5",
        name="Périphérique Trafic",
        mode="lines+markers",
    )
)
figtou.add_trace(
    go.Scatter(
        x=list(
            toupm10[
                toupm10.nom_station == "Toulouse - Port de l Embouchure Trafic"
            ].mois_annee.unique()
        ),
        y=list(
            toupm10[
                toupm10.nom_station == "Toulouse - Port de l Embouchure Trafic"
            ].valeur
        ),
        legendgroup="groupe 5",
        name="Port de l'Embouchure Trafic",
        mode="lines+markers",
    )
)
figtou.add_trace(
    go.Scatter(
        x=list(
            toupm10[
                toupm10.nom_station == "Toulouse-SETMI Eisenhower Industriel"
            ].mois_annee.unique()
        ),
        y=list(
            toupm10[
                toupm10.nom_station == "Toulouse-SETMI Eisenhower Industriel"
            ].valeur
        ),
        legendgroup="groupe 5",
        name="SETMI Eisenhower Industriel",
        mode="lines+markers",
    )
)
figtou.add_trace(
    go.Scatter(
        x=list(
            toupm10[
                toupm10.nom_station == "Toulouse-Mazades Urbain"
            ].mois_annee.unique()
        ),
        y=list(toupm10[toupm10.nom_station == "Toulouse-Mazades Urbain"].valeur),
        legendgroup="groupe 5",
        name="Mazades Urbain",
        mode="lines+markers",
    )
)
figtou.add_trace(
    go.Scatter(
        x=list(
            toupm10[
                toupm10.nom_station == "Toulouse-SETMI Chapitre Industriel"
            ].mois_annee.unique()
        ),
        y=list(
            toupm10[toupm10.nom_station == "Toulouse-SETMI Chapitre Industriel"].valeur
        ),
        legendgroup="groupe 5",
        name="SETMI Chapitre Industriel",
        mode="lines+markers",
    )
)


# PM2.5
figtou.add_trace(
    go.Scatter(
        x=list(
            toupm2_5[
                toupm2_5.nom_station == "Toulouse - Rte Albi Trafic"
            ].mois_annee.unique()
        ),
        y=list(toupm2_5[toupm2_5.nom_station == "Toulouse - Rte Albi Trafic"].valeur),
        legendgroup="groupe 6",
        legendgrouptitle_text="<b>PM2.5</b>",
        name="Rte Albi Trafic",
        mode="lines+markers",
    )
)
figtou.add_trace(
    go.Scatter(
        x=list(
            toupm2_5[
                toupm2_5.nom_station == "Toulouse-Berthelot Urbain"
            ].mois_annee.unique()
        ),
        y=list(toupm2_5[toupm2_5.nom_station == "Toulouse-Berthelot Urbain"].valeur),
        legendgroup="groupe 6",
        name="Berthelot Urbain",
        mode="lines+markers",
    )
)
figtou.add_trace(
    go.Scatter(
        x=list(
            toupm2_5[
                toupm2_5.nom_station == "Toulouse - Port de l Embouchure Trafic"
            ].mois_annee.unique()
        ),
        y=list(
            toupm2_5[
                toupm2_5.nom_station == "Toulouse - Port de l Embouchure Trafic"
            ].valeur
        ),
        legendgroup="groupe 6",
        name="Port de l'Embouchure Trafic",
        mode="lines+markers",
    )
)
figtou.add_trace(
    go.Scatter(
        x=list(
            toupm2_5[
                toupm2_5.nom_station == "Toulouse-Mazades Urbain"
            ].mois_annee.unique()
        ),
        y=list(toupm2_5[toupm2_5.nom_station == "Toulouse-Mazades Urbain"].valeur),
        legendgroup="groupe 6",
        name="Mazades Urbain",
        mode="lines+markers",
    )
)


figtou.update_layout(
    title={"text": "<b>Différences dans Toulouse</b>", "x": 0.5, "xanchor": "center"},
    xaxis_title="<b>Mois</b>",
    yaxis_title="<b>Concentration (µg.m⁻³)</b>",
    legend={"title": "<b>Polluants (et stations)</b>"},
    paper_bgcolor="rgba(100,100,100,0)",  # Couleur de contour de graphique
    plot_bgcolor="rgba(100,100,100,0)",  # Couleur du fond du graphique
    font=dict(color="Grey", size=10),
)
figtou.show()

# %%
"""
COMPARAISON INTER VILLES
On choisit 6 villes de populations différentes:
    Toulouse
    Montpellier
    Tarbes
    Montauban
    Argèles-Gazost
    Peyrusse-Vieille
Et on comparaison leur taux de population selon les différents polluants.
On fait une sélection de une ou deux stations pour les deux plus grandes villes pour ne pas crouler sous les informations.

Stations sélectionnées pour Montpellier:
    Liberte Trafic : beaucoup de trafic routier
    Prés d'Arènes Urbain : valeurs moyennes et surtout présent à chaque polluant
Stations sélectionnées pour Toulouse:
    Periphérique Trafic : beaucoup de trafic routier, valeurs élevées
    Berthelot Urbain : valeurs moyennes et présent partout
"""

# On restreint le dataframe aux 4 autres villes
tar = df[df.nom_com == "TARBES"]
mon = df[df.nom_com == "MONTAUBAN"]
arg = df[df.nom_com == "ARGELES-GAZOST"]
pey = df[df.nom_com == "PEYRUSSE-VIEILLE"]

# Et maintenant aux polluants traités
## Tarbes
tarno = tar[tar.nom_poll == "NO"].sort_values(by="date_debut")
tarno2 = tar[tar.nom_poll == "NO2"].sort_values(by="date_debut")
tarnox = tar[tar.nom_poll == "NOX"].sort_values(by="date_debut")
taro3 = tar[tar.nom_poll == "O3"].sort_values(by="date_debut")
tarpm10 = tar[tar.nom_poll == "PM10"].sort_values(by="date_debut")
tarpm2_5 = tar[tar.nom_poll == "PM2.5"].sort_values(by="date_debut")


## Montauban
monno = mon[mon.nom_poll == "NO"].sort_values(by="date_debut")
monno2 = mon[mon.nom_poll == "NO2"].sort_values(by="date_debut")
monnox = mon[mon.nom_poll == "NOX"].sort_values(by="date_debut")
mono3 = mon[mon.nom_poll == "O3"].sort_values(by="date_debut")
monpm10 = mon[mon.nom_poll == "PM10"].sort_values(by="date_debut")
monpm2_5 = mon[mon.nom_poll == "PM2.5"].sort_values(by="date_debut")


## Argèles-Gazost
argno = arg[arg.nom_poll == "NO"].sort_values(by="date_debut")
argno2 = arg[arg.nom_poll == "NO2"].sort_values(by="date_debut")
argnox = arg[arg.nom_poll == "NOX"].sort_values(by="date_debut")
argo3 = arg[arg.nom_poll == "O3"].sort_values(by="date_debut")
argpm10 = arg[arg.nom_poll == "PM10"].sort_values(by="date_debut")
argpm2_5 = arg[arg.nom_poll == "PM2.5"].sort_values(by="date_debut")


## Peyrusse-Vieille
peyno = pey[pey.nom_poll == "NO"].sort_values(by="date_debut")
peyno2 = pey[pey.nom_poll == "NO2"].sort_values(by="date_debut")
peynox = pey[pey.nom_poll == "NOX"].sort_values(by="date_debut")
peyo3 = pey[pey.nom_poll == "O3"].sort_values(by="date_debut")
peypm10 = pey[pey.nom_poll == "PM10"].sort_values(by="date_debut")
peypm2_5 = pey[pey.nom_poll == "PM2.5"].sort_values(by="date_debut")

# Initialisation de la figure
fig = go.Figure()

# NO
fig.add_trace(
    go.Scatter(
        x=list(
            mtpno[
                mtpno.nom_station == "Montpellier - Prés d Arènes Urbain"
            ].mois_annee.unique()
        ),
        y=list(mtpno[mtpno.nom_station == "Montpellier - Prés d Arènes Urbain"].valeur),
        legendgroup="groupe 1",
        legendgrouptitle_text="<b>NO</b>",
        name="Montpellier - Prés d'Arènes",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(
            mtpno[mtpno.nom_station == "Montpellier Liberte Trafic"].mois_annee.unique()
        ),
        y=list(mtpno[mtpno.nom_station == "Montpellier Liberte Trafic"].valeur),
        legendgroup="groupe 1",
        name="Montpellier - Liberté",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(
            touno[touno.nom_station == "Toulouse-Berthelot Urbain"].mois_annee.unique()
        ),
        y=list(touno[touno.nom_station == "Toulouse-Berthelot Urbain"].valeur),
        legendgroup="groupe 1",
        name="Toulouse - Berthelot",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(
            touno[
                touno.nom_station == "Toulouse-Périphérique Trafic"
            ].mois_annee.unique()
        ),
        y=list(touno[touno.nom_station == "Toulouse-Périphérique Trafic"].valeur),
        legendgroup="groupe 1",
        name="Toulouse - Périphérique",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(tarno[tarno.nom_station == "Tarbes-Dupuy Urbain"].mois_annee.unique()),
        y=list(tarno[tarno.nom_station == "Tarbes-Dupuy Urbain"].valeur),
        legendgroup="groupe 1",
        name="Tarbes",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(
            monno[
                monno.nom_station == "Montauban - Ramierou Urbain"
            ].mois_annee.unique()
        ),
        y=list(monno[monno.nom_station == "Montauban - Ramierou Urbain"].valeur),
        legendgroup="groupe 1",
        name="Montauban",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(argno[argno.nom_station == "Argeles-Gazost"].mois_annee.unique()),
        y=list(argno[argno.nom_station == "Argeles-Gazost"].valeur),
        legendgroup="groupe 1",
        name="Argèles-Gazost",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(
            peyno[peyno.nom_station == "Peyrusse Vieille Rural"].mois_annee.unique()
        ),
        y=list(peyno[peyno.nom_station == "Peyrusse Vieille Rural"].valeur),
        legendgroup="groupe 1",
        name="Peyrusse-Vieille",
        mode="lines+markers",
    )
)


# NO2
fig.add_trace(
    go.Scatter(
        x=list(
            mtpno2[
                mtpno2.nom_station == "Montpellier - Prés d Arènes Urbain"
            ].mois_annee.unique()
        ),
        y=list(
            mtpno2[mtpno2.nom_station == "Montpellier - Prés d Arènes Urbain"].valeur
        ),
        legendgroup="groupe 2",
        legendgrouptitle_text="<b>NO2</b>",
        name="Montpellier - Prés d'Arènes",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(
            mtpno2[
                mtpno2.nom_station == "Montpellier Liberte Trafic"
            ].mois_annee.unique()
        ),
        y=list(mtpno2[mtpno2.nom_station == "Montpellier Liberte Trafic"].valeur),
        legendgroup="groupe 2",
        name="Montpellier - Liberté",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(
            touno2[
                touno2.nom_station == "Toulouse-Berthelot Urbain"
            ].mois_annee.unique()
        ),
        y=list(touno2[touno2.nom_station == "Toulouse-Berthelot Urbain"].valeur),
        legendgroup="groupe 2",
        name="Toulouse - Berthelot",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(
            touno2[
                touno2.nom_station == "Toulouse-Périphérique Trafic"
            ].mois_annee.unique()
        ),
        y=list(touno2[touno2.nom_station == "Toulouse-Périphérique Trafic"].valeur),
        legendgroup="groupe 2",
        name="Toulouse - Périphérique",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(tarno2[tarno2.nom_station == "Tarbes-Dupuy Urbain"].mois_annee.unique()),
        y=list(tarno2[tarno2.nom_station == "Tarbes-Dupuy Urbain"].valeur),
        legendgroup="groupe 2",
        name="Tarbes",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(
            monno2[
                monno2.nom_station == "Montauban - Ramierou Urbain"
            ].mois_annee.unique()
        ),
        y=list(monno2[monno2.nom_station == "Montauban - Ramierou Urbain"].valeur),
        legendgroup="groupe 2",
        name="Montauban",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(argno2[argno2.nom_station == "Argeles-Gazost"].mois_annee.unique()),
        y=list(argno2[argno2.nom_station == "Argeles-Gazost"].valeur),
        legendgroup="groupe 2",
        name="Argèles-Gazost",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(
            peyno2[peyno2.nom_station == "Peyrusse Vieille Rural"].mois_annee.unique()
        ),
        y=list(peyno2[peyno2.nom_station == "Peyrusse Vieille Rural"].valeur),
        legendgroup="groupe 2",
        name="Peyrusse-Vieille",
        mode="lines+markers",
    )
)


# NOX
fig.add_trace(
    go.Scatter(
        x=list(
            mtpnox[
                mtpnox.nom_station == "Montpellier - Prés d Arènes Urbain"
            ].mois_annee.unique()
        ),
        y=list(
            mtpnox[mtpnox.nom_station == "Montpellier - Prés d Arènes Urbain"].valeur
        ),
        legendgroup="groupe 3",
        legendgrouptitle_text="<b>NOX</b>",
        name="Montpellier - Prés d'Arènes",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(
            mtpnox[
                mtpnox.nom_station == "Montpellier Liberte Trafic"
            ].mois_annee.unique()
        ),
        y=list(mtpnox[mtpnox.nom_station == "Montpellier Liberte Trafic"].valeur),
        legendgroup="groupe 3",
        name="Montpellier - Liberté",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(
            tounox[
                tounox.nom_station == "Toulouse-Berthelot Urbain"
            ].mois_annee.unique()
        ),
        y=list(tounox[tounox.nom_station == "Toulouse-Berthelot Urbain"].valeur),
        legendgroup="groupe 3",
        name="Toulouse - Berthelot",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(
            tounox[
                tounox.nom_station == "Toulouse-Périphérique Trafic"
            ].mois_annee.unique()
        ),
        y=list(tounox[tounox.nom_station == "Toulouse-Périphérique Trafic"].valeur),
        legendgroup="groupe 3",
        name="Toulouse - Périphérique",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(tarnox[tarnox.nom_station == "Tarbes-Dupuy Urbain"].mois_annee.unique()),
        y=list(tarnox[tarnox.nom_station == "Tarbes-Dupuy Urbain"].valeur),
        legendgroup="groupe 3",
        name="Tarbes",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(
            monnox[
                monnox.nom_station == "Montauban - Ramierou Urbain"
            ].mois_annee.unique()
        ),
        y=list(monnox[monnox.nom_station == "Montauban - Ramierou Urbain"].valeur),
        legendgroup="groupe 3",
        name="Montauban",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(argnox[argnox.nom_station == "Argeles-Gazost"].mois_annee.unique()),
        y=list(argnox[argnox.nom_station == "Argeles-Gazost"].valeur),
        legendgroup="groupe 3",
        name="Argèles-Gazost",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(
            peynox[peynox.nom_station == "Peyrusse Vieille Rural"].mois_annee.unique()
        ),
        y=list(peynox[peynox.nom_station == "Peyrusse Vieille Rural"].valeur),
        legendgroup="groupe 3",
        name="Peyrusse-Vieille",
        mode="lines+markers",
    )
)


# O3
fig.add_trace(
    go.Scatter(
        x=list(
            mtpo3[
                mtpo3.nom_station == "Montpellier - Prés d Arènes Urbain"
            ].mois_annee.unique()
        ),
        y=list(mtpo3[mtpo3.nom_station == "Montpellier - Prés d Arènes Urbain"].valeur),
        legendgroup="groupe 4",
        legendgrouptitle_text="<b>O3</b>",
        name="Montpellier - Prés d'Arènes",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(
            touo3[touo3.nom_station == "Toulouse-Berthelot Urbain"].mois_annee.unique()
        ),
        y=list(touo3[touo3.nom_station == "Toulouse-Berthelot Urbain"].valeur),
        legendgroup="groupe 4",
        name="Toulouse - Berthelot",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(taro3[taro3.nom_station == "Tarbes-Dupuy Urbain"].mois_annee.unique()),
        y=list(taro3[taro3.nom_station == "Tarbes-Dupuy Urbain"].valeur),
        legendgroup="groupe 4",
        name="Tarbes",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(
            mono3[
                mono3.nom_station == "Montauban - Ramierou Urbain"
            ].mois_annee.unique()
        ),
        y=list(mono3[mono3.nom_station == "Montauban - Ramierou Urbain"].valeur),
        legendgroup="groupe 4",
        name="Montauban",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(argo3[argo3.nom_station == "Argeles-Gazost"].mois_annee.unique()),
        y=list(argo3[argo3.nom_station == "Argeles-Gazost"].valeur),
        legendgroup="groupe 4",
        name="Argèles-Gazost",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(
            peyo3[peyo3.nom_station == "Peyrusse Vieille Rural"].mois_annee.unique()
        ),
        y=list(peyo3[peyo3.nom_station == "Peyrusse Vieille Rural"].valeur),
        legendgroup="groupe 4",
        name="Peyrusse-Vieille",
        mode="lines+markers",
    )
)


# PM10
fig.add_trace(
    go.Scatter(
        x=list(
            mtppm10[
                mtppm10.nom_station == "Montpellier - Prés d Arènes Urbain"
            ].mois_annee.unique()
        ),
        y=list(
            mtppm10[mtppm10.nom_station == "Montpellier - Prés d Arènes Urbain"].valeur
        ),
        legendgroup="groupe 5",
        legendgrouptitle_text="<b>PM10</b>",
        name="Montpellier - Prés d'Arènes",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(
            mtppm10[
                mtppm10.nom_station == "Montpellier Liberte Trafic"
            ].mois_annee.unique()
        ),
        y=list(mtppm10[mtppm10.nom_station == "Montpellier Liberte Trafic"].valeur),
        legendgroup="groupe 5",
        name="Montpellier - Liberté",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(
            toupm10[
                toupm10.nom_station == "Toulouse-Berthelot Urbain"
            ].mois_annee.unique()
        ),
        y=list(toupm10[toupm10.nom_station == "Toulouse-Berthelot Urbain"].valeur),
        legendgroup="groupe 5",
        name="Toulouse - Berthelot",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(
            toupm10[
                toupm10.nom_station == "Toulouse-Périphérique Trafic"
            ].mois_annee.unique()
        ),
        y=list(toupm10[toupm10.nom_station == "Toulouse-Périphérique Trafic"].valeur),
        legendgroup="groupe 5",
        name="Toulouse - Périphérique",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(
            tarpm10[tarpm10.nom_station == "Tarbes-Dupuy Urbain"].mois_annee.unique()
        ),
        y=list(tarpm10[tarpm10.nom_station == "Tarbes-Dupuy Urbain"].valeur),
        legendgroup="groupe 5",
        name="Tarbes",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(
            monpm10[
                monpm10.nom_station == "Montauban - Ramierou Urbain"
            ].mois_annee.unique()
        ),
        y=list(monpm10[monpm10.nom_station == "Montauban - Ramierou Urbain"].valeur),
        legendgroup="groupe 5",
        name="Montauban",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(argpm10[argpm10.nom_station == "Argeles-Gazost"].mois_annee.unique()),
        y=list(argpm10[argpm10.nom_station == "Argeles-Gazost"].valeur),
        legendgroup="groupe 5",
        name="Argèles-Gazost",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(
            peypm10[peypm10.nom_station == "Peyrusse Vieille Rural"].mois_annee.unique()
        ),
        y=list(peypm10[peypm10.nom_station == "Peyrusse Vieille Rural"].valeur),
        legendgroup="groupe 5",
        name="Peyrusse-Vieille",
        mode="lines+markers",
    )
)


# PM2.5
fig.add_trace(
    go.Scatter(
        x=list(
            mtppm2_5[
                mtppm2_5.nom_station == "Montpellier - Prés d Arènes Urbain"
            ].mois_annee.unique()
        ),
        y=list(
            mtppm2_5[
                mtppm2_5.nom_station == "Montpellier - Prés d Arènes Urbain"
            ].valeur
        ),
        legendgroup="groupe 6",
        legendgrouptitle_text="<b>PM2.5</b>",
        name="Montpellier - Prés d'Arènes",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(
            mtppm2_5[
                mtppm2_5.nom_station == "Montpellier Liberte Trafic"
            ].mois_annee.unique()
        ),
        y=list(mtppm2_5[mtppm2_5.nom_station == "Montpellier Liberte Trafic"].valeur),
        legendgroup="groupe 6",
        name="Montpellier - Liberté",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(
            toupm2_5[
                toupm2_5.nom_station == "Toulouse-Berthelot Urbain"
            ].mois_annee.unique()
        ),
        y=list(toupm2_5[toupm2_5.nom_station == "Toulouse-Berthelot Urbain"].valeur),
        legendgroup="groupe 6",
        name="Toulouse - Berthelot",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(
            toupm2_5[
                toupm2_5.nom_station == "Toulouse-Périphérique Trafic"
            ].mois_annee.unique()
        ),
        y=list(toupm2_5[toupm2_5.nom_station == "Toulouse-Périphérique Trafic"].valeur),
        legendgroup="groupe 6",
        name="Toulouse - Périphérique",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(
            tarpm2_5[tarpm2_5.nom_station == "Tarbes-Dupuy Urbain"].mois_annee.unique()
        ),
        y=list(tarpm2_5[tarpm2_5.nom_station == "Tarbes-Dupuy Urbain"].valeur),
        legendgroup="groupe 6",
        name="Tarbes",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(
            monpm2_5[
                monpm2_5.nom_station == "Montauban - Ramierou Urbain"
            ].mois_annee.unique()
        ),
        y=list(monpm2_5[monpm2_5.nom_station == "Montauban - Ramierou Urbain"].valeur),
        legendgroup="groupe 6",
        name="Montauban",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(argpm2_5[argpm2_5.nom_station == "Argeles-Gazost"].mois_annee.unique()),
        y=list(argpm2_5[argpm2_5.nom_station == "Argeles-Gazost"].valeur),
        legendgroup="groupe 6",
        name="Argèles-Gazost",
        mode="lines+markers",
    )
)
fig.add_trace(
    go.Scatter(
        x=list(
            peypm2_5[
                peypm2_5.nom_station == "Peyrusse Vieille Rural"
            ].mois_annee.unique()
        ),
        y=list(peypm2_5[peypm2_5.nom_station == "Peyrusse Vieille Rural"].valeur),
        legendgroup="groupe 6",
        name="Peyrusse-Vieille",
        mode="lines+markers",
    )
)

# On modifie le layout du graphe
fig.update_layout(
    title={
        "text": "<b>Comparaison entre différentes villes d'Occitanie</b>",
        "x": 0.5,
        "xanchor": "center",
    },
    xaxis_title="<b>Mois</b>",
    yaxis_title="<b>Concentration (µg.m⁻³)</b>",
    legend={"title": "<b>Polluants (et stations)</b>"},
    paper_bgcolor="rgba(100,100,100,0)",  # Couleur de contour de graphique
    plot_bgcolor="rgba(100,100,100,0)",  # Couleur du fond du graphique
    font=dict(color="Grey", size=10),
)

# On affiche le graphe
fig.show()
# %%
