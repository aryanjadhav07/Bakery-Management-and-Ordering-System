from django.db import models
from django.contrib.auth.models import User
from core.models import TimestampedModel

class Product(TimestampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_half_kg = models.FloatField(null=True, blank=True)
    price_1kg = models.FloatField(null=True, blank=True)
    price_2kg = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to='product_images/', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_products')

    def __str__(self):
        return self.name
