from django.contrib import admin

from storehouse.models import Order, OrderItem

from .models import Author, Book


class BookInline(admin.TabularInline):
    model = Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'genre', 'price', 'quantity']
    list_filter = ['genre', 'available', 'author']
    search_fields = ['title', 'author__first_name', 'author__last_name']
    actions = ['make_available', 'make_unavailable']
    ordering = ['title']
    list_per_page = 20

    def make_available(self, request, queryset):
        queryset.update(available=True)

    make_available.short_description = "Make selected books available"

    def make_unavailable(self, request, queryset):
        queryset.update(available=False)

    make_unavailable.short_description = "Make selected books unavailable"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(available=True)

    def get_ordering(self, request):
        if request.user.is_superuser:
            return self.ordering
        return ['title']

    def has_add_permission(self, request):
        return request.user.is_superuser


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'birth_date', 'has_photo']
    list_filter = ['birth_date', 'last_name', 'first_name']
    search_fields = ['first_name', 'last_name']
    inlines = [BookInline]
    ordering = ['last_name', 'first_name']
    list_per_page = 20

    def full_name(self, obj):
        return f"{obj.last_name}, {obj.first_name}"
    full_name.short_description = 'Author'

    def has_photo(self, obj):
        return bool(obj.image)
    has_photo.short_description = 'Photo'
    has_photo.boolean = True


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'book', 'quantity', 'price')
    search_fields = ('order__id', 'book__title', 'book__author__last_name', 'book__author__first_name')
    ordering = ('order', 'book')
    readonly_fields = ('price',)
    list_per_page = 20

    def price(self, obj):
        return obj.book.price


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_id_in_shop', 'first_name', 'last_name', 'address', 'status', 'created')
    list_filter = ('status', 'created')
    search_fields = ('id', 'client__username', 'client__first_name', 'client__last_name', 'first_name', 'last_name',
                     'address')
    ordering = ('-created',)
    list_per_page = 20
