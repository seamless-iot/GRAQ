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

def pushSignup(name, email, phone, carrier, tier, textAlerts, emailAlerts):
    ACCESS_KEY = ''
    SECRET_KEY = ''


    dynamodb = boto3.resource('dynamodb',
                              aws_access_key_id=ACCESS_KEY,
                              aws_secret_access_key=SECRET_KEY,
                              region_name='us-west-2'
                             )

    if(phone == ''):
        phone = 'none'
        carrier = 'n/a'

    table = dynamodb.Table('email_list')
    response = table.put_item(
                    Item={
                        'name': name,
                        'email':email,
                        'phone':phone,
                        'tier': tier,
                        'carrier': carrier,
                        'textAlerts': textAlerts,
                        'emailAlerts': emailAlerts
                    }
    )
    print("PutItem succeeded:")
    print(json.dumps(response, indent=4, cls=DecimalEncoder))
    return
