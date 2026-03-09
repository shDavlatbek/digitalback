from django.contrib import admin
from apps.common.mixins import AdminTranslation, DescriptionMixin
from apps.news.models import News, Category


@admin.register(Category)
class CategoryAdmin(AdminTranslation):
    list_display = ['name', 'is_active']

    prepopulated_fields = {
        'slug': ('name',),
    }


@admin.register(News)
class NewsAdmin(DescriptionMixin, AdminTranslation):
    list_display = ['image_tag', 'title', 'category', 'view_count', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    list_display_links = ['image_tag', 'title']
    prepopulated_fields = {
        'slug': ('title',),
    }
