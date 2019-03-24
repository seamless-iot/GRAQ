from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
import boto3
import json
import decimal
import datetime
from boto3.dynamodb.conditions import Key, Attr

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
import plotly.graph_objs as go

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


class graphDataGetter(object):
    def __init__(self):
        self.ACCESS_KEY = 'AKIAIJ55NBMNXJBAX2MA'
        self.SECRET_KEY = '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'
        self.dynamodb = boto3.resource('dynamodb',
                                aws_access_key_id=self.ACCESS_KEY,
                                aws_secret_access_key=self.SECRET_KEY,
                                region_name='us-west-2'
                                )
    def run(self):
        #gets the sensor IDs and locations from the table
        table = self.dynamodb.Table('sensor_locations')
        response = table.scan()
        self.locationData = response['Items']

        #this is to get the value from mapdata that is of the appropritate timestamp.
        #this is just a placeholder for a better way to
        #get this information in the future
        currentDT = datetime.datetime.now()
        strHour = currentDT.strftime("%H")
        begHour = strHour
        intHour = int(strHour)
        intHour += 1
        if intHour < 10:
            endHour = "0" + str(intHour)
        else:
            endHour = str(intHour)
        #searchBegTime = currentDT.strftime("%Y-%m-%d") + "/" + begHour + ":00:00"
        #searchEndTime = currentDT.strftime("%Y-%m-%d") + "/" + endHour + ":00:00"

        #set values to pull from the table for now
        searchBegTime = "2019-02-23/10:00:00"
        searchEndTime = "2019-02-23/11:00:00"

        #this goes with the placeholder code
        #it tries to pull the most recent value in the table
        table = self.dynamodb.Table('mapdata')
        response = table.scan(FilterExpression=Key('time').eq(searchEndTime))
        self.mapData = response["Items"]
        if len(self.mapData) == 0:
            response = table.scan(FilterExpression=Key('time').eq(searchBegTime))
            self.mapData = response["Items"]

        #this gets the sensor IDs and the AQIs for
        #those sensors into their own dictionary so that
        #the IDs can be compared to the ones
        #in the sensor table and the AQI values
        #can be added to the other dictionary
        #print(mapData)
        for i in self.mapData:
            sID = i["sensorIDs"]
            sID = sID[1:-1] #removes brackets
            sensorIDs = sID.split(",")
            sAQI = i["sensorAQI"]
            sAQI = sAQI[1:-1] #removes brackets
            sensorAQIs = sAQI.split(",")
            mapDict = dict(zip(sensorIDs, sensorAQIs))

        #this adds the AQI for each sensor to its
        #dictionary in locationData

        #print(locationData)
        for id, aqi in mapDict.items():
            for i in self.locationData:
                if i.get("device_id") == id:
                    i["AQI"] = aqi

        #print(locationData)

        #locationData has everything needed for the map -
        #device_gps_location in coordinates
        #device_id and device_type if you want them for hover information
        #AQI for that sensor

    def getLocationData(self):
        return self.locationData

    def getMapData(self):
        return self.mapData

