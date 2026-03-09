from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import F

from apps.common.mixins import IsActiveFilterMixin
from .models import ResourceVideo, ResourceFile
from .serializers import ResourceVideoSerializer, ResourceFileSerializer


class ResourceVideoListView(IsActiveFilterMixin, generics.ListAPIView):
    """List all resource videos"""
    queryset = ResourceVideo.objects.all()
    serializer_class = ResourceVideoSerializer


class ResourceVideoDetailView(IsActiveFilterMixin, generics.RetrieveAPIView):
    """Get a specific resource video and increment view count"""
    queryset = ResourceVideo.objects.all()
    serializer_class = ResourceVideoSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        ResourceVideo.objects.filter(pk=instance.pk).update(view_count=F('view_count') + 1)
        # Refresh the instance to get the updated view count
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ResourceFileListView(IsActiveFilterMixin, generics.ListAPIView):
    """List all resource files"""
    queryset = ResourceFile.objects.all()
    serializer_class = ResourceFileSerializer


class ResourceFileDetailView(IsActiveFilterMixin, generics.RetrieveAPIView):
    """Get a specific resource file and increment download count"""
    queryset = ResourceFile.objects.all()
    serializer_class = ResourceFileSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment download count
        ResourceFile.objects.filter(pk=instance.pk).update(download_count=F('download_count') + 1)
        # Refresh the instance to get the updated download count
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
