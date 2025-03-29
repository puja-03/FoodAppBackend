from django.core.management.base import BaseCommand
from userapp.models import CustomUser

class Command(BaseCommand):
    help = "Seeds an admin user"

    def handle(self, *args, **kwargs):
        email ="admin@gmail.com"
        username = "admin"
        password = "admin123"
        is_verified = True

        if not CustomUser.objects.filter(email=email).exists():
            admin_user = CustomUser.objects.create_superuser(email=email, username=username, password=password, is_verified=is_verified)
            self.stdout.write(self.style.SUCCESS(f"Admin user created: {admin_user.email}"))
        else:
            self.stdout.write(self.style.WARNING("Admin user already exists."))
