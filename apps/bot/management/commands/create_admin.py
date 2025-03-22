import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from dotenv import load_dotenv


load_dotenv()


class Command(BaseCommand):
    help = "Create default admin"

    def handle(self, *args, **options):
        username = os.getenv("USERNAME", "admin")
        email = os.getenv("EMAIL", "admin@example.com")
        password = os.getenv("PASSWORD", "admin")

        if not User.objects.filter(username=username).exists():
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )
            self.stdout.write(
                self.style.SUCCESS(f"✅ Суперпользователь {username} создан!")
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"⚡ Суперпользователь {username} уже существует.")
            )
