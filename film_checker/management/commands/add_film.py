from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Print hello with argument __name__'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str)

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Hello %s' % options['name']))