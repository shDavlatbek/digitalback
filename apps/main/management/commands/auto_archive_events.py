from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.main.models import Event, News


class Command(BaseCommand):
    help = 'Auto-archive events whose end_date is more than 1 month ago, and news older than 1 month'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be archived without actually archiving',
        )

    def handle(self, *args, **options):
        cutoff = timezone.now() - timedelta(days=30)
        dry_run = options['dry_run']

        # Archive events
        events = Event.objects.filter(
            is_archived=False,
            end_date__isnull=False,
            end_date__lt=cutoff,
        )

        if dry_run:
            for event in events:
                self.stdout.write(f'[DRY RUN] Would archive event: {event.title} (end_date: {event.end_date})')
        else:
            event_count = events.update(is_archived=True)
            self.stdout.write(self.style.SUCCESS(f'Archived {event_count} event(s)'))

        # Archive news
        news_qs = News.objects.filter(
            is_archived=False,
            created_at__lt=cutoff,
        )

        if dry_run:
            for news in news_qs:
                self.stdout.write(f'[DRY RUN] Would archive news: {news.title} (created_at: {news.created_at})')
        else:
            news_count = news_qs.update(is_archived=True)
            self.stdout.write(self.style.SUCCESS(f'Archived {news_count} news item(s)'))
