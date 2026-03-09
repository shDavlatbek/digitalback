from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from apps.common.mixins import IsActiveFilterMixin
from .models import Service, CultureService, CultureArt, FineArt
from .serializers import (
    ServiceListSerializer, ServiceDetailSerializer,
    CultureServiceListSerializer, CultureServiceDetailSerializer,
    CultureArtListSerializer, CultureArtDetailSerializer,
    FineArtListSerializer, FineArtDetailSerializer
)

# Create your views here.

class ServiceListView(IsActiveFilterMixin, ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceListSerializer


class ServiceDetailView(IsActiveFilterMixin, RetrieveAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceDetailSerializer
    lookup_field = 'slug'


class CultureServiceListView(IsActiveFilterMixin, ListAPIView):
    queryset = CultureService.objects.all()
    serializer_class = CultureServiceListSerializer


class CultureServiceDetailView(IsActiveFilterMixin, RetrieveAPIView):
    queryset = CultureService.objects.all()
    serializer_class = CultureServiceDetailSerializer
    lookup_field = 'slug'


class CultureArtListView(IsActiveFilterMixin, ListAPIView):
    queryset = CultureArt.objects.all()
    serializer_class = CultureArtListSerializer


class CultureArtDetailView(IsActiveFilterMixin, RetrieveAPIView):
    queryset = CultureArt.objects.all()
    serializer_class = CultureArtDetailSerializer
    lookup_field = 'slug'


class FineArtListView(IsActiveFilterMixin, ListAPIView):
    queryset = FineArt.objects.all()
    serializer_class = FineArtListSerializer


class FineArtDetailView(IsActiveFilterMixin, RetrieveAPIView):
    queryset = FineArt.objects.all()
    serializer_class = FineArtDetailSerializer
    lookup_field = 'slug'
