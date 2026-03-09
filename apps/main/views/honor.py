from rest_framework.generics import ListAPIView, RetrieveAPIView
from apps.common.mixins import IsActiveFilterMixin
from apps.main.models import Honors
from apps.main.serializers.honor import HonorsListSerializer, HonorsDetailSerializer


class HonorsListView(IsActiveFilterMixin, ListAPIView):
    queryset = Honors.objects.all()
    serializer_class = HonorsListSerializer


class HonorsDetailView(IsActiveFilterMixin, RetrieveAPIView):
    queryset = Honors.objects.all()
    serializer_class = HonorsDetailSerializer
    lookup_field = 'slug'
