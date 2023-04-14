from django.db import models

from storages.backends.s3boto3 import S3Boto3Storage


class BookImageStorage(S3Boto3Storage):
    location = 'book_image'


class AuthorPhotoStorage(S3Boto3Storage):
    location = 'author_photo'


class Author(models.Model):
    image = models.ImageField(upload_to='author_photo/', storage=AuthorPhotoStorage(), blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(max_length=3200, verbose_name='Bio', blank=True)
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


class Book(models.Model):
    GENRE_CHOICES = [
        ('Drama', 'Drama'),
        ('Mystery', 'Mystery'),
        ('Fantasy', 'Fantasy'),
        ('Historical', 'Historical'),
        ('Horror', 'Horror'),
        ('Sci-Fi', 'Sci-Fi'),
        ('Thriller', 'Thriller'),
        ('Comedy', 'Comedy'),
        ('Science', 'Science'),
        ('Romance', 'Romance'),
    ]
    image = models.ImageField(upload_to='book_image/', storage=BookImageStorage(), blank=True)
    title = models.CharField(max_length=200)
    author = models.ForeignKey("Author", on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
