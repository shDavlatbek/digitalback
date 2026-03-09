from rest_framework import serializers
from ..models import PresentationSubmission, PartnerApplication, CertificateCheck


class PresentationSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PresentationSubmission
        fields = [
            'full_name', 'position', 'organization_name',
            'phone', 'email', 'organization_website',
            'presentation_topic', 'pdf_file'
        ]


class PartnerApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerApplication
        fields = ['organization_name', 'contact_person', 'phone', 'email']


class CertificateCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificateCheck
        fields = ['full_name', 'certificate_number']
