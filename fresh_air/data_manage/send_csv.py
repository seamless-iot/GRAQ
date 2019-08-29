import boto3
import json
import decimal
import datetime
import csv
from boto3.dynamodb.conditions import Key, Attr

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def accessDatabase(dbName):
    ACCESS_KEY = ''
    SECRET_KEY = ''


    dynamodb = boto3.resource('dynamodb',
                              aws_access_key_id=ACCESS_KEY,
                              aws_secret_access_key=SECRET_KEY,
                              region_name='us-west-2'
                             )

    table = dynamodb.Table(dbName)
    response = table.scan()
    returnData = response['Items']
    return returnData

def ostFile(outputPath):
    ostData = accessDatabase('ost_data')
    currentDT = datetime.datetime.now()
    filename = "ost_" + currentDT.strftime("%Y-%m-%dT%H-%M-%S") + ".csv"
    with open(outputPath + filename, 'w+', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        colValues = ostData[0].keys()
        writeRow = ['dev_id', 'time']
        for i in colValues:
            if i != 'dev_id' and i != 'time':
                writeRow.append(i)
        filewriter.writerow(writeRow)
        for i in ostData:
            writeRow = []
            writeRow.append(i['dev_id'])
            writeRow.append(i['time'])
            for key in i:
                if key != 'dev_id' and key != 'time':
                    writeRow.append(i[key])
            filewriter.writerow(writeRow)

def simmsFile(outputPath):
    simmsData = accessDatabase('simms_data')
    currentDT = datetime.datetime.now()
    filename = "simms_" + currentDT.strftime("%Y-%m-%dT%H-%M-%S") + ".csv"
    with open(outputPath + filename, 'w+', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        colValues = simmsData[0].keys()
        writeRow = ['dev_id', 'time']
        for i in colValues:
            if i != 'dev_id' and i != 'time':
                writeRow.append(i)
        filewriter.writerow(writeRow)
        for i in simmsData:
            writeRow = []
            writeRow.append(i['dev_id'])
            writeRow.append(i['time'])
            for key in i:
                if key != 'dev_id' and key != 'time':
                    writeRow.append(i[key])
            filewriter.writerow(writeRow)

ostFile('C:/Users/etern/Documents/GitHub/freshair/fresh_air/data_manage/')
simmsFile('C:/Users/etern/Documents/GitHub/freshair/fresh_air/data_manage/')
