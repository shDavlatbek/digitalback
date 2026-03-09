from rest_framework import serializers
from ..models import ContactForm


class ContactFormCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactForm
        fields = ['full_name', 'phone_number', 'message']
