from rest_framework import serializers
from ..models import MainSettings, Footer, Contact


class MainSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainSettings
        fields = [
            'id', 'logo', 'title', 'desc', 'timer',
            'asosiy_qatnashchilar', 'top_menejerlar',
            'bolim_shaxslari', 'homiylar_va_hamkorlar', 'location'
        ]


class FooterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Footer
        fields = ['id', 'facebook', 'instagram', 'youtube', 'x', 'quote']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'tel_phone', 'email', 'address']
