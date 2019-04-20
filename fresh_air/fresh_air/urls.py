"""fresh_air URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_page, name="Home"),
    path('about/', views.about, name="About"),
    path('admin/', admin.site.urls),
    path('analysis/', views.analysis, name="Analysis"),
    path('report/', include('data_visualize.urls')),
    path('guide/', views.airqualityguide, name="AQG"),
    path('contact/', views.contact, name="Contact"),
    path('data/', views.data, name="Data"),
    # this is where our signup form points to. It activates the "signup" function in views.py
    path('thankyou/', views.signup, name='signup'),

    path('es/', views.home_page, name="EsHome"),
    path('es/about/', views.about, name="EsAbout"),
    path('es/guide/', views.airqualityguide, name="EsAQG"),
    path('es/report/', include('data_visualize.urls')),
    path('es/contact/', views.contact, name="EsContact"),
    path('es/data/', views.data, name="EsData"),

    path('django_plotly_dash/', include('django_plotly_dash.urls')),

]
