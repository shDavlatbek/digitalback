from rest_framework import generics

from apps.common.mixins import IsActiveFilterMixin
from ..models import Teacher
from ..serializers.teacher import TeacherListSerializer, TeacherDetailSerializer


class TeacherListView(IsActiveFilterMixin, generics.ListAPIView):
    queryset = Teacher.objects.all().prefetch_related('directions')
    serializer_class = TeacherListSerializer


class TeacherDetailView(IsActiveFilterMixin, generics.RetrieveAPIView):
    queryset = Teacher.objects.all().prefetch_related(
        'directions',
        'experiences'
    )
    serializer_class = TeacherDetailSerializer
    lookup_field = 'slug'
