from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

#from fresh_air.fresh_air.data_push import pushSignup
from data_push.data_push import pushSignup

#import data_visualize.sensorMap

from data_visualize.models import *


def home_page(request):
    return render(request, 'home.html')

def about(request):
    map = mapClass()
    context1 = {'sensorMap': map }

    return render(request, 'about.html', context=context1) #context=context)

def analysis(request):
    return render(request, 'analysis.html')

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
