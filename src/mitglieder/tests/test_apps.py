from django.apps import apps
from django.test import TestCase
from mitglieder.apps import MitgliederConfig


class ReportsConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(MitgliederConfig.name, 'mitglieder')
        self.assertEqual(apps.get_app_config('mitglieder').name, 'mitglieder')
