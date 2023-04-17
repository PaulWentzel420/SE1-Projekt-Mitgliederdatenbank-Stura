from django.apps import apps
from django.test import TestCase
from login.apps import LoginConfig


class ReportsConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(LoginConfig.name, 'login')
        self.assertEqual(apps.get_app_config('login').name, 'login')
