from rest_framework.generics import ListAPIView, RetrieveAPIView
from apps.common.mixins import IsActiveFilterMixin
from ..models import Event, Speaker, EventMedia
from ..serializers.event import EventListSerializer, EventDetailSerializer, SpeakerSerializer, EventMediaSerializer


class EventListView(IsActiveFilterMixin, ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventListSerializer


class EventDetailView(IsActiveFilterMixin, RetrieveAPIView):
    queryset = Event.objects.prefetch_related('schedules', 'speakers', 'event_media')
    serializer_class = EventDetailSerializer
    lookup_field = 'slug'


class SpeakerListView(IsActiveFilterMixin, ListAPIView):
    queryset = Speaker.objects.select_related('event')
    serializer_class = SpeakerSerializer


class SpeakerDetailView(IsActiveFilterMixin, RetrieveAPIView):
    queryset = Speaker.objects.select_related('event')
    serializer_class = SpeakerSerializer


class EventMediaListView(IsActiveFilterMixin, ListAPIView):
    queryset = EventMedia.objects.select_related('event')
    serializer_class = EventMediaSerializer
