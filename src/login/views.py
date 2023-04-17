from django.shortcuts import render, redirect

from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.

def main_screen(request):
    """
    This view processes all login requests made via the form found at the app's root URL.
    If a user who is already logged in tries to access the page, they will automatically be redirected to /mitglieder.
    If the form was submitted, the view gets all data from the submitted form and tries to authenticate the user using that data. 
    If authentication is sucessful, the user will be logged in and shown an appropriate welcome message. Otherwise, or if the submitted form is invalid, the user will be shown an error message.
    If the user navigates to the login form (i.e. is not submitting any data), the AuthenticationForm provided by Django will be rendered.

    :param request: The HTTP request that triggered the view.
    :return: The rendered AuthenticationForm if no data was submitted, or a redirect to /mitglieder if the user was logged in successfully.
    """
    if request.user.is_authenticated:
        return redirect("/mitglieder")

    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Herzlich Willkommen, {username}!")
                return redirect('/mitglieder')
            else:
                messages.error(request, "Benutzername oder Passwort ungültig.")
        else:
            messages.error(request, "Benutzername oder Passwort ungültig.")

    form = AuthenticationForm()

    return render(request=request,
                  template_name="login/login.html",
                  context={"form":form})

def logout_request(request):
    """
    This view processes all logout requests made by navigating to /logout. It logs the user out and displays a goodbye message.

    :param request: The HTTP request that triggered the view.
    :return: A redirect to the app's root URL (i.e. the login form).
    """
    logout(request)
    messages.info(request, "Bis zum nächsten Mal!")
    return redirect("/")
