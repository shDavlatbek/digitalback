from django.core.management.base import BaseCommand
from apps.main.models import MainSettings, Footer, Contact


class Command(BaseCommand):
    help = 'Create default settings (MainSettings, Footer, Contact) if they do not exist'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be created without actually creating',
        )

    def handle(self, *args, **options):
        dry_run = options.get('dry_run')

        created = []

        if not MainSettings.objects.exists():
            if dry_run:
                self.stdout.write(self.style.WARNING('[DRY RUN] Would create MainSettings'))
            else:
                MainSettings.objects.create(title="Forum")
                created.append('MainSettings')

        if not Footer.objects.exists():
            if dry_run:
                self.stdout.write(self.style.WARNING('[DRY RUN] Would create Footer'))
            else:
                Footer.objects.create()
                created.append('Footer')

        if not Contact.objects.exists():
            if dry_run:
                self.stdout.write(self.style.WARNING('[DRY RUN] Would create Contact'))
            else:
                Contact.objects.create(
                    tel_phone="",
                    email="",
                    address=""
                )
                created.append('Contact')

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created: {", ".join(created)}'))
        elif not dry_run:
            self.stdout.write('All settings already exist. Skipping.')
