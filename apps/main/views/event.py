from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.common.mixins import IsActiveFilterMixin
from ..models import Event, Speaker, EventMedia, News
from ..serializers.event import EventListSerializer, EventDetailSerializer, SpeakerSerializer, EventMediaSerializer
from ..serializers.content import NewsListSerializer


class EventListView(IsActiveFilterMixin, ListAPIView):
    queryset = Event.objects.filter(is_archived=False)
    serializer_class = EventListSerializer


class EventDetailView(IsActiveFilterMixin, RetrieveAPIView):
    queryset = Event.objects.prefetch_related('schedules', 'speakers', 'event_media')
    serializer_class = EventDetailSerializer
    lookup_field = 'slug'


class SpeakerListView(IsActiveFilterMixin, ListAPIView):
    queryset = Speaker.objects.select_related('event').filter(event__is_archived=False)
    serializer_class = SpeakerSerializer


class SpeakerDetailView(IsActiveFilterMixin, RetrieveAPIView):
    queryset = Speaker.objects.select_related('event')
    serializer_class = SpeakerSerializer


class EventMediaListView(IsActiveFilterMixin, ListAPIView):
    queryset = EventMedia.objects.select_related('event').filter(event__is_archived=False)
    serializer_class = EventMediaSerializer


# =============================================
# ARCHIVE ENDPOINTS
# =============================================

class ArchiveYearsView(APIView):
    """Returns distinct years that have archived events."""

    def get(self, request):
        years = list(
            Event.objects.filter(is_active=True, is_archived=True)
            .values_list('start_date__year', flat=True)
            .distinct()
            .order_by('-start_date__year')
        )
        return Response({'years': years})


class ArchiveByYearView(APIView):
    """Returns archived events and news for a specific year."""

    def get(self, request, year):
        events = Event.objects.filter(
            is_active=True,
            is_archived=True,
            start_date__year=year,
        ).prefetch_related('schedules', 'speakers', 'event_media').order_by('start_date')

        news = News.objects.filter(
            is_active=True,
            is_archived=True,
            created_at__year=year,
        ).order_by('-created_at')

        events_data = EventDetailSerializer(events, many=True, context={'request': request}).data
        news_data = NewsListSerializer(news, many=True, context={'request': request}).data

        return Response({
            'year': year,
            'events': events_data,
            'news': news_data,
        })
