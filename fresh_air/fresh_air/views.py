from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

def home_page(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

# this is the function called by the form
# we don't really need to print the post variables, but
# we can pass them to another function that stores them
# in the aws database
def signup(request):
    print(request.POST['email'])
    print(request.POST['phone'])
    return render(request, 'thankyou.html')
