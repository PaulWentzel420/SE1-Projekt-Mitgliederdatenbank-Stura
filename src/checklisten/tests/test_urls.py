from django.test import SimpleTestCase
from django.urls import reverse, resolve
from checklisten.views import *

class TestUrls(SimpleTestCase):
    def test_main_screen_url_resolves(self):
        url = reverse('checklisten:main_screen')
        self.assertEqual(resolve(url).func, main_screen)

    def test_abhaken_url_resolves(self):
        url = reverse('checklisten:abhaken')
        self.assertEqual(resolve(url).func, abhaken)

    def test_loeschen_url_resolves(self):
        url = reverse('checklisten:loeschen')
        self.assertEqual(resolve(url).func, loeschen)

    def test_erstellen_url_resolves(self):
        url = reverse('checklisten:erstellen')
        self.assertEqual(resolve(url).func, erstellen)

    def test_get_funktionen_url_resolves(self):
        url = reverse('checklisten:get_funktionen')
        self.assertEqual(resolve(url).func, get_funktionen)

    """
    Template

    def test_xxxx_url_resolves(self):
        url = reverse('mitglieder:')
        self.assertEqual(resolve(url).func, )
    """
