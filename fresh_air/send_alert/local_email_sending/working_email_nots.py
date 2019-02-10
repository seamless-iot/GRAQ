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

MY_ADDRESS = 'teambreatheoffreshair@gmail.com'
PASSWORD = 'CIS467BFA'

#parses contact list stored in a txt file 
#if we store in a DB this is an easy change 
def get_contacts(filename):
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as alert_list:
        for contact in alert_list:
            names.append(contact.split()[0])
            emails.append(contact.split()[1])
    return names, emails

#Reads in the template email body I wrote that can be easily changed again 
def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_email:
        template_email_body = template_email.read()
    return Template(template_email_body)

#function to add to the email list for the txt file 
def add_to_list(name, email_address):
    
    #open file and APPEND to it (do not overwrite)
    f= open("alertlist.txt","a+")

    #write contact info 
    f.write("" + (name) + " " + (email_address) + "\n")

    #close the file 
    f.close()

def main():

    #testing the add function 
    info_name = input("enter your name: ")
    info_email = input("enter your email: ")
    add_to_list(info_name, info_email)

    #reading docs in 
    names, emails = get_contacts('alertlist.txt')
    message_template = read_template('emailtemplate.txt')

    #SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    #loop through alert list to send to 
    for name, email in zip(names, emails):
        msg = MIMEMultipart()       

        # add name to the email template
        message = message_template.substitute(PERSON_NAME=name.title())
        
        # for error checking
        print(message)

        # setup the parameters of the message
        msg['From']=MY_ADDRESS
        msg['Subject']="This is TEST"

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
    
if __name__ == '__main__':
    main()