import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bakery_platform.settings')
django.setup()

from products.models import Product

cakes = [
    {"name": "Vanilla Cake", "price": 400.00, "desc": "Classic, moist vanilla cake with creamy frosting."},
    {"name": "Butterscotch Cake", "price": 450.00, "desc": "Rich butterscotch flavor with crunchy praline."},
    {"name": "Pineapple Cake", "price": 500.00, "desc": "Sweet pineapple chunks blended with whipped cream."},
    {"name": "Mix Fruit Cake", "price": 600.00, "desc": "Loaded with fresh seasonal fruits."},
    {"name": "Strawberry Cake", "price": 550.00, "desc": "Delightful strawberry flavor with fresh berry toppings."},
    {"name": "Blueberry Cake", "price": 650.00, "desc": "Tangy and sweet blueberry filling layered inside."},
    {"name": "Chocolate Cake", "price": 500.00, "desc": "Classic rich and moist chocolate cake."},
    {"name": "Chocolate Truffle Cake", "price": 650.00, "desc": "Dense chocolate sponge with layers of dark truffle."},
    {"name": "Black Currant Cake", "price": 550.00, "desc": "Unique black currant compote with fresh cream."},
    {"name": "Black Forest Cake", "price": 450.00, "desc": "German classic with fresh cream, cherries, and chocolate shards."},
    {"name": "Kesar Pista Cake", "price": 700.00, "desc": "Traditional Indian flavors of saffron and pistachios."},
    {"name": "Red Velvet Cake", "price": 600.00, "desc": "Vibrant red sponge with smooth cream cheese frosting."},
    {"name": "Doll Cake", "price": 900.00, "desc": "Beautiful princess doll cake, perfect for birthdays."},
    {"name": "Rasmalai Cake", "price": 800.00, "desc": "Fusion cake blending milk solids and delicate cardamom flavors."},
    {"name": "Photo Print Cake", "price": 850.00, "desc": "Personalized cake with an edible printed photo."},
    {"name": "KitKat Cake", "price": 750.00, "desc": "Surrounded by KitKat bars and topped with gems or chocolates."}
]

print("Deleting old products...")
Product.objects.all().delete()

print("Populating Cake Products...")
for cake in cakes:
    # We will just leave the image field empty, as the templates can fall back to a placeholder url
    Product.objects.create(
        name=cake["name"],
        description=cake["desc"],
        price=cake["price"]
    )

print("Done populating 16 cakes!")
