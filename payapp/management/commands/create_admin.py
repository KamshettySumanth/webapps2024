# myapp/management/commands/create_initial_user.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create initial admin user if it does not exist'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin1').exists():
            admin_user = User.objects.create_superuser('admin1', 'admin1@gmail.com', 'admin1')
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Successfully created admin user with superuser role'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists'))
