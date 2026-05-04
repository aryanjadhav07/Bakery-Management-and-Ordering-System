#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bakery_platform.settings')
    try:
        from django.core.management import execute_from_command_line
        import django

        django.setup()  # ✅ VERY IMPORTANT

        # ✅ NOW SAFE TO USE MODELS
        from django.contrib.auth import get_user_model

        User = get_user_model()

        try:
            user = User.objects.get(username="KAVITA")
            user.is_staff = True
            user.is_superuser = True
            user.save()
            print("KAVITA is now admin!")
        except User.DoesNotExist:
            print("User KAVITA not found")

    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()