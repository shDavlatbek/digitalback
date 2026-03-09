from rest_framework.generics import ListAPIView
from apps.common.mixins import IsActiveFilterMixin
from apps.main.models import Vacancy
from apps.main.serializers.vacancy import VacancyListSerializer


class VacancyListView(IsActiveFilterMixin, ListAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyListSerializer
