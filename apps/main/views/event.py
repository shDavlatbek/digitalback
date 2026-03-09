from rest_framework.generics import ListAPIView, RetrieveAPIView
from apps.common.mixins import IsActiveFilterMixin
from ..models import Event
from ..serializers.event import EventListSerializer, EventDetailSerializer


class EventListView(IsActiveFilterMixin, ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventListSerializer


class EventDetailView(IsActiveFilterMixin, RetrieveAPIView):
    queryset = Event.objects.prefetch_related('schedules', 'speakers', 'event_media')
    serializer_class = EventDetailSerializer
    lookup_field = 'slug'
