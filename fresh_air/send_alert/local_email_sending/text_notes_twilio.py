##alternative texting script using twilio, will decide best course of action in group meeting 
## pip install twilio

from twilio.rest import Client 
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

##TO DO: move this info to a credentials file 
MY_ADDRESS = 'teambreatheoffreshair@gmail.com'
PASSWORD = 'CIS467BFA'
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
        contacts_phone.append(temp)

    return contacts_phone

def send_texts(message):

    numbers = get_contacts_phone()

    account_sid = 'ACbf87eb8c0bd704d956525a4c9b7b9cc0'
    auth_token = 'd7c8ba3f9e209414d57daa64318d0a12'
    client = Client(account_sid, auth_token)

    for number in numbers:

        #will change to my hard coded number to number in real code 
        message = client.messages.create(
                                  from_='+15862216842',
                                  body='test test test',
                                  to='+15862601818'
                              )

        print(message)



def main():
    send_texts("AIR QUALITY ALERT")
    
if __name__ == '__main__':
    main()
