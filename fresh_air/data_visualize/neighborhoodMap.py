import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import fresh_air.data_pull as dataPull
from django_plotly_dash import DjangoDash



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
mapbox_access_token = "pk.eyJ1IjoicmFtaWphdmkiLCJhIjoiY2pyemJ5bm56MTdhMzRhbXRscjA0djd0dSJ9.TDjuO5EJnwFcz7hZCEXXwA"
graphData = dataPull.graphDataGetter()
graphData.run()
mapData = graphData.getMapData()
locationData = graphData.getLocationData()

app = DjangoDash('NeighborHoodMap', external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                go.Scattermapbox(
                    lat=['45.5017'],
                    lon=['-73.5673'],
                    mode='markers',
                )
            ],
            'layout': go.Layout(
                autosize=True,
                hovermode='closest',
                mapbox=dict(
                    layers=[
                        dict(
                            sourcetype='geojson',
                            source='https://raw.githubusercontent.com/chris-schertenlieb/fresh-air-cis467/'
                                   'master/City_of_Grand_Rapids_Neighborhood_Areas.geojson',
                            type='fill',
                            color='rgba(163,22,19,0.8)'
                        )
                    ],
                    accesstoken=mapbox_access_token,
                    bearing=0,
                    center=dict(
                        lat=42.97,
                        lon=-85.68
                    ),
                    pitch=0,
                    zoom=10
                )
            )
        }
    )
])
