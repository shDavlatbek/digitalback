from rest_framework import generics
from apps.common.mixins import IsActiveFilterMixin
from ..models import Comments
from ..serializers.comments import CommentsListSerializer, CommentsDetailSerializer


class CommentsListView(IsActiveFilterMixin, generics.ListAPIView):
    """List all comments"""
    queryset = Comments.objects.all()
    serializer_class = CommentsListSerializer


class CommentsDetailView(IsActiveFilterMixin, generics.RetrieveAPIView):
    """Get a specific comment by ID"""
    queryset = Comments.objects.all()
    serializer_class = CommentsDetailSerializer
    lookup_field = 'id'
