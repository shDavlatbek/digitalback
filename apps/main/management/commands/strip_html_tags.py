from django.core.management.base import BaseCommand
from django.utils.html import strip_tags

from apps.main.models import Event, News


class Command(BaseCommand):
    help = "Strip HTML tags from Event.title, Event.short_description, and News.title fields"

    def handle(self, *args, **options):
        # Strip tags from Event fields
        events = Event.objects.all()
        event_count = 0
        for event in events:
            changed = False
            if event.title and strip_tags(event.title) != event.title:
                event.title = strip_tags(event.title).strip()
                changed = True
            if event.short_description and strip_tags(event.short_description) != event.short_description:
                event.short_description = strip_tags(event.short_description).strip()
                changed = True
            if changed:
                event.save()
                event_count += 1

        # Strip tags from News fields
        news_items = News.objects.all()
        news_count = 0
        for news in news_items:
            if news.title and strip_tags(news.title) != news.title:
                news.title = strip_tags(news.title).strip()
                news.save()
                news_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Done! Cleaned {event_count} events and {news_count} news items."
        ))
