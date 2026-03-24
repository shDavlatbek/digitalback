from rest_framework import serializers
from apps.common.imgproxy import ImgproxyImageField
from ..models import News, NewsMedia, Supporter, Sponsor, FAQ, Comment, PastForum


class NewsMediaSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = NewsMedia
        fields = ['id', 'name', 'type', 'type_display', 'file', 'url', 'order']


class NewsListSerializer(serializers.ModelSerializer):
    image = ImgproxyImageField(imgproxy_options={'quality': 80, 'width': 1200})

    class Meta:
        model = News
        fields = ['id', 'title', 'slug', 'image', 'content', 'created_at', 'order']


class NewsDetailSerializer(serializers.ModelSerializer):
    image = ImgproxyImageField(imgproxy_options={'quality': 90, 'width': 1920})
    news_media = NewsMediaSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = ['id', 'title', 'slug', 'image', 'content', 'created_at', 'order', 'news_media']


class SupporterSerializer(serializers.ModelSerializer):
    logo = ImgproxyImageField(imgproxy_options={'quality': 85, 'width': 400})

    class Meta:
        page_size = 99
        model = Supporter
        fields = ['id', 'logo', 'company_name', 'order']


class SponsorSerializer(serializers.ModelSerializer):
    logo = ImgproxyImageField(imgproxy_options={'quality': 85, 'width': 400})

    class Meta:
        model = Sponsor
        fields = ['id', 'logo', 'company_name', 'order']


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'order']


class CommentSerializer(serializers.ModelSerializer):
    image = ImgproxyImageField(imgproxy_options={'quality': 80, 'width': 300, 'height': 300, 'resize_type': 'fill'})

    class Meta:
        model = Comment
        fields = ['id', 'image', 'full_name', 'profession', 'comment', 'created_at', 'order']


class PastForumSerializer(serializers.ModelSerializer):
    image = ImgproxyImageField(imgproxy_options={'quality': 80, 'width': 800})

    class Meta:
        model = PastForum
        fields = ['id', 'image', 'name', 'order']
