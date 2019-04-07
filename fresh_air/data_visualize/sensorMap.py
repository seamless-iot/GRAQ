import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
import plotly.graph_objs as go
from data_visualize import models as dataPull
from django_plotly_dash import DjangoDash

mapbox_access_token = 'pk.eyJ1IjoicmFtaWphdmkiLCJhIjoiY2pyemJ5bm56MTdhMzRhbXRscjA0djd0dSJ9.TDjuO5EJnwFcz7hZCEXXwA'
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('sensormap', external_stylesheets=external_stylesheets)

graphData = dataPull.graphDataGetter()
graphData.run()
locationData = graphData.getLocationData()
latC=[]
lonC=[]
textC=[]

buff=''
for i in locationData:
    index = 0
    for a in i['device_gps_location']:
        if(a == ','):
            latC.append(buff)
            buff = ''
        elif(index == len(i['device_gps_location'])-1):
            lonC.append(buff)
            buff = ''
        elif(a != ' '):
            buff += a
        index += 1

    textC.append('Device ID: ' + i['device_id'] + '. Device Type: ' + i['device_type'] + '. Current AQI measured: ' ) #+ i['aqi'] )


app.layout = html.Div(children=[
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                go.Scattermapbox(
                    lat=latC,
                    lon=lonC,
                    mode='markers',
                    marker=dict(
                        size=9
                    ),
                    text=textC
                )
            ],
            'layout': go.Layout(
                autosize=True,
                hovermode='closest',
                mapbox=dict(
                    accesstoken=mapbox_access_token,
                    bearing=0,
                    center=dict(
                        lat=42.97,
                        lon=-85.68
                    ),
                    pitch=0,
                    zoom=10
                ),
            )
        }
    )
])
