from django.urls import path
from . import views

app_name = 'historie'  # here for namespacing of urls.

urlpatterns = [
    path("", views.list, name="list"),
    path('ajax/fetch_entries', views.fetch_entries, name="fetch_entries")
]
