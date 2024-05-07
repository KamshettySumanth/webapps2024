from django.core.management.commands.runserver import Command as BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    def inner_run(self, *args, **options):
        call_command('create_initial_user')
        super().inner_run(*args, **options)