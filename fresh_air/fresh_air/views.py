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

def thankyou(request):
    return render(request, 'thankyou.html')

def signup(request):
    print(request.POST['email'])
    print(request.POST['phone'])
    return HttpResponseRedirect(reverse('thankyou'))