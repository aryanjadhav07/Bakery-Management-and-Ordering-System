import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bakery_platform.settings")
django.setup()

from django.contrib.auth.models import User

username = "dell"
new_password = "dell200105"

user = User.objects.get(username=username)
user.set_password(new_password)
user.is_staff = True
user.is_superuser = True
user.save()

print("Superuser password reset successful.")