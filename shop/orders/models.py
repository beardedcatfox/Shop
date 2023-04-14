from django.db import models

from shop.models import Book, Client


class Cart(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_subtotal(self):
        return self.book.price * self.quantity


class Order(models.Model):
    STATUS_CHOICES = [
        ('in_work', 'in_work'),
        ('success', 'success'),
        ('fail', 'fail'),
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='in_work')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'Order {self.id}'

    def get_total(self):
        return sum(item.quantity * item.book.price for item in OrderItem.objects.filter(order=self))

    def get_total_cost(self):
        return sum(item.quantity * item.book.price for item in self.order_items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def price(self):
        return self.book.price

    def get_cost(self):
        return self.quantity * self.book.price

    def __str__(self):
        return f"{self.quantity}x {self.book.title} in order #{self.order.id}"
