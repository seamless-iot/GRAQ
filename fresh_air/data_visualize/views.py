from django.shortcuts import render

import dash
import dash_core_components as dcc
import dash_html_components as html

from django_plotly_dash import DjangoDash
# Create your views here.
from django.http import HttpResponse
import os



def test(request):
    # -*- coding: utf-8 -*-
    import dash
    import dash_core_components as dcc
    import dash_html_components as html
    import plotly.graph_objs as go
    from data_visualize import models as dataPull
    import json
    from matplotlib import path

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    mapbox_access_token = "pk.eyJ1IjoicmFtaWphdmkiLCJhIjoiY2pyemJ5bm56MTdhMzRhbXRscjA0djd0dSJ9.TDjuO5EJnwFcz7hZCEXXwA"
    graphData = dataPull.graphDataGetter()
    graphData.run()
    locationData = graphData.getLocationData()
    print(locationData)
    lat=''
    lon=''
    sensorList=[]
    neighborhoods=[]
    buff=''

    for i in locationData:
        index = 0
        for a in i['device_gps_location']:
            if a == ',':
                lat += buff
                buff = ''
            elif index == len(i['device_gps_location'])-1:
                lon += buff
                buff = ''
            elif a != ' ':
                buff += a
            index += 1
        sensorList.append(dict(
            id=i['device_id'],
            coordinates=[float(lat), float(lon)],
            AQI=i['AQI']
        ))
        lat = ''
        lon = ''

    with open(os.path.dirname(__file__) + '/City_of_Grand_Rapids_Neighborhood_Areas.geojson') as f:
        geoFile = json.load(f)

    for i in geoFile['features']:
        neighborhoods.append(dict(
            name=i['properties']['NEBRH'],
            coordinates=i['geometry']['coordinates']
        ))

    listForMap = []

    for i in neighborhoods:
        coordinates = i['coordinates']
        coordinates2 = i['coordinates']

        tempJson = {
          "type": "FeatureCollection",
          "features": [
            {
              "type": "Feature",
              "properties": {},
              "geometry": {
                "type": "Polygon",
                "coordinates": [
                    coordinates
                ]
              }
            }
          ]
        }

        latHolder = coordinates2[0]
        coordinates2[0] = coordinates2[1]
        coordinates2[1] = latHolder
        tempPath = path.Path(coordinates2)
        AQICount=0
        sensorNum=0

        for a in sensorList:
            latHolder=a['coordinates'][0]
            a['coordinates'][0]=a['coordinates'][1]
            a['coordinates'][1]=latHolder
            tempPoint=a['coordinates']
            if tempPath.contains_point(tempPoint):
                print("contains point")
                AQICount+=a['AQI']
                sensorNum+=1

        #print(AQICount)
        #print(sensorNum)

        if sensorNum!=0:
            AQIAvg=AQICount/sensorNum
            print(AQIAvg)
            if AQIAvg <= 50:
                tempColor = 'rgba(0, 228, 0, 1)'
            elif AQIAvg > 50 and AQICount <= 100:
                tempColor = 'rgba(255, 255, 0, 1)'
            elif AQIAvg > 100 and AQICount <= 150:
                tempColor = 'rgba(255, 126, 0, 1)'
            elif AQIAvg > 150 and AQICount <= 200:
                tempColor = 'rgba(255, 0, 0, 1)'
            elif AQIAvg > 200 and AQICount <= 300:
                tempColor = 'rgba(153, 0, 76, 1)'
            elif AQIAvg > 300:
                tempColor = 'rgba(126, 0, 35, 1)'
        else:
            tempColor = 'rgba(245, 245, 245, 1)'

        AQICount = 0
        sensorNum = 0

        #DUBUGGING
        #print(tempColor)

        listForMap.append(dict(
            opacity=0.8,
            sourcetype='geojson',
            source=tempJson,
            type='fill',
            color=tempColor
        ))

    app = DjangoDash('Neighborhood', external_stylesheets=external_stylesheets)

    app.layout = html.Div(children=[
        html.H1(children='Air Quality Heatmap Sample Test'),
        html.Div(children='This is a test for the air quality heatmap '
                          'that will be displayed to our users through our web app.'),
        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    go.Scattermapbox(
                        mode='markers',
                        name="test",
                        hoverinfo='text'
                    )
                ],
                'layout': go.Layout(
                    autosize=True,
                    mapbox=dict(
                        layers = listForMap,
                        accesstoken=mapbox_access_token,
                        bearing=0,
                        center=dict(
                            lat=42.97,
                            lon=-85.68
                        ),
                        pitch=0,
                        zoom=10,
                    )
                )
            }
        )
    ])

    return render(request, 'report.html')
