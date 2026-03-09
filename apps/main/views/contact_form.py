from rest_framework import generics, status
from rest_framework.response import Response
from ..models import ContactForm
from ..serializers.contact_form import ContactFormCreateSerializer


class ContactFormCreateView(generics.CreateAPIView):
    """Create contact form requests - no authentication required"""
    queryset = ContactForm.objects.all()
    serializer_class = ContactFormCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            "message": "So'rov muvaffaqiyatli yuborildi",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
