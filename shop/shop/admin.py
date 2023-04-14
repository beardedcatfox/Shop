from django.contrib import admin

from orders.models import Cart, Order, OrderItem

from .models import Author, Book, Client


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'price', 'quantity', 'available')
    list_filter = ('genre', 'available')
    search_fields = ('title', 'author__first_name', 'author__last_name')
    ordering = ('title',)
    autocomplete_fields = ('author',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'bio', 'birth_date', 'death_date')
    list_filter = ('birth_date', 'death_date')
    search_fields = ('last_name', 'first_name')
    ordering = ('last_name', 'first_name')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'address', 'birth_date')
    list_filter = ('is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'quantity')
    search_fields = ('user__username', 'book__title', 'book__author__last_name', 'book__author__first_name')
    ordering = ('user', 'book')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'book', 'quantity', 'price')
    search_fields = ('order__id', 'book__title', 'book__author__last_name', 'book__author__first_name')
    ordering = ('order', 'book')
    readonly_fields = ('price',)

    def price(self, obj):
        return obj.book.price


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'first_name', 'last_name', 'address', 'status', 'created')
    list_filter = ('status', 'created')
    search_fields = ('id', 'client__username', 'client__first_name', 'client__last_name', 'first_name', 'last_name',
                     'address')
    ordering = ('-created',)
