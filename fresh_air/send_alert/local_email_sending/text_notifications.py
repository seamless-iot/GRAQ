##TO DO:
##add carrier to sign up page and then uncomment code 
##fix query to check if item exists 

import smtplib
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
import config

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
def get_contacts():
    contacts_phone = []
    contacts_name = []
    contacts_carrier = []
    dynamodb = boto3.resource('dynamodb',
                              aws_access_key_id=config.ACCESS_KEY,
                              aws_secret_access_key=config.SECRET_KEY,
                              region_name='us-west-2'
                             )
    # say what table this is
    table = dynamodb.Table('email_list')

    response = table.scan(FilterExpression=Key('phone'))


    for i in response["Items"]:
        try:
            temp = str(json.dumps(i["phone"], cls=DecimalEncoder))
            temp_phone = temp.replace("\"", "")
            temp = str(json.dumps(i["name"], cls=DecimalEncoder))
            temp_name = temp.replace("\"", "")
            contacts_name.append(temp_name)
            contacts_phone.append(temp_phone)
            #temp = str(json.dumps(i["carrier"], cls=DecimalEncoder))
            #temp = temp.replace("\"", "")
            #contacts_carrier.append(temp)
        except:
            print("there is an issue here and i caught it")

    #return contacts_name, contacts_phone, contacts_carrier
    return contacts_name, contacts_phone

def send_texts(message):
    
    carriers_list = {
    'alltel': '@mms.alltelwireless.com',
    'att':    '@mms.att.net',
    'boost': '@myboostmobile.com',
    'cricket': '@mms.cricketwireless.net',
    'metropcs': '@mymetropcs.com',
    'googlefi': '@msg.fi.google.com',
    'sprint':   '@page.nextel.com',
    'tmobile': '@tmomail.net',
    'us_cellular': '@mms.uscc.net', 
    'verizon':  '@vtext.com',
    'virginmobile': '@vmpix.com'
    }

    #names, numbers, carriers = get_contacts()
    names, numbers = get_contacts()
    
    #temp with my number for testing 
    #to_number = '5862601818{}'.format(carriers['att'])

    # Establish a secure session with gmail's outgoing SMTP server using your gmail account
    #SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(config.MY_ADDRESS, config.PASSWORD)

    #for name, number, carrier in zip(names, numbers, carriers):
    for name, number in zip(names, numbers):
        #for testing delete after 
        name = 'Megan'
        number ='5862601818'
        carrier = 'att'


        number = number + '{}'
        number = number.format(carriers_list[carrier]) 
        text = name + message
        s.sendmail(config.MY_ADDRESS, number, text)

def main():
    send_texts("AIR QUALITY ALERT")
    
if __name__ == '__main__':
    main()
