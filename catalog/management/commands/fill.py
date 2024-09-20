from django.conf import settings
from django.core.management import BaseCommand
from django.core.management import call_command

FIXTURES_PATH = settings.BASE_DIR.joinpath('catalog.json')


class Command(BaseCommand):

    def handle(self, *args, **options):

        call_command('loaddata', FIXTURES_PATH)
