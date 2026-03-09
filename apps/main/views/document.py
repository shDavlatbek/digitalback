from rest_framework.generics import ListAPIView
from apps.common.mixins import IsActiveFilterMixin
from ..models import Document, DocumentCategory
from ..serializers.document import DocumentSerializer, DocumentCategorySerializer


class DocumentCategoryListView(IsActiveFilterMixin, ListAPIView):
    queryset = DocumentCategory.objects.all()
    serializer_class = DocumentCategorySerializer
    pagination_class = None


class DocumentListView(IsActiveFilterMixin, ListAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    pagination_class = None
