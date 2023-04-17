from django.test import SimpleTestCase
from django.urls import reverse, resolve

from login.views import *

class TestUrls(SimpleTestCase):
    def test_main_screen_url_resolves(self):
        url = reverse('login:homepage')
        self.assertEqual(resolve(url).func, main_screen)

    def test_logout_request_url_resolves(self):
        url = reverse('login:logout')
        self.assertEqual(resolve(url).func, logout_request)

    """
    Template

    def test_xxxx_url_resolves(self):
        url = reverse('mitglieder:')
        self.assertEqual(resolve(url).func, )
    """
