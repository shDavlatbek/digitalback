from rest_framework import generics

from apps.common.mixins import IsActiveFilterMixin
from ..models import Leader
from ..serializers.leader import LeaderListSerializer, LeaderDetailSerializer


class LeaderListView(IsActiveFilterMixin, generics.ListAPIView):
    queryset = Leader.objects.all()
    serializer_class = LeaderListSerializer


class LeaderDetailView(IsActiveFilterMixin, generics.RetrieveAPIView):
    queryset = Leader.objects.all()
    serializer_class = LeaderDetailSerializer
    lookup_field = 'slug'
