from rest_framework import serializers
from ..models import News, Supporter, Sponsor, FAQ, Comment, PastForum


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'image', 'content', 'created_at']


class SupporterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supporter
        fields = ['id', 'logo', 'company_name']


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ['id', 'logo', 'company_name']


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'image', 'full_name', 'profession', 'comment', 'created_at']


class PastForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = PastForum
        fields = ['id', 'image', 'name']
