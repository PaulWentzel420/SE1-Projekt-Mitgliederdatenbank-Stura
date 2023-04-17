from django.urls import path
from . import views


app_name = 'login'  # here for namespacing of urls.

urlpatterns = [
    path("", views.main_screen, name="homepage"),
    path('logout/', views.logout_request, name="logout")
]
