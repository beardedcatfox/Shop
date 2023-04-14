import random

from django.core.management.base import BaseCommand

from faker import Faker

from shop.models import Author, Book, Client


class Command(BaseCommand):
    help = 'Generates fake data for Client, Author, and Book models'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of each model to create')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        fake = Faker()

        for i in range(count):
            username = fake.unique.user_name()
            email = fake.unique.email()
            first_name = fake.first_name()
            last_name = fake.last_name()
            address = fake.address()
            birth_date = fake.date_of_birth()
            password = fake.password()
            client = Client.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                address=address,
                birth_date=birth_date,
            )
            self.stdout.write(self.style.SUCCESS(f'Created client {client}'))

        for i in range(count):
            author = Author.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                bio=fake.text(max_nb_chars=3200),
                birth_date=fake.date_of_birth(),
                death_date=fake.date_between(start_date='-90y', end_date='today'),
                id_in_store=fake.random_int()
            )

        for i in range(count):
            title = fake.sentence(nb_words=4, variable_nb_words=True, ext_word_list=None)
            author = random.choice(Author.objects.all())
            summary = fake.text(max_nb_chars=1000)
            genre = random.choice(['Drama', 'Mystery', 'Fantasy', 'Historical', 'Horror', 'Sci-Fi', 'Thriller',
                                   'Comedy', 'Science', 'Romance'])
            available = fake.boolean(chance_of_getting_true=90)
            price = fake.pydecimal(left_digits=3, right_digits=2, positive=True)
            quantity = fake.random_int(min=0, max=100)
            id_in_store = fake.unique.random_number()
            book = Book.objects.create(
                title=title,
                author=author,
                summary=summary,
                genre=genre,
                available=available,
                price=price,
                quantity=quantity,
                id_in_store=id_in_store,
            )
            self.stdout.write(self.style.SUCCESS(f'Created book {book}'))
