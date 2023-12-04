from meteo import graphique, trace, graphique_polar, graphique_axe, resultats, moy
from carte import Markero
import plotly.graph_objects as go
import pandas as pd
import folium

def test_graphique():
    fig = go.Figure()  # Créer une instance de la classe Figure de Plotly
    graphique(fig, "Titre", "Axe X")
    # Ajouter des assertions pour vérifier que la mise en page du graphique est correcte
    assert fig.layout.title.text == "Titre"
    assert fig.layout.xaxis.title.text == "Axe X"
    assert fig.layout.yaxis.title.text == "Concentration (µg.m⁻³)"

def test_trace():
    df = pd.DataFrame({'date': ['2023-01-01', '2023-01-02'], 'valeur': [10, 20]})
    courbe = trace(df, 'blue', 'Courbe', 'date')
    # Ajouter des assertions pour vérifier que la courbe a été correctement créée
    assert courbe.x.tolist() == ['2023-01-01', '2023-01-02']
    assert courbe.y.tolist() == [10, 20]

def test_graphique_polar():
    fig = go.Figure()
    graphique_polar(fig)

def test_graphique_axe():
    fig = go.Figure()
    graphique_axe(fig, "Titre", "Axe Y2")
    assert fig.layout.title.text == "Titre"
    assert fig.layout.xaxis.title.text == "Temps (jours)"
    assert fig.layout.yaxis.title.text == "Concentration (µg.m⁻³)"
    assert fig.layout.yaxis2.title.text == "Axe Y2"

def test_resultats():
    date = 'Jour'
    polluants_tous = ['Polluant1', 'Polluant2']
    polluants = pd.DataFrame({'Jour': ['2023-01-01', '2023-01-01', '2023-01-02', '2023-01-02'],
                              'valeur': [10, 15, 20, 25],
                              'nom_poll': ['Polluant1', 'Polluant2', 'Polluant1', 'Polluant2']})
    mapping = {'2023-01-01': 'Lundi', '2023-01-02': 'Mardi'}
    result = resultats(date, polluants_tous, polluants, mapping)
    assert result[0].shape == (2, 3)  # Vérifier la forme du DataFrame résultant

def test_moy():
    var = pd.DataFrame({'date': ['2023-01-01', '2023-01-01', '2023-01-02', '2023-01-02'],
                        'valeur': [10, 15, 20, 25],
                        'nom1': ['Polluant1', 'Polluant2', 'Polluant1', 'Polluant2']})
    resultat = moy(var, 'nom1', 'Polluant1', 'date')
    assert resultat.shape == (2, 2)  # Vérifier la forme du DataFrame résultant
    
def test_markero_sur_carte():
    # Créer une carte Folium
    carte = folium.Map(location=[0, 0], zoom_start=5)

    # Créer une instance de la classe Markero
    marqueur = Markero(100, -20, "nom", "popup")

    # Appeler la méthode SurCarte pour placer le marqueur sur la carte
    marqueur.SurCarte(carte)

    # Vérifier que le marqueur a été ajouté à la carte
    children = list(carte._children.values())  # Convertir en liste

    # Vérifier que les propriétés du marqueur sont correctes
    marqueur_map_child = children[1]
    assert marqueur_map_child.location == [100,-20]