from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

def home_page(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')
