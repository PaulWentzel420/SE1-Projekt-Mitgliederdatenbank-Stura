from django.urls import path
from . import views

app_name = 'mitglieder'  # here for namespacing of urls.

urlpatterns = [
    path("", views.main_screen, name="homepage"),
    path("erstellen", views.mitgliedErstellenView, name="erstellenView"),
    path("erstellen/speichern", views.erstellen, name="erstellen"),
    path("<int:mitglied_id>/bearbeiten", views.mitgliedBearbeitenView, name="bearbeitenView"),
    path("<int:mitglied_id>/bearbeiten/speichern", views.speichern, name="speichern"),

    path('ajax/laden', views.mitglied_laden, name='mitglied_laden'),
    path("ajax/mitglieder-loeschen", views.mitglieder_loeschen, name="mitglieder_loeschen"),
    path('ajax/bereiche-laden', views.bereiche_laden, name='bereiche_laden'),
    path('ajax/funktionen-laden', views.funktionen_laden, name='aemter_laden'),
    path('ajax/funktionen-html-laden', views.funktionen_html_laden, name='aemter_html_laden'),
    path('ajax/<int:mitglied_id>/funktionen-max-member-ueberpruefen', views.funktionen_max_member_ueberpruefen, name='funktionen-max-member-ueberpruefen'),
    path('ajax/funktion-loeschen', views.funktion_loeschen, name='amt_loeschen'),
    path('ajax/email-html-laden', views.email_html_laden, name='email_html_laden'),
    path('ajax/email-loeschen', views.email_loeschen, name='email_loeschen'),
    path('ajax/suchen', views.suchen, name="suchen"),
]
