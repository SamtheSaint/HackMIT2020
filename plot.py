import pandas as pd
import plotly
import plotly.graph_objs as go

from plotly.graph_objs import *

df_merged = pd.read_csv("csvfile.csv")  # TODO: REPLACE CSV FILENAME HERE

date = "2020-07-20"

df_sect = df_merged[df_merged['date'] == date]

scl = [[0.0, '#ffffff'], [0.2, '#ff9999'], [0.4, '#ff4d4d'],
       [0.6, '#ff1a1a'], [0.8, '#cc0000'], [1.0, '#4d0000']]

for col in df_sect.columns:
    df_sect[col] = df_sect[col].astype(str)

df_sect['text'] = 'Lat: ' + df_sect['Latitude'] + 'Long: ' + df_sect['Longitude'] + 'Phone Calls: ' + \
                  df_sect['marquee'] + 'Confirmed Cases: ' + df_sect['gov']
data = [dict(
    type='choropleth',  # type of map-plot
    colorscale=scl,
    autocolorscale=False,
    lon=df_sect['Longitude'],
    lat=df_sect['Latitude'],
    z=df_sect['Confirmed Cases'].astype(float),
    text=df_sect['text'],  # hover text
    marker=dict(
        line=dict(
            color='rgb(255,255,255)',
            width=2)),
    colorbar=dict(
        title="Confirmed Cases")
)
]

layout = dict(
    title=date,
    geo=dict(
        scope='europe',
        projection=dict(type='equirectangular'),
    ),
)

fig = dict(data=data, layout=layout)

plotly.offline.iplot(fig)
