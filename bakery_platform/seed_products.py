"""
seed_products.py
Run with: python seed_products.py
Re-populates the products table with the actual webp images from media/product_images/.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bakery_platform.settings')
django.setup()

from django.contrib.auth.models import User
from products.models import Product

baker = User.objects.filter(is_staff=True).first()
if not baker:
    print("WARNING: No baker (is_staff=True) user found. Products will have created_by=None.")

Product.objects.all().delete()
print("Cleared old products.")

cakes = [
    {
        'name': 'Biscoff Cheese Cake',
        'description': 'Creamy biscoff cheesecake with a crunchy lotus biscuit base and caramel drizzle.',
        'price': 750.00, 'price_half_kg': 400.00, 'price_1kg': 750.00, 'price_2kg': 1400.00,
        'image': 'product_images/biscoff_cheese_cake.webp',
    },
    {
        'name': 'Chocolate & Hazelnut Cake',
        'description': 'Rich chocolate sponge layered with smooth hazelnut praline cream.',
        'price': 700.00, 'price_half_kg': 380.00, 'price_1kg': 700.00, 'price_2kg': 1300.00,
        'image': 'product_images/chocolate_and_hazelnut.webp',
    },
    {
        'name': 'Chocolate Truffle Cake',
        'description': 'Dense chocolate sponge with layers of dark truffle ganache and cocoa dusting.',
        'price': 650.00, 'price_half_kg': 350.00, 'price_1kg': 650.00, 'price_2kg': 1200.00,
        'image': 'product_images/chocolat_truffle.webp',
    },
    {
        'name': 'Fruit Overload Cake',
        'description': 'Loaded with fresh seasonal fruits on a light vanilla sponge with whipped cream.',
        'price': 600.00, 'price_half_kg': 320.00, 'price_1kg': 600.00, 'price_2kg': 1100.00,
        'image': 'product_images/fruit-overload-cake.webp',
    },
    {
        'name': 'Vanilla Cake',
        'description': 'Classic moist vanilla cake with creamy frosting.',
        'price': 400.00, 'price_half_kg': 220.00, 'price_1kg': 400.00, 'price_2kg': 750.00,
        'image': '',
    },
    {
        'name': 'Butterscotch Cake',
        'description': 'Rich butterscotch flavor with crunchy praline topping.',
        'price': 450.00, 'price_half_kg': 240.00, 'price_1kg': 450.00, 'price_2kg': 850.00,
        'image': '',
    },
    {
        'name': 'Pineapple Cake',
        'description': 'Sweet pineapple chunks blended with fresh whipped cream.',
        'price': 500.00, 'price_half_kg': 270.00, 'price_1kg': 500.00, 'price_2kg': 950.00,
        'image': '',
    },
    {
        'name': 'Strawberry Cake',
        'description': 'Delightful strawberry flavor with fresh berry toppings.',
        'price': 550.00, 'price_half_kg': 290.00, 'price_1kg': 550.00, 'price_2kg': 1000.00,
        'image': '',
    },
    {
        'name': 'Black Forest Cake',
        'description': 'German classic with fresh cream, cherries, and chocolate shards.',
        'price': 450.00, 'price_half_kg': 240.00, 'price_1kg': 450.00, 'price_2kg': 850.00,
        'image': '',
    },
    {
        'name': 'Red Velvet Cake',
        'description': 'Vibrant red sponge with smooth cream cheese frosting.',
        'price': 600.00, 'price_half_kg': 320.00, 'price_1kg': 600.00, 'price_2kg': 1100.00,
        'image': '',
    },
    {
        'name': 'Rasmalai Cake',
        'description': 'Fusion cake blending milk solids and delicate cardamom flavors.',
        'price': 800.00, 'price_half_kg': 430.00, 'price_1kg': 800.00, 'price_2kg': 1500.00,
        'image': '',
    },
    {
        'name': 'KitKat Cake',
        'description': 'Surrounded by KitKat bars and topped with gems or chocolates.',
        'price': 750.00, 'price_half_kg': 400.00, 'price_1kg': 750.00, 'price_2kg': 1400.00,
        'image': '',
    },
]

for cake in cakes:
    p = Product(
        name=cake['name'],
        description=cake['description'],
        price=cake['price'],
        price_half_kg=cake['price_half_kg'],
        price_1kg=cake['price_1kg'],
        price_2kg=cake['price_2kg'],
        created_by=baker,
    )
    if cake['image']:
        p.image = cake['image']
    p.save()
    img_status = cake['image'] if cake['image'] else '(no image — fallback will show)'
    print(f"  Created: {cake['name']} | {img_status}")

print(f"\nDone. Total products in DB: {Product.objects.count()}")
