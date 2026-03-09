from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Deprecated - timetables are no longer part of this project'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.WARNING('This command is deprecated. Timetables are no longer part of this project.')
        )
