from book.models import Author, Book

from django.core.management.base import BaseCommand

from faker import Faker

fake = Faker()


class Command(BaseCommand):
    help = 'Create fixtures for Author and Book models.'

    def add_arguments(self, parser):
        parser.add_argument('num_authors', type=int, help='Number of authors to create.')
        parser.add_argument('num_books', type=int, help='Number of books for each author.')

    def handle(self, *args, **options):
        num_authors = options['num_authors']
        num_books = options['num_books']

        for i in range(num_authors):
            first_name = fake.first_name()
            last_name = fake.last_name()
            bio = fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
            birth_date = fake.date_of_birth()
            author = Author(first_name=first_name,
                            last_name=last_name,
                            bio=bio,
                            birth_date=birth_date)
            author.save()

            for j in range(num_books):
                title = fake.sentence(nb_words=4, variable_nb_words=True)
                summary = fake.paragraph(nb_sentences=5, variable_nb_sentences=True)
                genre = fake.random_element(elements=[choice[0] for choice in Book.GENRE_CHOICES])
                price = fake.pyfloat(left_digits=2, right_digits=2, positive=True)
                quantity = 1000

                book = Book(title=title,
                            author=author,
                            summary=summary,
                            genre=genre,
                            available=True,
                            price=price,
                            quantity=quantity)
                book.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully created {num_authors} authors and {num_books} '
                                             f'books for each author.'))

# python manage.py create_fixtures <num_authors> <num_books>
