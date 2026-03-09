from rest_framework.generics import ListAPIView
from apps.common.mixins import IsActiveFilterMixin
from ..models import EduInfo
from ..serializers.edu_info import EduInfoSerializer


class EduInfoListView(IsActiveFilterMixin, ListAPIView):
    queryset = EduInfo.objects.all()
    serializer_class = EduInfoSerializer
    pagination_class = None
