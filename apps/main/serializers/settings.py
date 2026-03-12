from rest_framework import serializers
from ..models import MainSettings


class MainSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainSettings
        fields = [
            'id', 'logo', 'title', 'short_description', 'menu_timer',
            'main_participants', 'top_managers',
            'department_personnel', 'sponsors_and_partners', 'location',
            'facebook', 'instagram', 'youtube', 'x', 'quote',
            'phone_number', 'email', 'address',
        ]
