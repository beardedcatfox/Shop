from book.models import Author, Book

from rest_framework import serializers

from storehouse.models import Order, OrderItem


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_id_in_shop', 'status']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['book', 'quantity']
