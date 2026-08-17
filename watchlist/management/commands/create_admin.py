import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create the admin user if it does not already exist"

    def handle(self, *args, **options):
        User = get_user_model()

        username = "admin"
        password = os.environ.get("DJANGO_ADMIN_PASSWORD")

        if not password:
            self.stdout.write("DJANGO_ADMIN_PASSWORD is not set.")
            return

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "is_staff": True,
                "is_superuser": True,
            },
        )

        if created:
            user.set_password(password)
            user.save()
            self.stdout.write("Admin user created.")
        else:
            self.stdout.write("Admin user already exists.")