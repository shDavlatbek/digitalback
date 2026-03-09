from rest_framework import generics

from apps.common.mixins import IsActiveFilterMixin
from ..models import Staff
from ..serializers.staff import StaffListSerializer


class StaffListView(IsActiveFilterMixin, generics.ListAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffListSerializer
