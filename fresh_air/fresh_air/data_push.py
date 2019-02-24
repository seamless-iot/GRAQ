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

# this is our function that pushes to dynamoDB.
# currently takes 4 parameters, this may change
def pushSignup(name, email, phone, tier):
    ACCESS_KEY = 'AKIAIJ55NBMNXJBAX2MA'
    SECRET_KEY = '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'


    dynamodb = boto3.resource('dynamodb',
                              aws_access_key_id=ACCESS_KEY,
                              aws_secret_access_key=SECRET_KEY,
                              region_name='us-west-2'
                             )
    # say what table this is
    table = dynamodb.Table('email_list')
    # "put_item" is a dynamodb function we are calling
    response = table.put_item(
                    Item={
                        # id is hard coded. I think we can go without this in general.
                        # currently because the id is the same, it will overwrite the id=45 row in the db
                        # because the id is the partition key.
                        # change the id to something else to add a new entry. In the future,
                        # we can use email as the partition key
                        'id': 45,
                        'name': name,
                        'email':email,
                        'phone':phone,
                        'tier': tier
                    }
    )
    print("PutItem succeeded:")
    print(json.dumps(response, indent=4, cls=DecimalEncoder))
    return
