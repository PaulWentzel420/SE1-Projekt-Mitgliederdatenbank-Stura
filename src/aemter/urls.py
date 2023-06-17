from django.urls import path
from . import views
#from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static


app_name = 'aemter'  # here for namespacing of urls.

urlpatterns = [
    path("", views.main_screen, name="homepage"), 
] 

