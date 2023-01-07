import requests
from core import settings
from bs4 import BeautifulSoup
from django.utils import timezone
from film_checker.models import Film, CheckOne
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Check rating of all films in database'

    # def add_arguments(self, parser):
    #     parser.add_argument('film_name', type=str)

    def handle(self, *args, **options):
        for film in Film.objects.all():
            for page in range(1, settings.PAGES):
                try:
                    response = requests.get(
                        f'https://www.imdb.com/list/ls046196709/?sort=list_order,asc&st_dt=&mode=detail&page={page}',
                        'lxml')
                except Exception as e:
                    raise CommandError('Error with request: %s' % e)

                soup = BeautifulSoup(response.text, 'lxml')

                # get all titles and ratings of films
                title_rating = []
                content = soup.find('div', class_='lister-list').find_all('div', class_='lister-item-content')
                for item in content:
                    title = item.find_next('a').text
                    rating = item.find_next('span', class_='ipl-rating-star__rating').text
                    title_rating.append((title, rating))

                found = False

                # item[0] - title | item[1] = rating
                for item in title_rating:
                    if item[0] == film.title:
                        found = True

                        # insert film data in database
                        try:
                            # film = Film.objects.get(title=film.title)
                            film.last_rating = item[1]
                            film.last_time_checked = timezone.now()
                            film.save()
                        except Exception as e:
                            raise CommandError('Error with inserting into database: %s' % e)

                        # insert check data in database
                        try:
                            check_one = CheckOne(film=film, rating=item[1])
                            check_one.save()
                        except Exception as e:
                            raise CommandError('Error with inserting into database: %s' % e)

                        self.stdout.write(
                            self.style.SUCCESS('Film [%s] has rating - [%s]' % (film.title, item[1])))

                # stop iteration if rating was found
                if found:
                    break


