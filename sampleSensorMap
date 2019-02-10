# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
import plotly.graph_objs as go

mapbox_access_token = 'pk.eyJ1IjoicmFtaWphdmkiLCJhIjoiY2pyemJ5bm56MTdhMzRhbXRscjA0djd0dSJ9.TDjuO5EJnwFcz7hZCEXXwA'
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Sensor Location Sample Test'),
    html.Div(children='This is a test for a map that shows were air quality sensors are '
                      'located. Right now this is made out of sample data.'),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                go.Scattermapbox(
                    lat=['42.969335', '42.975471', '42.985795',
                         '42.958977', '42.956529'],
                    lon=['-85.650579','-85.684851','-85.635066',
                         '-85.691903','-85.652708'],
                    mode='markers',
                    marker=dict(
                        size=9
                    ),
                    text=['Air Quality Sensor 1', 'Air Quality Sensor 2', 'Air Quality Sensor 3',
                          'Air Quality Sensor 4', 'Air Quality Sensor 5']
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

if __name__ == '__main__':
    app.run_server(debug=True)
