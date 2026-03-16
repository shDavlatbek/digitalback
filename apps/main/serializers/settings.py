from rest_framework import serializers
from django.utils import timezone
from apps.common.imgproxy import ImgproxyImageField
from ..models import MainSettings


class MainSettingsSerializer(serializers.ModelSerializer):
    menu_timer = serializers.SerializerMethodField()
    logo = ImgproxyImageField(imgproxy_options={'quality': 90, 'width': 800})

    class Meta:
        model = MainSettings
        fields = [
            'id', 'logo', 'title', 'short_description', 'menu_timer',
            'main_participants', 'top_managers',
            'department_personnel', 'sponsors_and_partners', 'location',
            'facebook', 'instagram', 'youtube', 'x', 'quote',
            'phone_number', 'email', 'address',
        ]

    def get_menu_timer(self, obj):
        if obj.menu_timer:
            now = timezone.now()
            diff = obj.menu_timer - now
            return int(diff.total_seconds() * 1000)  # returning difference in milliseconds
        return None
