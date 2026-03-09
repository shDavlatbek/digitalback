from django.core.management.base import BaseCommand
from apps.main.models import SiteSettings


class Command(BaseCommand):
    help = 'Create default SiteSettings if it does not exist'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be created without actually creating',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Update existing SiteSettings with default values for empty fields',
        )

    def handle(self, *args, **options):
        dry_run = options.get('dry_run')
        force = options.get('force')

        default_settings = {
            'school_life': "Maktabimiz hayoti haqida ma'lumot",
            'directions': "Bizning yo'nalishlar haqida ma'lumot",
            'numbers': "Maktab raqamlari haqida ma'lumot",
            'teachers': "O'qituvchilarimiz haqida ma'lumot",
            'honors': "Maktabimiz faxrlari haqida ma'lumot",
            'news': "Yangiliklar bo'limi haqida ma'lumot",
            'gallery': "Galereya bo'limi haqida ma'lumot",
            'contact': "Bog'lanish bo'limi haqida ma'lumot",
            'comments': "Izohlar bo'limi haqida ma'lumot",
            'faqs': "Ko'p beriladigan savollar haqida ma'lumot",
            'leaders': "Rahbariyat bo'limi haqida ma'lumot",
            'vacancies': "Vakansiyalar bo'limi haqida ma'lumot",
            'documents': "Hujjatlar bo'limi haqida ma'lumot",
            'timetables': "O'quv reja bo'limi haqida ma'lumot",
            'edu_infos': "Ta'lim ma'lumotlari bo'limi haqida ma'lumot",
            'events': "Tadbirlar bo'limi haqida ma'lumot",
            'resources': "Resurslar bo'limi haqida ma'lumot",
            'culture_services': "Madaniy xizmatlar haqida ma'lumot",
            'culture_arts': "Madaniy san'at haqida ma'lumot",
            'fine_arts': "Tasviriy san'at haqida ma'lumot"
        }

        existing = SiteSettings.objects.first()

        if existing and not force:
            self.stdout.write(
                self.style.WARNING(f'SiteSettings already exists (ID: {existing.id}) - skipped')
            )
            return

        if dry_run:
            if existing and force:
                self.stdout.write(self.style.WARNING('[DRY RUN] Would update existing SiteSettings'))
            else:
                self.stdout.write(self.style.SUCCESS('[DRY RUN] Would create SiteSettings'))
            return

        if existing and force:
            for field, value in default_settings.items():
                if not getattr(existing, field):
                    setattr(existing, field, value)
            existing.save()
            self.stdout.write(self.style.SUCCESS(f'Updated existing SiteSettings (ID: {existing.id})'))
        else:
            site_settings = SiteSettings.objects.create(**default_settings)
            self.stdout.write(self.style.SUCCESS(f'Created SiteSettings (ID: {site_settings.id})'))
