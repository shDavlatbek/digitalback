from django.contrib import admin
from apps.common.mixins import AdminTranslation, DescriptionMixin
from .models import CultureArt, FineArt, CultureService, ServiceImage, CultureServiceFile


class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 1
    fk_name = "service"
    fields = ('image', 'is_active')

    class Media:
        js = (
            "admin/js/jquery.init.js",
            "modeltranslation/js/force_jquery.js",
            "modeltranslation/js/tabbed_translation_fields.js",
        )
        css = {
            "all": ("modeltranslation/css/tabbed_translation_fields.css", "css/admin_translation.css",),
        }


class CultureServiceFileInline(admin.TabularInline):
    model = CultureServiceFile
    extra = 1
    fields = ('file', 'is_active')

    class Media:
        js = (
            "admin/js/jquery.init.js",
            "modeltranslation/js/force_jquery.js",
            "modeltranslation/js/tabbed_translation_fields.js",
        )
        css = {
            "all": ("modeltranslation/css/tabbed_translation_fields.css", "css/admin_translation.css",),
        }


@admin.register(CultureArt)
class CultureArtAdmin(DescriptionMixin, AdminTranslation):
    list_display = ('name', 'author_name', 'author_direction', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'author_name', 'description', 'tags')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ServiceImageInline]


@admin.register(FineArt)
class FineArtAdmin(DescriptionMixin, AdminTranslation):
    list_display = ('name', 'author_name', 'author_direction', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'author_name', 'description', 'tags')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ServiceImageInline]


@admin.register(CultureService)
class CultureServiceAdmin(DescriptionMixin, AdminTranslation):
    list_display = ('name', 'price', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description', 'tags')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ServiceImageInline, CultureServiceFileInline]
