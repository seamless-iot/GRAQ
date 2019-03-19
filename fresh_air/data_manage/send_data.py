import boto3
import json
import decimal
import datetime
import random
from boto3.dynamodb.conditions import Key, Attr

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


ACCESS_KEY = 'AKIAIJ55NBMNXJBAX2MA'
SECRET_KEY = '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'


dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id=ACCESS_KEY,
                          aws_secret_access_key=SECRET_KEY,
                          region_name='us-west-2'
                         )

# Here are the standard values for each of
# the pollutants that are measured by our
# sensors
# gotten from
# https://www.epa.vic.gov.au/your-environment/air/air-pollution/air-quality-index/calculating-a-station-air-quality-index
o3standard = 100 # ppb
pm10standard = 50 # ug/m3
pm25standard = 25 # ug/m3
no2standard = 120 # ppb
so2standard = 200 # ppb

# This section of code gets the locations of all the sensors being used
table = dynamodb.Table('sensor_locations')
response = table.scan()
locationData = response['Items']
# This is to make sure data is pulled for all sensors, something can be filled in
# if a sensor doesn't have any data
for i in locationData:
    i["AQI"] = 0

# This gets the hour to use for the map
currentDT = datetime.datetime.now()
strHour = currentDT.strftime("%H")
intHour = int(strHour)
intHour += 1
if intHour < 10:
    strHour = "0" + str(intHour)
else:
    strHour = str(intHour)
sendTime = currentDT.strftime("%Y-%m-%d") + "/" + strHour + ":00:00"

# Start with ost_data
# Get data for the last hours
# Ex: from 9:00:01 to 10:00:00
table = dynamodb.Table('ost_data')
# For testing purposes, using fake date
#end_time = currentDT.strftime("%Y-%m-%d") + 'T' + strHour + ':00:00'
end_time = '2018-09-26T14:00:00'

intHour -= 1
if intHour <10:
    strHour = "0" + str(intHour)
else:
    strHour = str(intHour)
# For testing purposes, using fake date
#start_time = currentDT.strftime("%Y-%m-%d") + 'T' + strHour + ':00:01'
start_time = '2018-09-26T13:00:01'

# Pull all ost_data from table for time interval
response = table.scan(FilterExpression=Key('time').between(start_time, end_time))
ostData = response['Items']

# Note for ost_data
# Has o3 (o3), pm10 (pm10average), and pm2.5 (pm25average)
for i in locationData:
    deviceData = []
    # Get all of the data for this device
    for j in ostData:
        if j['dev_id'] == i['device_id']:
            deviceData.append(j)
    # If there is data for this sensor,
    # calculate the average AQI for the
    # time period
    aqiValues = []
    if len(deviceData) != 0:
        # Get AQI for each time in table
        for k in range(len(deviceData)):
            ozone = (int(deviceData[k]['o3']) / o3standard) * 100
            pm10 = (int(deviceData[k]['pm10Average']) / pm10standard) * 100
            pm25 = (int(deviceData[k]['pm25Average']) / pm25standard) * 100
            aqi = max(ozone, pm10, pm25)
            aqiValues.append(aqi)
        # Get the average AQI for this sensor in this time
        aqi = sum(aqiValues) / len(aqiValues)
        i["AQI"] = int(aqi)

# Pull all simms_data from table for time interval
table = dynamodb.Table('simms_data')
# For testing purposes, using fake date and time
start_time = '2019-01-11T22:00:01'
end_time = '2019-01-11T23:00:00'
response = table.scan(FilterExpression=Key('time').between(start_time, end_time))
simmsData = response['Items']

# Note for simms_data
# Has no2 (no2), o3 (o3), pm2.5 (pm25), so2 (so2)
for i in locationData:
    deviceData = []
    # Get all of the data for this device
    for j in simmsData:
        if j['dev_id'] == i['device_id']:
            deviceData.append(j)
    # If there is data for this sensor,
    # calculate the average AQI for the
    # time period
    aqiValues = []
    if len(deviceData) != 0:
        # Get AQI for each time in table
        # Was originally doing a different calculation for this and may
        # go back to it in the future, need to do a bit more research
        # as to what the best option is
        for k in range(len(deviceData)):
            no2 = (int(deviceData[k]["no2"]) / no2standard) * 100
            ozone = (int(deviceData[k]['o3']) / o3standard) * 100
            pm25 = (int(deviceData[k]['pm25']) / pm25standard) * 100
            so2 = (int(deviceData[k]['so2']) / so2standard) * 100
            aqi = max(no2, ozone, pm25, so2)
            aqiValues.append(aqi)
        # Get the average AQI for this sensor in this time
        aqi = sum(aqiValues) / len(aqiValues)
        if i["AQI"] != 0:
            i["AQI"] = max(aqi, i["AQI"])
        else:
            i["AQI"] = aqi

# For testing purposes, this code can
# fill the locations with no AQI data
# with random values
for i in locationData:
    if i["AQI"] == 0:
        i["AQI"] = 25 + random.randint(1, 75)

strIDs = "["
strAQIs = "["
for i in locationData:
    strIDs = strIDs + i.get("device_id") + ","
    strAQIs = strAQIs + str(i["AQI"]) + ","
strIDs = strIDs[:-1] + "]"
strAQIs = strAQIs[:-1] + "]"

table = dynamodb.Table('mapdata')
# "put_item" is a dynamodb function we are calling
response = table.put_item(
    Item={
        'time':sendTime,
        'sensorAQI':strAQIs,
        'sensorIDs':strIDs,
    }
)