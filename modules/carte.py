import time 
start = time.time()
import folium


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

end = time.time()
print(f"Execution time: {end - start:.5f} s.")

