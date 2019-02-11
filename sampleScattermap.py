# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
mapbox_access_token = "pk.eyJ1IjoicmFtaWphdmkiLCJhIjoiY2pyemJ5bm56MTdhMzRhbXRscjA0djd0dSJ9.TDjuO5EJnwFcz7hZCEXXwA"

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Air Quality Heatmap Sample Test'),
    html.Div(children='This is a test for the air quality heatmap '
                      'that will be displayed to our users through our web app.'),

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
                height=600,
                autosize=True,
                hovermode='closest',
                mapbox=dict(
                    layers=[
                        dict(
                            sourcetype='geojson',
                            source='https://raw.githubusercontent.com/chris-schertenlieb/fresh-air-cis467/master/testMap1.json',
                            type='fill',
                            color='rgba(163,22,19,0.8)'
                        ),
                        dict(
                            sourcetype='geojson',
                            source='https://raw.githubusercontent.com/chris-schertenlieb/fresh-air-cis467/master/testMap2.json',
                            type='fill',
                            color='rgba(40,0,113,0.8)'
                        )
                    ],
                    accesstoken=mapbox_access_token,
                    bearing=0,
                    center=dict(
                        lat=42.97,
                        lon=-85.68
                    ),
                    pitch=0,
                    zoom=10,
                    style='light'
                )
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
