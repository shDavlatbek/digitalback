from rest_framework import serializers
from django.utils.html import strip_tags
from ..models import Event, EventSchedule, Speaker, EventMedia


class EventScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventSchedule
        fields = ['id', 'date', 'name', 'start_time', 'end_time']


class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = ['id', 'full_name', 'profession', 'content', 'image']


class EventMediaSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = EventMedia
        fields = ['id', 'name', 'date', 'type', 'type_display', 'file', 'url']


class EventListSerializer(serializers.ModelSerializer):
    short_description = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'slug', 'image', 'address',
            'start_date', 'end_date', 'short_description', 'location', 'created_at'
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

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'slug', 'image', 'address',
            'start_date', 'end_date', 'content', 'short_description', 'location',
            'schedules', 'speakers', 'event_media', 'created_at'
        ]
