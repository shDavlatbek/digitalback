from rest_framework.generics import ListAPIView
from apps.common.mixins import IsActiveFilterMixin
from apps.main.models import TimeTable
from apps.main.serializers.timetable import TimeTableListSerializer


class TimeTableListView(IsActiveFilterMixin, ListAPIView):
    queryset = TimeTable.objects.all()
    serializer_class = TimeTableListSerializer
    pagination_class = None
