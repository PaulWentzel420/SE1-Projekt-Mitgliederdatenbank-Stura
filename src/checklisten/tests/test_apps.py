from django.apps import apps
from django.test import TestCase
from checklisten.apps import ChecklistenConfig


class ReportsConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(ChecklistenConfig.name, 'checklisten')
        self.assertEqual(apps.get_app_config('checklisten').name, 'checklisten')
