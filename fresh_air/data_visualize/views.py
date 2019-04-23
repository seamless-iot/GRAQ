from django.shortcuts import render

import dash
import dash_core_components as dcc
import dash_html_components as html

from django_plotly_dash import DjangoDash
# Create your views here.
from django.http import HttpResponse
import os
from django.urls import resolve




def report(request):
    # -*- coding: utf-8 -*-
    import dash
    import dash_core_components as dcc
    import dash_html_components as html
    import plotly.graph_objs as go
    from  data_visualize import models as dataPull
    import json
    from matplotlib import path
    import math

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    mapbox_access_token = "pk.eyJ1IjoicmFtaWphdmkiLCJhIjoiY2pyemJ5bm56MTdhMzRhbXRscjA0djd0dSJ9.TDjuO5EJnwFcz7hZCEXXwA"

    # Initiating and running dataPull script. This script is used to pull data from the DynamoDB
    graphData = dataPull.graphDataGetter()
    graphData.run()

    # getLocationData() returns the location, device ID, device type and AQI for all sensors on the DB
    locationData = graphData.getLocationData()

    # Instantiating variables
    lat = ''
    lon = ''
    sensorList = []
    neighborhoods = []
    buff = ''
    listForMap = []
    AQIList = []
    neighborhoodsToModify = []

    # This nested for loop gets the data from getLocationData() and stores the relevant variables on the sensorList
    # dictionary list, which will later be used. getLocationData() returns the GPS coordinates as a string, so
    # they must be separated into latitude and longitude and then stored as floats on different variables
    for i in locationData:
        index = 0
        for a in i['device_gps_location']:
            if a == ',':
                lon += buff
                buff = ''
            elif index == len(i['device_gps_location'])-1:
                lat += buff
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

    # Open the GeoJson file containing the different neighborhoods of Grand Rapids
    target_dir = os.path.dirname(__file__)
    file_path = os.path.join(target_dir, 'City_of_Grand_Rapids_Neighborhood_Areas.geojson')

    with open(file_path) as f:
        geoFile = json.load(f)

    # From this file we only need the name of the neighborhoods, in order to be able to identify them, and the coordinates
    # of the polygons that make up the neighborhood shapes. These variables will be saved to the neighborhoods dictionary
    # list
    for i in geoFile['features']:
        neighborhoods.append(dict(
            name=i['properties']['NEBRH'],
            coordinates=i['geometry']['coordinates']
        ))

    # Loop through every entry of the neighborhoods dictionary list
    for i in neighborhoods:
        # Create two copies of the neighborhood coordinates
        coordinates = i['coordinates']
        coordinates2 = i['coordinates']

        # For every neighborhood in the neighborhoods dict list we create a temporary GeoJson object
        # A GeoJson object is the same as a Json object, but specific for mapping points, shapes, etc.
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

        # In the second copy the neighborhood coordinates we will change the order of the latitude and longitude. This is
        # because the matPlotLib, which is used below, uses the format (latitude, longitude) while GeoJson uses the
        # format (longitude, latitude).
        latHolder = coordinates2[0]
        coordinates2[0] = coordinates2[1]
        coordinates2[1] = latHolder
        tempPath = path.Path(coordinates2)
        AQICount = 0
        sensorNum = 0

        for a in sensorList:
            # For every sensor in sensorList a temp point is created
            tempPoint = a['coordinates']
            # Check if the point is contained in the neighborhood
            if tempPath.contains_point(tempPoint):
                # If the sensor is in the neighborhood, then sum its AQI to AQICount and increase the sensor number by 1
                AQICount += a['AQI']
                sensorNum += 1

        # Check if there is at least 1 sensor the neighborhood
        if sensorNum != 0:
            # Compute the AQI average from the reading from the different sensors
            AQIAvg = AQICount/sensorNum
            AQIList.append(AQIAvg)
            # Assign a color to the neighborhood depending on its AQI measurements. This color assignment corresponds
            # to the map legend
            if AQIAvg <= 16:
                tempColor = 'rgba(25, 191, 0, 1)'
            elif 16 < AQIAvg <= 33:
                tempColor = 'rgba(48, 187, 1, 1)'
            elif 33 < AQIAvg <= 50:
                tempColor = 'rgba(71, 184, 2, 1)'
            elif 50 < AQIAvg <= 66:
                tempColor = 'rgba(93, 180, 4, 1)'
            elif 66 < AQIAvg <= 83:
                tempColor = 'rgba(114, 177, 5, 1)'
            elif 83 < AQIAvg <= 100:
                tempColor = 'rgba(134, 174, 6, 1)'
            elif 100 < AQIAvg <= 116:
                tempColor = 'rgba(152, 170, 8, 1)'
            elif 116 < AQIAvg <= 133:
                tempColor = 'rgba(167, 165, 9, 1)'
            elif 133 < AQIAvg <= 150:
                tempColor = 'rgba(164, 142, 10, 1)'
            elif 150 < AQIAvg <= 166:
                tempColor = 'rgba(160, 120, 11, 1)'
            elif 166 < AQIAvg <= 183:
                tempColor = 'rgba(157, 100, 12, 1)'
            elif 183 < AQIAvg <= 200:
                tempColor = 'rgba(154, 80, 13, 1)'
            elif 200 < AQIAvg <= 233:
                tempColor = 'rgba(150, 62, 14, 1)'
            elif 233 < AQIAvg <= 266:
                tempColor = 'rgba(147, 44, 15, 1)'
            elif 266 < AQIAvg <= 300:
                tempColor = 'rgba(144, 28, 15, 1)'
            elif 300 < AQIAvg <= 366:
                tempColor = 'rgba(140, 16, 20, 1)'
            elif 366 < AQIAvg <= 433:
                tempColor = 'rgba(137, 17, 36, 1)'
            elif AQIAvg > 433:
                tempColor = 'rgba(134, 18, 51, 1)'
        # If neighborhood has no data, assign color grey
        else:
            tempColor = 'rgba(67, 67, 67, 0.4)'
            AQIList.append(0)

        AQICount = 0
        sensorNum = 0

        # Append a dictionary to the listForMap list. This dict includes the temporary GeoJson object created from the
        # neighborhood, the color assigned, and other properties that are common to all neighborhoods in the list
        listForMap.append(dict(
            opacity=0.8,
            sourcetype='geojson',
            source=tempJson,
            type='fill',
            color=tempColor
        ))
        # For every neighborhood, another additional dictionary will be appended for drawing the borders of each
        # neighborhood. This is why type='line'
        listForMap.append(dict(
            opacity=0.8,
            sourcetype='geojson',
            source=tempJson,
            type='line',
            color='#000000',
            line={
                'width': 1
            }
        ))

    # This is the AQI Averaging Algorithm. It will check the neighborhoods that have no AQI data and will approximate an
    # average AQI based on the data of its neighbors. Therefore, only neighborhoods that are contiguous to other
    # neighborhoods with data will be able to get an approximate AQI.
    # This can be a very CPU-intensive algorithm and it may slow down the loading of the maps quite a bit for certain
    # users with a slow internet connection or a slow CPU.
    #
    # The principle of this algorithm is the following: For every neighborhood with no data, it will check if there are any
    # neighborhoods with data that are adjacent to it. It will do this by checking the distance of all the points of the
    # two neighborhoods being checked. If the points are close enough, then it considers the neighborhoods to be adjacent
    #
    # Loop through all neighborhoods in the listForMap list
    for nonFilledNeighborhood in listForMap:
        # If the index is even and has no AQI data
        if listForMap.index(nonFilledNeighborhood) % 2 == 0 and nonFilledNeighborhood['color'] == 'rgba(67, 67, 67, 0.4)':
            # Reset AQI approximation and count variables to 0
            AQIApprox = 0
            approxCt = 0
            # Loop through all neighborhoods in the listForMap list
            for filledNeighborhood in listForMap:
                # If the index is even and has AQI data
                if listForMap.index(filledNeighborhood) % 2 == 0 and filledNeighborhood['color'] != 'rgba(67, 67, 67, 0.4)':
                    # Assume the neighborhoods are not adjacent
                    isAdjacent = False
                    # Loop through all the points of the neighborhood maps
                    for pt1 in filledNeighborhood['source']['features'][0]['geometry']['coordinates'][0]:
                        for pt2 in nonFilledNeighborhood['source']['features'][0]['geometry']['coordinates'][0]:
                            # Calculate the distance between the points
                            if math.sqrt(((pt1[1] - pt2[1])**2)+((pt1[0] - pt2[0])**2)) <= 0.0001:
                                # If the distance is small enough, then the neighborhoods are adjacent
                                isAdjacent = True
                                # If it's adjacent, then increase approx count by 1 and break out of the inner loop
                                approxCt += 1
                                break
                        if isAdjacent:
                            # Break out of the outer loop
                            break
                    if isAdjacent:
                        # If the neighborhood is adjacent, then add it's AQI to AQIApprox
                        AQIApprox += AQIList[int((listForMap.index(filledNeighborhood))/2)]
            if approxCt != 0:
                # Append dictionary with index and approximate AQI of neighborhood whose AQI we've estimated
                neighborhoodsToModify.append(dict(
                    index=listForMap.index(nonFilledNeighborhood),
                    AQI=AQIApprox/approxCt
                ))
    # Loop through the neighborhoodsToModify list and change the color of the neighborhood according to its AQI
    for x in neighborhoodsToModify:
        if x['AQI'] <= 16:
            listForMap[x['index']]['color'] = 'rgba(25, 191, 0, 1)'
        elif 16 < x['AQI'] <= 33:
            listForMap[x['index']]['color'] = 'rgba(48, 187, 1, 1)'
        elif 33 < x['AQI'] <= 50:
            listForMap[x['index']]['color'] = 'rgba(71, 184, 2, 1)'
        elif 50 < x['AQI'] <= 66:
            listForMap[x['index']]['color'] = 'rgba(93, 180, 4, 1)'
        elif 66 < x['AQI'] <= 83:
            listForMap[x['index']]['color'] = 'rgba(114, 177, 5, 1)'
        elif 83 < x['AQI'] <= 100:
            listForMap[x['index']]['color'] = 'rgba(134, 174, 6, 1)'
        elif 100 < x['AQI'] <= 116:
            listForMap[x['index']]['color'] = 'rgba(152, 170, 8, 1)'
        elif 116 < x['AQI'] <= 133:
            listForMap[x['index']]['color'] = 'rgba(167, 165, 9, 1)'
        elif 133 < x['AQI'] <= 150:
            listForMap[x['index']]['color'] = 'rgba(164, 142, 10, 1)'
        elif 150 < x['AQI'] <= 166:
            listForMap[x['index']]['color'] = 'rgba(160, 120, 11, 1)'
        elif 166 < x['AQI'] <= 183:
            listForMap[x['index']]['color'] = 'rgba(157, 100, 12, 1)'
        elif 183 < x['AQI'] <= 200:
            listForMap[x['index']]['color'] = 'rgba(154, 80, 13, 1)'
        elif 200 < x['AQI'] <= 233:
            listForMap[x['index']]['color'] = 'rgba(150, 62, 14, 1)'
        elif 233 < x['AQI'] <= 266:
            listForMap[x['index']]['color'] = 'rgba(147, 44, 15, 1)'
        elif 266 < x['AQI'] <= 300:
            listForMap[x['index']]['color'] = 'rgba(144, 28, 15, 1)'
        elif 300 < x['AQI'] <= 366:
            listForMap[x['index']]['color'] = 'rgba(140, 16, 20, 1)'
        elif 366 < x['AQI'] <= 433:
            listForMap[x['index']]['color'] = 'rgba(137, 17, 36, 1)'
        elif x['AQI'] > 433:
            listForMap[x['index']]['color'] = 'rgba(134, 18, 51, 1)'

    app = DjangoDash('neighborhood_map', external_stylesheets=external_stylesheets)

    app.layout = html.Div(children=[
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
                        layers=listForMap,
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
    current_url = resolve(request.path_info).url_name
    if current_url == 'Report':
        return render(request, 'report.html')
    else:
        return render(request, 'spanish-templates/report.html')
