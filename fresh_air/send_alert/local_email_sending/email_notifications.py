
import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from validate_email import validate_email
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
    contacts_emails = []
    contacts_names = []

    dynamodb = boto3.resource('dynamodb',
                              aws_access_key_id=config.ACCESS_KEY,
                              aws_secret_access_key=config.SECRET_KEY,
                              region_name='us-west-2'
                             )
   
    # say what table this is
    table = dynamodb.Table('email_list')

    response = table.scan()

    for i in response["Items"]:
        temp = str(json.dumps(i["emailAlerts"], cls=DecimalEncoder))
        if temp == 'true':
            temp = str(json.dumps(i["email"], cls=DecimalEncoder))
            temp_email = temp.replace("\"", "")
            temp = str(json.dumps(i["name"], cls=DecimalEncoder))
            temp_name = temp.replace("\"", "")
            contacts_emails.append(temp_email)
            contacts_names.append(temp_name)

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
    s.login(config.MY_ADDRESS, config.PASSWORD)

    #loop through alert list to send to 
    for name, email in zip(names, emails):
        msg = MIMEMultipart()       

        # add name to the email template
        message = message_template.substitute(PERSON_NAME=name.title())
 
        # setup the parameters of the message
        msg['From']=config.MY_ADDRESS
        msg['Subject']="Air Quality Alert"
        msg['To']=email
        
        msg.attach(MIMEText(message, 'plain'))

        s.send_message(msg)
        
        del msg
        
    # Terminate the SMTP session and close the connection
    s.quit()

def main():
    send_emails()
    
if __name__ == '__main__':
    main()