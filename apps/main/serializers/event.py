from rest_framework import serializers
from django.utils.html import strip_tags
from apps.common.imgproxy import ImgproxyImageField
from ..models import Event, EventSchedule, Speaker, EventMedia


class EventScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventSchedule
        fields = ['id', 'date', 'name', 'start_time', 'end_time', 'order']


class SpeakerSerializer(serializers.ModelSerializer):
    event_name = serializers.CharField(source='event.title', read_only=True)
    image = ImgproxyImageField(imgproxy_options={'quality': 85, 'width': 400, 'height': 400, 'resize_type': 'fill'})

    class Meta:
        model = Speaker
        fields = ['id', 'full_name', 'profession', 'content', 'image', 'order', 'event_name']


class EventMediaSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = EventMedia
        fields = ['id', 'name', 'date', 'type', 'type_display', 'file', 'url', 'order']


class EventListSerializer(serializers.ModelSerializer):
    short_description = serializers.SerializerMethodField()
    image = ImgproxyImageField(imgproxy_options={'quality': 80, 'width': 1200})

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'slug', 'image', 'address',
            'start_date', 'end_date', 'short_description', 'location', 'created_at', 'order',
            'is_archived',
        ]

    def get_short_description(self, obj):
        if obj.short_description:
            return obj.short_description
        if obj.content:
            plain = strip_tags(obj.content)
            return plain[:200] + '...' if len(plain) > 200 else plain
        return ''


class EventDetailSerializer(serializers.ModelSerializer):
    schedules = EventScheduleSerializer(many=True, read_only=True)
    speakers = SpeakerSerializer(many=True, read_only=True)
    event_media = EventMediaSerializer(many=True, read_only=True)
    image = ImgproxyImageField(imgproxy_options={'quality': 90, 'width': 1920})

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'slug', 'image', 'video_url', 'video_file', 'address',
            'start_date', 'end_date', 'content', 'short_description', 'location',
            'schedules', 'speakers', 'event_media', 'created_at', 'order',
            'is_archived',
        ]
