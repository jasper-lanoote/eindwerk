from django.core.management.base import BaseCommand
from weerstation.tasks import start_loop, stop_loop

class Command(BaseCommand):
    help = 'Start de weerstation lus'

    def handle(self, *args, **kwargs):
        self.stdout.write("De weerstation lus wordt gestart...")
        try:
            start_loop()
        except KeyboardInterrupt:
            stop_loop()
            self.stdout.write("De weerstation lus is gestopt.")
