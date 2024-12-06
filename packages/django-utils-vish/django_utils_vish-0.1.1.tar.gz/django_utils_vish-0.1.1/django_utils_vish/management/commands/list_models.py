from django.core.management.base import BaseCommand
from django.apps import apps

class Command(BaseCommand):
    help = "List all models in the project with their respective app labels."

    def handle(self, *args, **kwargs):
        for app_config in apps.get_app_configs():
            self.stdout.write(f"App: {app_config.label}")
            for model in app_config.get_models():
                self.stdout.write(f"  - {model.__name__}")
