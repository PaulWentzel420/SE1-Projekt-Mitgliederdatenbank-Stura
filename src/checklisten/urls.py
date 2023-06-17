from django.urls import path
from . import views
#from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static


app_name = 'checklisten'  # here for namespacing of urls.

urlpatterns = [
    path("", views.main_screen, name="main_screen"),
    path("abhaken", views.abhaken, name="abhaken"),
    path("loeschen", views.loeschen, name="loeschen"),
    path("erstellen", views.erstellen, name="erstellen"),
    path("get_funktionen", views.get_funktionen, name="get_funktionen")
]