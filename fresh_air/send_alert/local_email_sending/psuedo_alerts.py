#for template email 
from string import Template

# import the smtplib module. It should be included in Python by default
import smtplib

# email stuff 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#check to make sure email is valid  
from validate_email import validate_email

#********************************************************************************************
#starting layout and code for sending email notifications for air quality warnings 
#WARNING: totally psuedo code does not run just testing layout and ideas and stuff 
#have a working file that just sends emails does not include psuedo code for the AQI
#tutorials followed:
# 	https://medium.freecodecamp.org/send-emails-using-code-4fcea9df63f
#********************************************************************************************

#our email info TBD idk if anyone has a prefered platform/way to execute this 
#if not i will likely use gmail which i have in the working file 
MY_ADDRESS = 'email'
PASSWORD = 'password'

#best solution to me for sending the current levels is a dict that has the pollutant as the key and the current level as the value 
#so after we parse the data from the database we would store it as the following 
#will change from sensor to sensor 
#example:
#current_levels = {
#	ozone : 0.03,
#	carbon_dioxide : 0.5,
#	particulate_matter_two_five : 0.001
#}

#Several options for sending alerts: 
#set constants for each max level of pollutants we monitor(more fitting for push notifications or texts)
MAX_OZONE = 0.1 #(in ppm)

#or send alert level (which i think is more fitting for email) 
#requires a level dict for each pollutant 
ozone_alert_level = { #also in ppm
	0.2 : "no more than 2 hours exposure", 
	0.1 : "8 hours per day exposure doing light work",
	0.08 : "8 hours per day exposure doing moderate work",
	0.05 : "8 hours per day exposure doing heavy work"
}

#or we can send alert for overall air quality marks rather than checking for a specfic pollutants level(also a good option for text/push notifications)
#we could do all of the above and let users select which type of notifications they would like to recieve 
#overall air quality might be difficult however because we might be missing stats on the top five pollutants used to calculate it 
#this requires a standard level dict (might be complicated to calculate bc of different units of measure & average time & calculation methods see: https://www.epa.vic.gov.au/your-environment/air/air-pollution/air-quality-index/calculating-a-station-air-quality-index)
#found a package that may be able to help with calculations https://media.readthedocs.org/pdf/python-aqi/latest/python-aqi.pdf  
standard_level = {
	'ozone' : 100, #ppb
	'carbon_monoxide' : 9, #ppm
	'nitrogen_dioxide' : 120, #ppb 
	'particulate_matter_twofive' : 25, #µg/m3
	'sulfur_dioxide' : 200 #ppb 
}

#once we establish air qualtiy standards we want to use 
#this can be called at whatever interval we find fit (dont want to send an alert every time we find a high level bc of how often we are getting data) 
#may also want to include a timing portions like if ozone has been high for five or more checks of the sensor then send the emails 
def polutant_quality(current_levels):
	alert_list = {}

	#levels option 
	#because all sensors don't monitor the same pollutants we have to check if each pollutant is in the current level dict sent 
	if "ozone" in current_levels:
		if current_levels[ozone] >= 0.2:
			alert_list.update({"ozone", ozone_alert_level[0.2]})

		elif current_levels[ozone] >= 0.1 and current_levels[ozone] < 0.2:
			alert_list.update({"ozone", ozone_alert_level[0.1]})

		elif current_levels[ozone] >= 0.08 and current_levels[ozone] < 0.1:
			alert_list.update({"ozone", ozone_alert_level[0.08]})

		elif current_levels[ozone] >= 0.05 and current_levels[ozone] < 0.08:
			alert_list.update({"ozone", ozone_alert_level[0.05]})

	#maximum option 
	#either would repeat for all contaminents that we are monitoring 
	if "ozone" in current_levels:
		if current_levels[ozone] >= MAX_OZONE:
			alert_list.update({"ozone", current_levels[ozone]})

	#overall option 
	current_AQI, index = air_quality_calc(current_levels)
	if current_AQI > 3
		alert_list.update({"AQI", index})

	#if there is one or more pollutant with a high level send the alert out 
	if len(alert_list) >= 1: 
		email_alert(alert_list)
		
		#not sure if this is something we would like to implement but I have resources on how to implement both(eventually): 
		#	text_alert(alert_list)
		#	push_notifications_alert(alert_list)


#calculates the AQI to the most accurate level we can 
def air_quality_calc(current_levels):
	current_AQI = 0

	#decide calculation method and standards

	#example levels I saw online will likely be changed 
	if index <= 33 
		current_AQI = 1 #very good 
	elif  index >= 34 and index < 67:
		current_AQI = 2 #good 
	elif  index >= 67 and index < 100:
		current_AQI = 3 #fair 
	elif  index >= 100 and index < 150:
		current_AQI = 4 #poor
	elif  index >= 150:
		current_AQI = 5 #very poor 

	return current_AQI, index



#handles the logic to send out email alerts 
def email_alert(alert_list):
	 
	# set up the SMTP server
	s = smtplib.SMTP(host='your_host_address_here', port=your_port_here)

	#if we use outlook for example we would do: 
	#s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)

	s.starttls()
	s.login(MY_ADDRESS, PASSWORD)

	#gets the names and emails of people that we need to alert 
	names, emails = get_contacts('alertlist.txt')  

	#gets our email template 
	message_template = read_template('emailtemplate.txt')

	#loops through the email list 
	for name, email in zip(names, emails):
        
        # create a message
        msg = MIMEMultipart()       

	    # add in the actual person name to the message template and alert list(needs formating)
        message = message_template.substitute(PERSON_NAME=name.title())
        #message = message_template.substitute(CURRENT_ALERTS=alert_list) #not correct syntax or formating 

        # Prints out the message body for error checking 
        print(message)

        # setup the parameters of the message
        msg['From']=MY_ADDRESS
        msg['Subject']="AIR QUALITY ALERT"
        
        #will also need this checking function in the form where they sign up for email alerts DOES NOT WORK RN 
        if(validate_email(email,verify=True)): 
        	 msg['To']=email

       	#email checks we can use + explanatins: 
       		#Check email string is valid format:
       		#is_valid = validate_email(email)
       		#Check if the host has SMTP Server:
			#is_valid = validate_email(email,check_mx=True)
			#Check if the host has SMTP Server and the email really exists:
			#is_valid = validate_email(email,verify=True)

       	else:
       		#have a cleaner function for if the email is no longer in use 
       		#breaks out of this name in the loop and continues to the next 
       		continue 

        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        
        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg
	


# Function to read the contacts from a given contact file and return a
# list of names and email addresses
def get_contacts(filename):
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as alert_list:
        for a_contact in alert_list:
            names.append(a_contact.split()[0])
            names.append(a_contact.split()[1])
            emails.append(a_contact.split()[2])
    return names, emails

#reads the template email we created 
def read_template_email(filename):
    with open(filename, 'r', encoding='utf-8') as template_email:
        template_email_content = template_email.read()
    return Template(template_email_content)

#function to add to the email list for the txt file 
def add_to_list(name, email_address):
    
    #open file and APPEND to it (do not overwrite)
    f= open("alertlist.txt","a+")

    #write contact info 
    f.write("" + (name) + " " + (email_address) + "\n")

    #close the file 
    f.close()
