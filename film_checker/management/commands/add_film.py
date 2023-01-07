from django.core.management.base import BaseCommand, CommandError
from film_checker.models import Film


class Command(BaseCommand):
    help = 'Add film in the database'

    def add_arguments(self, parser):
        parser.add_argument('film_name', type=str)

    def handle(self, *args, **options):
        if Film.objects.filter(title=options['film_name']).exists():
            raise CommandError('Film already exists. Try another film')

        Film(title=options['film_name']).save()

        self.stdout.write(self.style.SUCCESS('Film [%s] was successfully added' % options['film_name']))
