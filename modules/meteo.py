import plotly.graph_objects as go
import pandas as pd


def graphique(fig, titre, xaxis_title):
    """Mise en page d'un graphique cartésien"""
    fig.update_layout(
        title=titre,
        xaxis=dict(title=xaxis_title),
        yaxis=dict(title="Concentration (µg.m⁻³)", side="left", position=0),
        font_size=15,
        showlegend=True,
        legend=dict(x=1, y=1),
        paper_bgcolor="rgba(230, 230, 230,0)",
        # Couleur de contour de graphique
        plot_bgcolor="rgba(100,100,100,0)",  # Couleur du fond du graphique
        font=dict(color="Grey"),
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="LightGrey")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="LightGrey")


def trace(df, color, name, date):
    """Ajout courbe sur un graphique cartésien"""
    return go.Scatter(
        x=df[date],
        y=df["valeur"],
        mode="lines",
        line=dict(width=2, color=color),
        name=name,
    )


def graphique_polar(fig):
    """Mise en page d'un graphique polaire"""
    fig.update_layout(
        font_size=15,
        font_color="grey",
        showlegend=True,
        polar=dict(
            bgcolor="rgba(223, 223, 223,0)",
            angularaxis=dict(linewidth=3, showline=True, linecolor="grey"),
            radialaxis=dict(
                showline=True,
                linewidth=2,
                gridcolor="rgba(100, 100, 100,0.5)",
                gridwidth=2,
            ),
            angularaxis_gridcolor="rgba(100, 100, 100,0.5)",
            radialaxis_linecolor="rgb(100, 100, 100)",
            radialaxis_color="grey",
        ),
        paper_bgcolor="rgba(230, 230, 230,0)",  # Couleur de contour de graphique
        plot_bgcolor="rgba(230, 230, 230,0)",  # Couleur du fond du graphique
    )


def graphique_axe(fig, titre, yaxis2_title):
    """Mise en page d'un graphique cartésien avec 2 axes y"""
    fig.update_layout(
        title=titre,
        xaxis=dict(title="Temps (jours)"),  # Abscisse
        yaxis=dict(title="Concentration (µg.m⁻³)", side="left", position=0),  # Ordonnée
        yaxis2=dict(
            title=yaxis2_title, overlaying="y", side="right", position=1
        ),  # Deuxième ordonnée
        font_size=15,
        showlegend=True,
        paper_bgcolor="rgba(230, 230, 230,0)",  # Couleur de contour de graphique
        plot_bgcolor="rgba(100,100,100,0)",  # Couleur du fond du graphique
        font=dict(color="Grey"),
        legend=dict(x=1.1, y=1),
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="LightGrey")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="LightGrey")


def resultats(date, polluants_tous, polluants, mapping):
    """moyenne des valeurs des polluants"""
    resultat = []
    # Moyenne des valeurs des polluants par jour
    for polluant in polluants_tous:
        # Moyenne des valeurs de chaque polluant par jour
        df_polluant = (
            polluants[polluants["nom_poll"] == polluant]
            .groupby(date)["valeur"]
            .mean()
            .reset_index()
        )
        # Ajout de la colonne éponyme pour la reconnaître
        df_polluant["nom"] = polluant
        if date == "Jour":
            # Trier par date et la renommer
            df_polluant["Jour"] = pd.Categorical(
                df_polluant["Jour"],
                categories=[
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday",
                ],
                ordered=True,
            )
            df_polluant = df_polluant.sort_values(date)
        # Renommer la date
        df_polluant[date] = df_polluant[date].replace(mapping)
        resultat.append(df_polluant)
    return resultat


def moy(var, nom1, nom2, date):
    """Moyenne des valeurs des variables par date"""
    return var[(var[nom1] == nom2)].groupby(date)["valeur"].mean().reset_index()
