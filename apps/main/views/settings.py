from rest_framework.generics import RetrieveAPIView
from apps.common.mixins import IsActiveFilterMixin
from ..models import MainSettings
from ..serializers.settings import MainSettingsSerializer


class MainSettingsView(RetrieveAPIView):
    serializer_class = MainSettingsSerializer

    def get_object(self):
        obj = MainSettings.objects.first()
        if not obj:
            obj = MainSettings.objects.create(title="Forum")
        return obj
