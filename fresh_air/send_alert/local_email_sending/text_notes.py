## most simple way i could find to send texts through email will probably change 
##the issue here is knowing the cell carrier 
##we COULD send the text through all carriers and see which send(inefficent but it is an option) 

import smtplib
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
    
    carriers = {
    'att':    '@mms.att.net',
    'tmobile':' @tmomail.net',
    'verizon':  '@vtext.com',
    'sprint':   '@page.nextel.com'
    }

    numbers = get_contacts_phone()
    
    #temp with my number for testing 
    to_number = '5862601818{}'.format(carriers['att'])
    auth = (MY_ADDRESS, PASSWORD)

    # Establish a secure session with gmail's outgoing SMTP server using your gmail account
    #SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(auth[0], auth[1])

    for i in numbers: 
        text = "Megan "
        text += message
        s.sendmail( auth[0], to_number, text)

def main():
    send_texts("AIR QUALITY ALERT")
    
if __name__ == '__main__':
    main()
