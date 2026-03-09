from rest_framework.generics import RetrieveAPIView
from apps.common.mixins import IsActiveFilterMixin
from ..models import MainSettings, Footer, Contact
from ..serializers.settings import MainSettingsSerializer, FooterSerializer, ContactSerializer


class MainSettingsView(RetrieveAPIView):
    serializer_class = MainSettingsSerializer

    def get_object(self):
        obj = MainSettings.objects.first()
        if not obj:
            obj = MainSettings.objects.create(title="Forum")
        return obj


class FooterView(RetrieveAPIView):
    serializer_class = FooterSerializer

    def get_object(self):
        obj = Footer.objects.first()
        if not obj:
            obj = Footer.objects.create()
        return obj


class ContactView(RetrieveAPIView):
    serializer_class = ContactSerializer

    def get_object(self):
        obj = Contact.objects.first()
        if not obj:
            obj = Contact.objects.create(
                tel_phone="",
                email="",
                address=""
            )
        return obj
