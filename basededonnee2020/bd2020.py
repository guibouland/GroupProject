import pandas as pd
import plotly.express as px
from plotly.offline import plot
import numpy as np
x = np.arange(13)
bdd = pd.read_csv("/home/qufst/projetgroupe2/GroupProject/basededonnee2020/donnees2020.csv")
bdd2 = bdd[bdd['code_zone'] == 200070803]
bdd2['coleur']='blue'
bdd3 = bdd[bdd['code_zone'] == 200042372]
bdd3['coleur']='red'
bdd4 = bdd[bdd['code_zone'] == 248200099]
bdd4['coleur']='green'
bdd5 = bdd[bdd['code_zone'] == 244600573]
bdd5['coleur']='yellow'
bdd6 = bdd[bdd['code_zone'] == 241200187]
bdd6['coleur']='orange'
bdd7 = bdd[bdd['code_zone'] == 241200914]
bdd7['coleur']='purple'
bdd8 = bdd[bdd['code_zone'] == 243100518]
bdd8['coleur']='cyan'
bdd9 = bdd[bdd['code_zone'] == 200066223]
bdd9['coleur']='magenta'
bdd10 = bdd[bdd['code_zone'] == 200069144]
bdd10['coleur']='brown'
bdd11 = bdd[bdd['code_zone'] == 200034692]
bdd11['coleur']='gray'
bdd12 = bdd[bdd['code_zone'] == 243400819]
bdd12['coleur']='pink'
bdd13 = bdd[bdd['code_zone'] == 200035715]
bdd13['coleur']='teal'
bdd14 = bdd[bdd['code_zone'] == 200027183]
bdd14['coleur']='olive'

BDD = pd.concat([bdd2, bdd3, bdd4, bdd5, bdd6, bdd7, bdd8, bdd9, bdd10, bdd11, bdd12, bdd13, bdd14], ignore_index=True)
fig = px.scatter(BDD, x='date_ech', y='val_no2', animation_frame='date_ech',animation_group='code_zone', color='coleur',size = 'val_no2',hover_name='date_ech',log_x=False,range_x=(0,50),range_y=(-1,5))
#fig = px.line(BDD, x='date_ech', y='val_no2', animation_frame='date_ech', animation_group='code_zone', color='coleur', line_shape='linear')
fig.update_layout(
    title='évolution du no2 en stade en occitanie durant2020',
    xaxis_title='2020',
    yaxis_title='Stade de pollution')
fig.show()












