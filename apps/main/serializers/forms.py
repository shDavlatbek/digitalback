from rest_framework import serializers
from ..models import PresentationSubmission, PartnerApplication, Certificate


class PresentationSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PresentationSubmission
        fields = [
            'full_name', 'profession', 'organization_name',
            'phone', 'email', 'organization_website',
            'presentation_topic', 'pdf_file'
        ]


class PartnerApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerApplication
        fields = ['organization_name', 'contact_person', 'phone', 'email']


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ['full_name', 'event_name', 'certificate_number']
