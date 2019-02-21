#works to send emails 
#from tutorial mentioned in the other .py file 
#currently just being run on local machine but should have little issue moving to the web app 

#requirements for validate email:
#   pip install validate_email
#   pip install py3dns

import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from validate_email import validate_email
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
def get_contacts():
    contacts_emails = []
    contacts_names = []

    dynamodb = boto3.resource('dynamodb',
                              aws_access_key_id=ACCESS_KEY,
                              aws_secret_access_key=SECRET_KEY,
                              region_name='us-west-2'
                             )
    # say what table this is
    table = dynamodb.Table('email_list')

    response = table.scan()

    for i in response["Items"]:
        temp = str(json.dumps(i["email"], cls=DecimalEncoder))
        temp = temp.replace("\"", "")
        contacts_emails.append(temp)
        temp = str(json.dumps(i["name"], cls=DecimalEncoder))
        temp = temp.replace("\"", "")
        contacts_names.append(temp)

    return contacts_names, contacts_emails

#Reads in the template email body I wrote that can be easily changed again 
def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_email:
        template_email_body = template_email.read()
    return Template(template_email_body)

def send_emails():

    names, emails = get_contacts()

    message_template = read_template('email_template.txt')

    #SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    #loop through alert list to send to 
    for name, email in zip(names, emails):
        msg = MIMEMultipart()       

        # add name to the email template
        message = message_template.substitute(PERSON_NAME=name.title())
        
        #testing
        print(message)

        # setup the parameters of the message
        msg['From']=MY_ADDRESS
        msg['Subject']="This is a TEST"

        #will also need this checking function in the form where they sign up for email alerts 
        #there is an issue with this check 
        #if(validate_email(email,verify=True)):
        msg['To']=email
        #else: 
        #    continue
        
        msg.attach(MIMEText(message, 'plain'))

        #commented for testing 
        #s.send_message(msg)
        
        del msg
        
    # Terminate the SMTP session and close the connection
    s.quit()

def main():
    send_emails()
    
if __name__ == '__main__':
    main()
