from django.core.management.base import BaseCommand
from apps.main.models import TimeTable


class Command(BaseCommand):
    help = 'Add default timetables if none exist'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be created without actually creating',
        )

    def handle(self, *args, **options):
        dry_run = options.get('dry_run')

        time_tables = [
            {'uz': '1-sinflar', 'ru': '1-классы', 'en': '1-classes'},
            {'uz': '2-sinflar', 'ru': '2-классы', 'en': '2-classes'},
            {'uz': '3-sinflar', 'ru': '3-классы', 'en': '3-classes'},
            {'uz': '4-sinflar', 'ru': '4-классы', 'en': '4-classes'},
            {'uz': '5-sinflar', 'ru': '5-классы', 'en': '5-classes'},
            {'uz': '6-sinflar', 'ru': '6-классы', 'en': '6-classes'},
            {'uz': '7-sinflar', 'ru': '7-классы', 'en': '7-classes'},
            {'uz': '8-sinflar', 'ru': '8-классы', 'en': '8-classes'},
            {'uz': '9-sinflar', 'ru': '9-классы', 'en': '9-classes'},
        ]

        existing_count = TimeTable.objects.count()

        if existing_count > 0:
            self.stdout.write(
                f"Already have {existing_count} timetables. Skipping."
            )
            return

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f"[DRY RUN] Would create {len(time_tables)} timetables."
                )
            )
            return

        for time_table in time_tables:
            TimeTable.objects.create(
                title=time_table['uz'],
                title_uz=time_table['uz'],
                title_ru=time_table['ru'],
                title_en=time_table['en']
            )

        self.stdout.write(
            self.style.SUCCESS(f"Created {len(time_tables)} timetables.")
        )
