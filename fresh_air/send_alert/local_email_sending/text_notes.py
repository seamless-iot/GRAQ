import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

##TO DO: move this info to a credentials file 
ACCESS_KEY = 'AKIAIJ55NBMNXJBAX2MA'
SECRET_KEY = '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'

# Helper class to convert a DynamoDB item to JSON.
#from amazon docs
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

# pulls contact info from the db 
def get_contacts_phone():
    contacts_names = []
    contacts_phone = []
    dynamodb = boto3.resource('dynamodb',
                              aws_access_key_id=ACCESS_KEY,
                              aws_secret_access_key=SECRET_KEY,
                              region_name='us-west-2'
                             )
    # say what table this is
    table = dynamodb.Table('email_list')

    response = table.scan()

    for i in response["Items"]:
        temp = str(json.dumps(i["phone"], cls=DecimalEncoder))
        temp = temp.replace("\"", "")
        contacts.append(temp)
        temp = str(json.dumps(i["name"], cls=DecimalEncoder))
        temp = temp.replace("\"", "")
        contacts_names.append(temp)

    return contacts_names, contacts_phone

def send_texts():
	
	names, numbers = get_contacts_phone()