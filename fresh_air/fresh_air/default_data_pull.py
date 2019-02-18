import boto3
import json
import decimal
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

table = dynamodb.Table('simms_data')

start_date = '2019-01-14T01'
end_date = '2019-01-16T05'


response = table.scan(FilterExpression=Key('time').between(start_date, end_date))
data = response['Items']

while response.get('LastEvaluatedKey'):
    response = table.scan(
        FilterExpression=Key('time').between(start_date, end_date),
        ExclusiveStartKey=response['LastEvaluatedKey'])

    data.extend(response['Items'])


# get specific elements from data
#for i in data:
#    if 'o3' in i:
#        print (i['o3'])

# Use this code to get all dev IDs from current table in timeframe
dev_ids = []
for i in data:
    if i['dev_id'] not in dev_ids:
        dev_ids.append(i['dev_id'])


for i in dev_ids:
    print (i)