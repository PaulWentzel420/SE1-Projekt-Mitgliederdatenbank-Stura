from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

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
        self.main_screen = reverse('checklisten:main_screen')
        self.abhaken = reverse('checklisten:abhaken')
        self.loeschen = reverse('checklisten:loeschen')
        self.erstellen = reverse('checklisten:erstellen')
        self.get_funktionen = reverse('checklisten:get_funktionen')
        pass

    def test_main_screen_GET(self):
        # unangemeldet
        response = self.client.get(self.main_screen)
        self.assertEqual(response.status_code, 302)

        # als admin
        self.client.login(username='testlukasadmin', password='0123456789test')
        response = self.client.get(self.main_screen)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checklisten/main_screen.html')
        self.client.logout()

        # als user
        self.client.login(username='testlukas', password='0123456789test')
        response = self.client.get(self.main_screen)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checklisten/main_screen.html')
        self.client.logout()
        pass
    pass
