from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from core.models import TimestampedModel

class Order(TimestampedModel):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Accepted', 'Accepted'),
        ('Baking', 'Baking'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_orders")
    baker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="baker_orders")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    receipt_image = models.ImageField(upload_to='receipts/', null=True, blank=True)
    cancel_reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f'{self.quantity} x {self.product.name} (Order {self.order.id})'
