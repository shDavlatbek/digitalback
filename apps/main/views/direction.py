from rest_framework import generics

from apps.common.mixins import IsActiveFilterMixin
from ..models import DirectionSchool
from ..serializers.direction import DirectionListSerializer, DirectionDetailSerializer


class DirectionListView(IsActiveFilterMixin, generics.ListAPIView):
    queryset = DirectionSchool.objects.all()
    serializer_class = DirectionListSerializer


class DirectionDetailView(IsActiveFilterMixin, generics.RetrieveAPIView):
    queryset = DirectionSchool.objects.select_related('direction').prefetch_related(
        'subjects',
        'musical_instruments',
        'direction_images',
        'direction_videos'
    )
    serializer_class = DirectionDetailSerializer
    lookup_field = 'direction__slug'
    lookup_url_kwarg = 'slug'
