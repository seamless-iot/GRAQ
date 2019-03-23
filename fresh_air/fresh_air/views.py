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



def home_page(request):
    return render(request, 'home.html')

def about(request):


    mapbox_access_token = 'pk.eyJ1IjoicmFtaWphdmkiLCJhIjoiY2pyemJ5bm56MTdhMzRhbXRscjA0djd0dSJ9.TDjuO5EJnwFcz7hZCEXXwA'
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = DjangoDash('sensormap', external_stylesheets=external_stylesheets)

    graphData = dataPull.graphDataGetter()
    graphData.run()
    locationData = graphData.getLocationData()
    latC = []
    lonC = []
    textC = []

    buff = ''
    for i in locationData:
        index = 0
        for a in i['device_gps_location']:
            if (a == ','):
                latC.append(buff)
                buff = ''
            elif (index == len(i['device_gps_location']) - 1):
                lonC.append(buff)
                buff = ''
            elif (a != ' '):
                buff += a
            index += 1

        textC.append('Device ID: ' + i['device_id'] + '. Device Type: ' + i[
            'device_type'] + '. Current AQI measured: ')  # + i['aqi'] )

    app.layout = html.Div(children=[
        html.H1(children='Sensor Location Sample Test'),
        html.Div(children='This is a test for a map that shows were air quality sensors are '
                          'located. Right now this is made out of sample data.'),
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

    return render(request, 'about.html')

def analysis(request):
    return render(request, 'analysis.html')

def airqualityguide(request):
    return render(request, 'air-quality-guide.html')

def contact(request):
    return render(request, 'contact.html')

def data(request):
    return render(request, 'data.html')

# this is the function called by the form
# we don't really need to print the post variables, but
# we can pass them to another function that stores them
# in the aws database
def signup(request):
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    tier = 1
    if request.POST.get('tier_optin', False):
        tier = 2

    #print("HEYYYYYYYYYYYYYYYYYYY")
    #print(request.POST.get('tier-optin'))
    #if (request.POST.get('tier-optin') == True):
      #  tier = 2

    # we get "pushSignup" from the "data_push" app i.e. fresh_air/data_push/data_push.py
    pushSignup(name, email, phone, tier)
    #print(request.POST['email'])
    #print(request.POST['phone'])
    return render(request, 'thankyou.html')
