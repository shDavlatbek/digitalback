from rest_framework.generics import ListAPIView
from apps.common.mixins import IsActiveFilterMixin
from apps.main.models import Menu
from apps.main.serializers.menu import MenuSerializer


class MenuView(IsActiveFilterMixin, ListAPIView):
    serializer_class = MenuSerializer
    pagination_class = None
    permission_classes = []

    queryset = (
        Menu.objects.root_nodes()
        .prefetch_related(
            "children",
            "children__children",
            "children__children__children",
        )
    )
