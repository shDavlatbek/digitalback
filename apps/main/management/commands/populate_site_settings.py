from django.core.management.base import BaseCommand
from apps.main.models import MainSettings


class Command(BaseCommand):
    help = 'Create default MainSettings if it does not exist'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be created without actually creating',
        )

    def handle(self, *args, **options):
        dry_run = options.get('dry_run')

        if not MainSettings.objects.exists():
            if dry_run:
                self.stdout.write(self.style.WARNING('[DRY RUN] Would create MainSettings'))
            else:
                MainSettings.objects.create(title="Forum")
                self.stdout.write(self.style.SUCCESS('Created: MainSettings'))
        else:
            if not dry_run:
                self.stdout.write('MainSettings already exists. Skipping.')
