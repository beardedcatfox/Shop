from book.models import Author, Book
from book.serializers import AuthorSerializer, BookSerializer, StatusSerializer

from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.utils import json

from storehouse.models import Order, OrderItem


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class AuthorList(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class OrderList(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = StatusSerializer


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def create_order(request):
    order_data = json.loads(request.body)

    order = Order.objects.create(
        order_id_in_shop=order_data['order_id_in_shop'],
        first_name=order_data['first_name'],
        last_name=order_data['last_name'],
        address=order_data['address'],
        status=order_data['status'],
        created=order_data['created']
    )

    for order_item_data in order_data['order_items']:
        OrderItem.objects.create(
            order=order,
            book_id=order_item_data['book'],
            quantity=order_item_data['quantity']
        )

    return Response(status=status.HTTP_201_CREATED)
