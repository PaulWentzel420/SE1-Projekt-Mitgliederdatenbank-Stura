from django.apps import AppConfig


class AemterConfig(AppConfig):
    name = 'aemter'
    verbose_name = "Funktionen"

    def ready(self):
        import aemter.signals.handlers