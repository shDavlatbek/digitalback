from rest_framework.generics import ListAPIView
from apps.common.mixins import IsActiveFilterMixin
from apps.main.models import FAQ
from apps.main.serializers.faq import FAQListSerializer


class FAQListView(IsActiveFilterMixin, ListAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQListSerializer
    pagination_class = None
