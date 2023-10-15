#%%
import pandas as pd
import plotly.express as px
from plotly.offline import plot
import numpy as np
bdd = pd.read_csv("/home/qufst/projetgroupe2/GroupProject/basededonnee2020/Mesure_annuelle_Region_Occitanie_Polluants_Principaux.csv")
bdd['valeur'].fillna(0, inplace=True)
bdd1 = bdd[bdd['nom_poll'] == 'NO']
bdd2 = bdd[bdd['nom_poll'] == 'NO2']
bdd3 = bdd[bdd['nom_poll'] == 'NOX']
bdd4 = bdd[bdd['nom_poll'] == 'O3']
bdd5 = bdd[bdd['nom_poll'] == 'PM10']
#%%NO
fig = px.scatter(bdd1, x='date_debut', y='valeur', animation_frame='date_debut',animation_group='nom_com', color='nom_dept',size = 'valeur',hover_name='date_debut',log_x=False,range_x=(0,5),range_y=(-1,50))
#fig = px.line(BDD, x='date_ech', y='val_no2', animation_frame='date_ech', animation_group='code_zone', color='coleur', line_shape='linear')
fig.update_layout(
    title='évolution de la pollution moyenne en NO des 5 dernières années en occitanie',
    xaxis_title='année',
    yaxis_title='valeur ug.m-3')
fig.show()
#%%NO2
fig = px.scatter(bdd2, x='date_debut', y='valeur', animation_frame='date_debut',animation_group='nom_com', color='nom_dept',size = 'valeur',hover_name='date_debut',log_x=False,range_x=(0,5),range_y=(-1,20))
fig.update_layout(
    title='évolution de la pollution moyenne en NO2 des 5 dernières années en occitanie',
    xaxis_title='année',
    yaxis_title='valeur ug.m-3')
fig.show()
#%%NOX
fig = px.scatter(bdd3, x='date_debut', y='valeur', animation_frame='date_debut',animation_group='nom_com', color='nom_dept',size = 'valeur',hover_name='date_debut',log_x=False,range_x=(0,5),range_y=(-1,50))
fig.update_layout(
    title='évolution de la pollution moyenne en NOX des 5 dernières années en occitanie',
    xaxis_title='année',
    yaxis_title='valeur ug.m-3')
fig.show()
#%%O3
fig = px.scatter(bdd4, x='date_debut', y='valeur', animation_frame='date_debut',animation_group='nom_com', color='nom_dept',size = 'valeur',hover_name='date_debut',log_x=False,range_x=(0,5),range_y=(10,100))
fig.update_layout(
    title='évolution de la pollution moyenne en O3 des 5 dernières années en occitanie',
    xaxis_title='année',
    yaxis_title='valeur ug.m-3')
fig.show()
#%%PM10
fig = px.scatter(bdd5, x='date_debut', y='valeur', animation_frame='date_debut',animation_group='nom_com', color='nom_dept',size = 'valeur',hover_name='date_debut',log_x=False,range_x=(0,5),range_y=(-1,20))
fig.update_layout(
    title='évolution de la pollution moyenne en PM10 des 5 dernières années en occitanie',
    xaxis_title='année',
    yaxis_title='valeur ug.m-3')
fig.show()
#%%
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Charger les données depuis le fichier CSV
bdd = pd.read_csv("/home/qufst/projetgroupe2/GroupProject/basededonnee2020/Mesure_annuelle_Region_Occitanie_Polluants_Principaux.csv")
bdd['valeur'].fillna(0, inplace=True)

# Créer une application Dash
app = dash.Dash(__name__)

# Définir la mise en page de l'application
app.layout = html.Div([
    html.H1("Évolution de la pollution moyenne en Occitanie"),
    dcc.Dropdown(
        id='polluant-dropdown',
        options=[
            {'label': 'NO', 'value': 'NO'},
            {'label': 'NO2', 'value': 'NO2'},
            {'label': 'NOX', 'value': 'NOX'},
            {'label': 'O3', 'value': 'O3'},
            {'label': 'PM10', 'value': 'PM10'}
        ],
        value='NO'
    ),
    dcc.Graph(id='pollution-graph')
])

# Définir la mise à jour du graphique en fonction de la sélection du polluant
@app.callback(
    Output('pollution-graph', 'figure'),
    [Input('polluant-dropdown', 'value')]
)
def update_pollution_graph(selected_polluant):
    filtered_data = bdd[bdd['nom_poll'] == selected_polluant]

    fig = px.scatter(filtered_data, x='date_debut', y='valeur', animation_frame='date_debut', color='nom_dept', size='valeur', hover_name='date_debut', log_x=False, range_x=(0, 5), range_y=(-1, 100))

    fig.update_layout(
        title=f'Évolution de la pollution moyenne en {selected_polluant} des 5 dernières années en Occitanie',
        xaxis_title='année',
        yaxis_title=f'Valeur {selected_polluant} (ug.m-3)'
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

# %%
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Charger les données
bdd = pd.read_csv("/home/qufst/projetgroupe2/GroupProject/basededonnee2020/Mesure_annuelle_Region_Occitanie_Polluants_Principaux.csv")
bdd['valeur'].fillna(0, inplace=True)

# Créer une application Dash
app = dash.Dash(__name__)

# Créer la mise en page de l'application
app.layout = html.Div([
    html.H1("Évolution de la pollution en Occitanie"),
    
    # Sélection du polluant
    dcc.Dropdown(
        id='polluant-dropdown',
        options=[
            {'label': 'NO', 'value': 'NO'},
            {'label': 'NO2', 'value': 'NO2'},
            {'label': 'NOX', 'value': 'NOX'},
            {'label': 'O3', 'value': 'O3'},
            {'label': 'PM10', 'value': 'PM10'}
        ],
        value='NO'
    ),
    
    # Graphique interactif
    dcc.Graph(id='pollution-graph')
])

# Mettre à jour le graphique en fonction de la sélection du polluant
@app.callback(
    Output('pollution-graph', 'figure'),
    [Input('polluant-dropdown', 'value')]
)
def update_graph(selected_polluant):
    filtered_data = bdd[bdd['nom_poll'] == selected_polluant]
    fig = px.scatter(
        filtered_data, x='date_debut', y='valeur',
        animation_frame='date_debut', animation_group='nom_com',
        color='nom_dept', size='valeur', hover_name='date_debut',
        log_x=False, range_x=(0, 5), range_y=(-1, 100)
    )
    fig.update_layout(
        title=f'Évolution de la pollution moyenne en {selected_polluant} des 5 dernières années en Occitanie',
        xaxis_title='Année',
        yaxis_title='Valeur ug.m-3'
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

# %%
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Charger les données
bdd = pd.read_csv("/home/qufst/projetgroupe2/GroupProject/basededonnee2020/Mesure_annuelle_Region_Occitanie_Polluants_Principaux.csv")
bdd['valeur'].fillna(0, inplace=True)

# Créer une application Dash
app = dash.Dash(__name__)

# Créer la mise en page de l'application
app.layout = html.Div([
    html.H1("Évolution de la pollution en Occitanie"),
    
    # Sélection du polluant
    dcc.Dropdown(
        id='polluant-dropdown',
        options=[
            {'label': 'NO', 'value': 'NO cliquer pour changer'},
            {'label': 'NO2', 'value': 'NO2 cliquer pour changer'},
            {'label': 'NOX', 'value': 'NOX cliquer pour changer'},
            {'label': 'O3', 'value': 'O3 cliquer pour changer'},
            {'label': 'PM10', 'value': 'PM10 cliquer pour changer'}
        ],
        value='NO'
    ),
    
    # Graphique interactif
    dcc.Graph(id='pollution-graph')
])

# Mettre à jour le graphique en fonction de la sélection du polluant
@app.callback(
    Output('pollution-graph', 'figure'),
    [Input('polluant-dropdown', 'value')]
)
def update_graph(selected_polluant):
    filtered_data = bdd[bdd['nom_poll'] == selected_polluant]
    fig = px.scatter(
        filtered_data, x='date_debut', y='valeur',
        animation_frame='date_debut', animation_group='nom_com',
        color='nom_dept', size='valeur', hover_name='date_debut',
        log_x=False, range_x=(0, 5), range_y=(-1, 100)
    )
    
    # Ralentir l'animation (1000 ms = 1 seconde)
    fig.update_layout(
        title=f'Évolution de la pollution moyenne en {selected_polluant} des 5 dernières années en Occitanie',
        xaxis_title='Année',
        yaxis_title='Valeur ug.m-3'
    )
    
    # Spécifier la durée de chaque frame (animation)
    frame_duration = 1000  # Durée de chaque frame en millisecondes
    fig.update_traces(marker=dict(size=filtered_data['valeur']))
    fig.add_traces
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

# %%
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Charger les données
bdd = pd.read_csv("/home/qufst/projetgroupe2/GroupProject/basededonnee2020/Mesure_annuelle_Region_Occitanie_Polluants_Principaux.csv")
bdd['valeur'].fillna(0, inplace=True)

# Créer une application Dash
app = dash.Dash(__name__)

# Créer la mise en page de l'application
app.layout = html.Div([
    html.H1("Évolution de la pollution en Occitanie"),
    
    # Sélection du polluant
    dcc.Dropdown(
        id='polluant-dropdown',
        options=[
            {'label': 'NO', 'value': 'NO'},
            {'label': 'NO2', 'value': 'NO2'},
            {'label': 'NOX', 'value': 'NOX'},
            {'label': 'O3', 'value': 'O3'},
            {'label': 'PM10', 'value': 'PM10'}
        ],
        value='NO'
    ),
    
    # Graphique interactif
    dcc.Graph(id='pollution-graph')
])

# Mettre à jour le graphique en fonction de la sélection du polluant
@app.callback(
    Output('pollution-graph', 'figure'),
    [Input('polluant-dropdown', 'value')]
)
def update_graph(selected_polluant):
    filtered_data = bdd[bdd['nom_poll'] == selected_polluant]
    fig = px.scatter(
        filtered_data, x='date_debut', y='valeur',
        animation_frame='date_debut', animation_group='nom_com',
        color='nom_dept', size='valeur', hover_name='date_debut',
        log_x=False, range_x=(0, 5), range_y=(-1, 100)
    )
    fig.update_layout(
        title=f'Évolution de la pollution moyenne en {selected_polluant} des 5 dernières années en Occitanie',
        xaxis_title='Année',
        yaxis_title='Valeur ug.m-3'
    )
    
    # Ajouter une trace pour chaque département
    for nom_dept in filtered_data['nom_dept'].unique():
        trace_data = filtered_data[filtered_data['nom_dept'] == nom_dept]
        fig.add_scatter(
            x=trace_data['date_debut'],
            y=trace_data['valeur'],
            name=nom_dept  # Utilisez le nom du département comme nom de la trace
        )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)




