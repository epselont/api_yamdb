import csv

from django.core.management import BaseCommand

from reviews.models import Genre_title, Genres, Titles

ALREDY_LOADED_ERROR_MESSAGE = """
Если вам нужно перезагрузить данные из CSV-файла,
сначала удалите файл db.sqlite3, чтобы уничтожить базу данных.
Затем запустите `python manage.py migrate` для новой пустой
базы данных с таблицами"""


class Command(BaseCommand):
    help = "Загрузка данных в genres.csv"

    def handle(self, *args, **options):

        if Genre_title.objects.exists():
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        print("Загрузка данных")

        with open('./static/data/genre_title.csv', encoding='utf-8') as file:
            data = csv.DictReader(file)
            for row in data:
                genre_title = Genre_title.objects.create()
                genre_title.id = row['id']
                if row['title_id'] != '':
                    genre_title.title_id = Titles.objects.get(
                        pk=row['title_id']
                    )
                if row['genre_id'] != '':
                    genre_title.genre_id = Genres.objects.get(
                        pk=row['genre_id']
                    )
                genre_title.save()

        print("Данные загружены")

#                data_load = Genre_title(
#                    id=row['id'],
#                    title_id=row['title_id'],
#                    genre_id=row['genre_id']
#                )
