from rest_framework.generics import ListAPIView
from apps.common.mixins import IsActiveFilterMixin
from apps.main.models import SchoolLife
from apps.main.serializers.school_life import SchoolLifeSerializer


class SchoolLifeView(IsActiveFilterMixin, ListAPIView):
    serializer_class = SchoolLifeSerializer
    queryset = SchoolLife.objects.all()
    page_size = 3
