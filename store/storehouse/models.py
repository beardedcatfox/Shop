from book.models import Book

from django.db import models


class Order(models.Model):
    STATUS_CHOICES = [
        ('in_work', 'in_work'),
        ('success', 'success'),
        ('fail', 'fail'),
    ]
    order_id_in_shop = models.IntegerField(verbose_name='Order id in shop', unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='in_work')
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.status == 'success':
            for item in self.orderitem_set.all():
                book = item.book
                book.quantity -= item.quantity
                book.save()

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'Order {self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, to_field='order_id_in_shop', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def price(self):
        return self.book.price

    def __str__(self):
        return f"{self.quantity}x {self.book.title} in order #{self.order.id}"
