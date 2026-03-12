from rest_framework.generics import CreateAPIView
from ..models import PresentationSubmission, PartnerApplication, Certificate
from ..serializers.forms import (
    PresentationSubmissionSerializer,
    PartnerApplicationSerializer,
    CertificateSerializer,
)


class PresentationSubmissionCreateView(CreateAPIView):
    queryset = PresentationSubmission.objects.all()
    serializer_class = PresentationSubmissionSerializer


class PartnerApplicationCreateView(CreateAPIView):
    queryset = PartnerApplication.objects.all()
    serializer_class = PartnerApplicationSerializer


class CertificateCreateView(CreateAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
