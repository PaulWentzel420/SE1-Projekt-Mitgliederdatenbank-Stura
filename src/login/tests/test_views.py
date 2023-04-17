from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
import json

from mitglieder.models import Mitglied, MitgliedAmt, MitgliedMail

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        # Hinzufügen von Admin
        user = get_user_model().objects.create_superuser(
            username='testlukasadmin', password='0123456789test')

        # Hinzufügen von Nutzern
        user = get_user_model().objects.create_user(
            username='testlukas', password='0123456789test')

        # URLS
        self.main_screen = reverse('login:homepage')
        self.logout_request = reverse('login:logout')

    def test_main_screen_GET(self):
        # unangemeldet
        response = self.client.get(self.main_screen)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/login.html')

        # als admin
        self.client.login(username='testlukasadmin', password='0123456789test')
        response = self.client.get(self.main_screen)
        self.assertEqual(response.status_code, 302)
        self.client.logout()

        # als user
        self.client.login(username='testlukas', password='0123456789test')
        response = self.client.get(self.main_screen)
        self.assertEqual(response.status_code, 302)
        self.client.logout()

    def test_logout_request_GET(self):
        # unangemeldet
        response = self.client.get(self.logout_request)
        self.assertEqual(response.status_code, 302)

        # als admin
        self.client.login(username='testlukasadmin', password='0123456789test')
        response = self.client.get(self.logout_request)
        self.assertEqual(response.status_code, 302)
        self.client.logout()

        # als user
        self.client.login(username='testlukas', password='0123456789test')
        response = self.client.get(self.logout_request)
        self.assertEqual(response.status_code, 302)
        self.client.logout()
