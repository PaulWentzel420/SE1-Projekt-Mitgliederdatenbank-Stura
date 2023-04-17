from django.apps import apps
from django.test import TestCase
from historie.apps import HistorieConfig


class ReportsConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(HistorieConfig.name, 'historie')
        self.assertEqual(apps.get_app_config('historie').name, 'historie')
