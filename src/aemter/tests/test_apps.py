from django.apps import apps
from django.test import TestCase
from aemter.apps import AemterConfig


class ReportsConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(AemterConfig.name, 'aemter')
        self.assertEqual(apps.get_app_config('aemter').name, 'aemter')
