from rest_framework.generics import CreateAPIView
from ..models import PresentationSubmission, PartnerApplication, CertificateCheck
from ..serializers.forms import (
    PresentationSubmissionSerializer,
    PartnerApplicationSerializer,
    CertificateCheckSerializer,
)


class PresentationSubmissionCreateView(CreateAPIView):
    queryset = PresentationSubmission.objects.all()
    serializer_class = PresentationSubmissionSerializer


class PartnerApplicationCreateView(CreateAPIView):
    queryset = PartnerApplication.objects.all()
    serializer_class = PartnerApplicationSerializer


class CertificateCheckCreateView(CreateAPIView):
    queryset = CertificateCheck.objects.all()
    serializer_class = CertificateCheckSerializer
