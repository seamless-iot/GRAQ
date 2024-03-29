from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from data_push.data_push import pushSignup
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from data_visualize import models as dataPull
from django_plotly_dash import DjangoDash
from django.urls import resolve




def home_page(request):
    current_url = resolve(request.path_info).url_name
    if current_url == 'Home':
        return render(request, 'home.html')
    else:
        return render(request, 'spanish-templates/home.html')


def about(request):
    mapbox_access_token = 'pk.eyJ1IjoicmFtaWphdmkiLCJhIjoiY2pyemJ5bm56MTdhMzRhbXRscjA0djd0dSJ9.TDjuO5EJnwFcz7hZCEXXwA'
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = DjangoDash('sensormap', external_stylesheets=external_stylesheets)

    # Initiating and running dataPull script
    # This script is used to pull data from the DynamoDB
    graphData = dataPull.graphDataGetter()
    graphData.run()

    # getLocationData() returns the location, device ID, device type
    # and AQI for all sensors on the DB
    locationData = graphData.getLocationData()

    # For debugging purposes
    # print(locationData)

    latC=[]
    lonC=[]
    textC=[]
    buff=''

    # This nested for loop gets the data from getLocationData()
    # and stores the relevant variables in the three lists we initialized
    # above. These lists store the latitude and longitude of each sensor,
    # as well as the text that will be displayed on their tags.
    for i in locationData:
        index = 0
        for a in i['device_gps_location']:
            if(a == ','):
                latC.append(buff)
                buff = ''
            elif(index == len(i['device_gps_location'])-1):
                lonC.append(buff)
                buff = ''
            elif(a != ' '):
                buff += a
            index += 1
        textC.append('Device ID: ' + i['device_id'] + '. Device Type: ' + i['device_type']
                     + '. Current AQI measured:' + str(i['AQI']))

    app.layout = html.Div(children=[
        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    go.Scattermapbox(
                        lat=latC,
                        lon=lonC,
                        mode='markers',
                        marker=dict(
                            size=9
                        ),
                        text=textC
                    )
                ],
                'layout': go.Layout(
                    autosize=True,
                    hovermode='closest',
                    mapbox=dict(
                        accesstoken=mapbox_access_token,
                        bearing=0,
                        center=dict(
                            lat=42.97,
                            lon=-85.68
                        ),
                        pitch=0,
                        zoom=10
                    ),
                )
            }
        )
    ])
    current_url = resolve(request.path_info).url_name

    if current_url == 'About':
        return render(request, 'about.html')
    else:
        return render(request, 'spanish-templates/about.html')

def analysis(request):
    return render(request, 'analysis.html')

def airqualityguide(request):
    current_url = resolve(request.path_info).url_name
    if current_url == 'AQG':
        return render(request, 'air-quality-guide.html')
    else:
        return render(request, 'spanish-templates/air-quality-guide.html')

def contact(request):
    current_url = resolve(request.path_info).url_name
    if current_url == 'Contact':
        return render(request, 'contact.html')
    else:
        return render(request, 'spanish-templates/contact.html')

def data(request):
    current_url = resolve(request.path_info).url_name
    if current_url == 'Data':
        return render(request, 'data.html')
    else:
        return render(request, 'spanish-templates/data.html')


def signup(request):
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    carrier = request.POST['carrier']

    textAlerts = False
    if request.POST.get('phone_optin', False):
        textAlerts = True

    emailAlerts = False
    if request.POST.get('email_optin', False):
        emailAlerts = True

    tier = 1
    if request.POST.get('tier_optin', False):
        tier = 2

    #print("HEYYYYYYYYYYYYYYYYYYY")
    #print(request.POST.get('tier-optin'))
    #if (request.POST.get('tier-optin') == True):
      #  tier = 2

    # we get "pushSignup" from the "data_push" app i.e. fresh_air/data_push/data_push.py
    pushSignup(name, email, phone, carrier, tier, textAlerts, emailAlerts)
    #print(request.POST['email'])
    #print(request.POST['phone'])
    return render(request, 'thankyou.html')
