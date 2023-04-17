from django.test import SimpleTestCase
from django.urls import reverse, resolve

from historie.views import *

class TestUrls(SimpleTestCase):
    def test_main_screen_url_resolves(self):
        url = reverse('historie:list')
        self.assertEqual(resolve(url).func, list)

    """
    Template

    def test_xxxx_url_resolves(self):
        url = reverse('mitglieder:')
        self.assertEqual(resolve(url).func, )
    """
