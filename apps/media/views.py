from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Prefetch

from apps.common.mixins import IsActiveFilterMixin
from .models import MediaCollection, MediaImage, MediaVideo
from .serializers import MediaCollectionListSerializer, MediaCollectionDetailSerializer, MediaVideoSerializer, MediaImageSerializer


class MediaCollectionListView(IsActiveFilterMixin, generics.ListAPIView):
    queryset = MediaCollection.objects.all().prefetch_related(
        Prefetch(
            'media_images',
            queryset=MediaImage.objects.filter(is_active=True).order_by('-show_in_main', 'id'),
            to_attr='ordered_images'
        )
    )
    serializer_class = MediaCollectionListSerializer


class MediaCollectionDetailView(IsActiveFilterMixin, generics.RetrieveAPIView):
    queryset = MediaCollection.objects.all().prefetch_related(
        'media_images__collection'
    )
    serializer_class = MediaCollectionDetailSerializer
    lookup_field = 'slug'


class MediaImageListView(IsActiveFilterMixin, generics.ListAPIView):
    queryset = MediaImage.objects.filter(show_in_main=True).select_related('collection')
    serializer_class = MediaImageSerializer


class MediaVideoListView(IsActiveFilterMixin, generics.ListAPIView):
    queryset = MediaVideo.objects.all()
    serializer_class = MediaVideoSerializer
