from rest_framework.generics import ListAPIView, RetrieveAPIView
from apps.common.mixins import IsActiveFilterMixin
from ..models import News, Supporter, Sponsor, FAQ, Comment, PastForum
from ..serializers.content import (
    NewsSerializer, SupporterSerializer, SponsorSerializer,
    FAQSerializer, CommentSerializer, PastForumSerializer,
)


class NewsListView(IsActiveFilterMixin, ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class NewsDetailView(IsActiveFilterMixin, RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    lookup_field = 'slug'


class SupporterListView(IsActiveFilterMixin, ListAPIView):
    queryset = Supporter.objects.all()
    serializer_class = SupporterSerializer


class SponsorListView(IsActiveFilterMixin, ListAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer


class FAQListView(IsActiveFilterMixin, ListAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer


class CommentListView(IsActiveFilterMixin, ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class PastForumListView(IsActiveFilterMixin, ListAPIView):
    queryset = PastForum.objects.all()
    serializer_class = PastForumSerializer
