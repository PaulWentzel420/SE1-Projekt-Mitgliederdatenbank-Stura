from django.urls import path
from . import views

app_name = 'kandidaturen'  # here for namespacing of urls.

urlpatterns = [
     path("", views.main_screen, name="homepage"),
     path("erstellen", views.kandidaturErstellenView, name="erstellenView"),
     path("erstellen/speichern", views.erstellen, name="erstellen"),
     path("<int:kandidatur_id>/bearbeiten", views.kandidaturBearbeitenView, name="bearbeitenView"),
     path("<int:kandidatur_id>/bearbeiten/speichern", views.speichern, name="speichern"),

     path('ajax/laden', views.kandidatur_laden, name='kandidatur_laden'),
     path("ajax/kandidaturen-loeschen", views.kandidaturen_loeschen, name="kandidaturen_loeschen"),
     path('ajax/bereiche-laden', views.bereiche_laden, name='bereiche_laden'),
     path('ajax/funktionen-laden', views.funktionen_laden, name='aemter_laden'),
     path('ajax/funktionen-html-laden', views.funktionen_html_laden, name='aemter_html_laden'),
     path('ajax/funktion-loeschen', views.funktion_loeschen, name='amt_loeschen'),
     path('ajax/email-html-laden', views.email_html_laden, name='email_html_laden'),
     path('ajax/email-loeschen', views.email_loeschen, name='email_loeschen'),
     path('ajax/suchen', views.suchen, name="suchen"),
     path('ajax/kandidatur-aufnehmen', views.kandidatur_aufnehmen, name="kandidatur_aufnehmen")
]
