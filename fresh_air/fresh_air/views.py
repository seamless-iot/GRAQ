from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

#from fresh_air.fresh_air.data_push import pushSignup
from data_push.data_push import pushSignup




def home_page(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

# this is the function called by the form
# we don't really need to print the post variables, but
# we can pass them to another function that stores them
# in the aws database


def signup(request):
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
    pushSignup(email, phone, tier)
    #print(request.POST['email'])
    #print(request.POST['phone'])
    return render(request, 'thankyou.html')
