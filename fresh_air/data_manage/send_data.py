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

table = dynamodb.Table('sensor_locations')
response = table.scan()
locationData = response['Items']

currentDT = datetime.datetime.now()
strHour = currentDT.strftime("%H")
intHour = int(strHour)
intHour += 1
if intHour < 10:
    strHour = "0" + str(intHour)
else:
    strHour = str(intHour)
sendTime = currentDT.strftime("%Y-%m-%d") + "/" + strHour + ":00:00"

strIDs = "["
strAQIs = "["
for i in locationData:
    #print(i.get("device_gps_location"))
    #print(i.get("device_id"))
    #print(i.get("device_type"))
    strIDs = strIDs + i.get("device_id") + ","
    strAQIs = strAQIs + str((random.randint(1,75) + 50)) + ","
strIDs = strIDs[:-1] + "]"
strAQIs = strAQIs[:-1] + "]"

print(strIDs)
print(strAQIs)

#table = dynamodb.Table('mapdata')
# "put_item" is a dynamodb function we are calling
#response = table.put_item(
    #Item={
    #    'time':sendTime,
   #     'sensorAQI':strAQIs,
  #      'sensorIDs':strIDs,
 #   }
#)