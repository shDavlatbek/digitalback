from rest_framework import serializers
from apps.main.models import Vacancy


class VacancyListSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Vacancy
        fields = [
            'id', 'title', 'slug', 'description', 'salary', 'requirements',
            'location', 'type', 'type_display', 'created_at'
        ]
