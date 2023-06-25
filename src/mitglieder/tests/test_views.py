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

        # Ein mitglied erstellen
        Mitglied.objects.create(
            name = "Peter",
            vorname = "Hans",
            spitzname = "Hansi",
            tel_mobil = "0352075199"
        )

        # URLS
        self.main_url = reverse('mitglieder:homepage')
        self.erstellenView = reverse('mitglieder:erstellenView')
        self.bearbeitenView = reverse('mitglieder:bearbeitenView', args="1")


    def test_main_GET(self):
        # unangemeldet
        response = self.client.get(self.main_url)
        self.assertEqual(response.status_code, 302)

        # als admin
        self.client.login(username='testlukasadmin', password='0123456789test')
        response = self.client.get(self.main_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mitglieder/mitglieder.html')
        self.client.logout()

        # als user
        self.client.login(username='testlukas', password='0123456789test')
        response = self.client.get(self.main_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mitglieder/mitglieder.html')
        self.client.logout()

    def test_erstellenView_GET(self):
        # unangemeldet
        response = self.client.get(self.erstellenView)
        self.assertEqual(response.status_code, 302)

        # als admin
        self.client.login(username='testlukasadmin', password='0123456789test')
        response = self.client.get(self.erstellenView)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mitglieder/mitglied_erstellen_bearbeiten.html')
        self.client.logout()

        # als user
        self.client.login(username='testlukas', password='0123456789test')
        response = self.client.get(self.erstellenView)
        self.assertEqual(response.status_code, 302)
        self.client.logout()

    def test_bearbeitenView_GET(self):
        # unangemeldet
        response = self.client.get(self.bearbeitenView)
        self.assertEqual(response.status_code, 302)

        # als admin
        self.client.login(username='testlukasadmin', password='0123456789test')
        response = self.client.get(self.bearbeitenView)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mitglieder/mitglied_erstellen_bearbeiten.html')
        self.client.logout()

        # als user
        self.client.login(username='testlukas', password='0123456789test')
        response = self.client.get(self.erstellenView)
        self.assertEqual(response.status_code, 302)
        self.client.logout()
