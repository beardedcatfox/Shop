import os
from urllib.parse import urlparse

from celery import shared_task

from django.core.mail import send_mail

from orders.models import Order, OrderItem

import requests

from rest_framework.renderers import JSONRenderer

from .models import Author, Book


@shared_task
def update_authors():
    response = requests.get('http://127.0.0.1:8000/authors/')
    data = response.json()
    for item in data:
        author_id = item.get('id')
        author = Author.objects.filter(id_in_store=author_id).first()
        if not author:
            author = Author(id_in_store=author_id)
        author.id_in_store = author_id
        author.first_name = item.get('first_name')
        author.last_name = item.get('last_name')
        author.bio = item.get('bio')
        author.birth_date = item.get('birth_date') if item.get('birth_date') else None
        author.death_date = item.get('death_date') if item.get('death_date') else None
        image_url = item.get('image')
        if image_url:
            parsed_url = urlparse(image_url)
            image_name = os.path.basename(parsed_url.path)
            author.image = 'author_photo/' + image_name
        else:
            author.image = None
        author.save()


@shared_task
def update_books():
    response = requests.get('http://127.0.0.1:8000/books/')
    data = response.json()
    for item in data:
        book_id = item.get('id')
        book = Book.objects.filter(id_in_store=book_id).first()
        if not book:
            book = Book(id_in_store=book_id)
        book.id_in_store = book_id
        book.title = item.get('title')
        book.price = item.get('price')
        book.summary = item.get('summary')
        book.genre = item.get('genre')
        book.available = item.get('available')
        book.quantity = item.get('quantity')
        image_url = item.get('image')
        if image_url:
            parsed_url = urlparse(image_url)
            image_name = os.path.basename(parsed_url.path)
            book.image = 'book_image/' + image_name
        else:
            book.image = None
        author_id_in_store = item.get('author')
        if author_id_in_store:
            author = Author.objects.filter(id_in_store=author_id_in_store).first()
            if author:
                book.author = author
        book.save()


@shared_task
def order_send(order_id):
    order = Order.objects.get(id=order_id)

    key = os.environ.get('TOKEN_KEY')
    headers = {
        'Authorization': 'Token ' + key,
    }

    # Create list order items
    order_items = []
    for order_item in OrderItem.objects.filter(order=order):
        book = order_item.book.id_in_store
        quantity = order_item.quantity
        order_items.append({
            'order': order.id,
            'book': book,
            'quantity': quantity
        })

    # Create dict of order data
    order_data = {
        'order_id_in_shop': order.id,
        'first_name': order.first_name,
        'last_name': order.last_name,
        'address': order.address,
        'status': order.status,
        'created': order.created,
        'order_items': order_items
    }
    order_email = order.client.email

    send_mail(
        f'Your order #{order.id} received, wait for update',
        f'Your order #{order.id} received, wait for update',
        'from@example.com',
        [order_email],
        fail_silently=False,
    )

    renderer = JSONRenderer()
    serialized_order_data = renderer.render(order_data)

    requests.post('http://127.0.0.1:8000/orders/create/', data=serialized_order_data, headers=headers)


@shared_task
def check_order_statuses():
    response = requests.get('http://127.0.0.1:8000/status/')
    if response.status_code != 200:
        return

    order_statuses = response.json()

    for order_status in order_statuses:

        order_id = order_status['order_id_in_shop']
        new_status = order_status['status']
        try:
            order = Order.objects.get(id=order_id)
            if order.status != new_status:
                order.status = new_status
                order.save()
                order_email = order.client.email

                send_mail(
                    f'Your order #{order.id} has a new status: {new_status}',
                    f'Your order #{order.id} has a new status: {new_status}',
                    'from@example.com',
                    [order_email],
                    fail_silently=False,
                )
        except Order.DoesNotExist:
            pass
