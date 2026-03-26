from django.contrib import admin
from adminsortable2.admin import SortableInlineAdminMixin
from apps.common.mixins import DescriptionMixin, AdminTranslation, SortableAdminMixinCustom
from modeltranslation.admin import TranslationTabularInline
from modeltranslation import settings as mt_settings
from django.utils.safestring import mark_safe
from django import forms
from . import models
from apps.common.widgets import LeafletLocationWidget


# =============================================
# MAIN SECTION - Settings (Singletons)
# =============================================

@admin.register(models.MainSettings)
class MainSettingsAdmin(AdminTranslation):
    exclude = ('is_active', 'order')
    list_display = ('__str__', 'created_at')

    fieldsets = (
        ('Asosiy', {
            'fields': ('logo', 'title', 'short_description', 'menu_timer', 'location', 'quote')
        }),
        ('Hero Video', {
            'fields': ('hero_video_file', 'hero_video_url'),
            'description': 'Video fayl yuklansa, YouTube havolasidan ustunlik oladi. Agar ikkalasi ham bo\'sh bo\'lsa, standart rasm ko\'rsatiladi.',
        }),
        ('Raqamlar', {
            'fields': ('main_participants', 'top_managers', 'department_personnel', 'sponsors_and_partners')
        }),
        ('Ijtimoiy tarmoqlar', {
            'fields': ('facebook', 'instagram', 'youtube', 'x')
        }),
        ('Kontakt ma\'lumotlar', {
            'fields': ('phone_number', 'email', 'address')
        })
    )

    PLACEHOLDERS = {
        # 'title': 'Forum sarlavhasini kiriting',
        'short_description': 'Qisqa tavsif...',
        'facebook': 'https://facebook.com/sahifa',
        'instagram': 'https://instagram.com/username',
        'youtube': 'https://youtube.com/@kanal',
        'x': 'https://x.com/username',
        'phone_number': '+998 90 123 45 67',
        'email': 'info@example.com',
        'address': 'Toshkent sh., ...',
        'quote': 'Iqtibos matnini kiriting...',
        'main_participants': '500',
        'top_managers': '50',
        'department_personnel': '100',
        'sponsors_and_partners': '30',
    }

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'location':
            kwargs['widget'] = LeafletLocationWidget()
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if field and db_field.name in self.PLACEHOLDERS:
            field.widget.attrs['placeholder'] = self.PLACEHOLDERS[db_field.name]
        return field

    def has_add_permission(self, request):
        if models.MainSettings.objects.exists():
            return False
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


# =============================================
# WEB SECTION - Content
# =============================================

class EventScheduleInline(SortableInlineAdminMixin, TranslationTabularInline):
    model = models.EventSchedule
    extra = 0

    class Media:
        js = (
            "admin/js/jquery.init.js",
            "modeltranslation/js/force_jquery.js",
            mt_settings.JQUERY_UI_URL,
            "modeltranslation/js/tabbed_translation_fields.js",
        )
        css = {
            "all": ("modeltranslation/css/tabbed_translation_fields.css", "css/admin_translation.css",),
        }


class SpeakerInline(SortableInlineAdminMixin, TranslationTabularInline):
    model = models.Speaker
    extra = 0

    class Media:
        js = (
            "admin/js/jquery.init.js",
            "modeltranslation/js/force_jquery.js",
            mt_settings.JQUERY_UI_URL,
            "modeltranslation/js/tabbed_translation_fields.js",
        )
        css = {
            "all": ("modeltranslation/css/tabbed_translation_fields.css", "css/admin_translation.css",),
        }


class EventMediaInline(SortableInlineAdminMixin, TranslationTabularInline):
    model = models.EventMedia
    extra = 0

    class Media:
        js = (
            "admin/js/jquery.init.js",
            "modeltranslation/js/force_jquery.js",
            mt_settings.JQUERY_UI_URL,
            "modeltranslation/js/tabbed_translation_fields.js",
            "js/admin_media_toggle.js",
        )
        css = {
            "all": ("modeltranslation/css/tabbed_translation_fields.css", "css/admin_translation.css",),
        }


@admin.register(models.Event)
class EventAdmin(SortableAdminMixinCustom, DescriptionMixin, AdminTranslation):
    list_display = ('image_tag', 'title', 'start_date', 'end_date', 'is_archived', 'location', 'is_active')
    list_display_links = ('image_tag', 'title')
    list_filter = ('is_active', 'is_archived', 'start_date')
    list_editable = ('is_archived',)
    search_fields = ('title', 'content', 'location')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [EventScheduleInline, SpeakerInline, EventMediaInline]
    actions = ['mark_archived', 'mark_unarchived']

    PLACEHOLDERS = {
        'title': 'Tadbir sarlavhasini kiriting',
        'address': 'Toshkent sh., Amir Temur ko\'chasi 1',
        'short_description': 'Tadbir haqida qisqa ma\'lumot...',
    }

    @admin.action(description="Tanlangan tadbirlarni arxivlash")
    def mark_archived(self, request, queryset):
        count = queryset.update(is_archived=True)
        self.message_user(request, f"{count} ta tadbir arxivlandi.")

    @admin.action(description="Tanlangan tadbirlarni arxivdan chiqarish")
    def mark_unarchived(self, request, queryset):
        count = queryset.update(is_archived=False)
        self.message_user(request, f"{count} ta tadbir arxivdan chiqarildi.")

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'location':
            kwargs['widget'] = LeafletLocationWidget()
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if field and db_field.name in self.PLACEHOLDERS:
            field.widget.attrs['placeholder'] = self.PLACEHOLDERS[db_field.name]
        return field


class NewsMediaInline(SortableInlineAdminMixin, TranslationTabularInline):
    model = models.NewsMedia
    extra = 0

    class Media:
        js = (
            "admin/js/jquery.init.js",
            "modeltranslation/js/force_jquery.js",
            mt_settings.JQUERY_UI_URL,
            "modeltranslation/js/tabbed_translation_fields.js",
            "js/admin_media_toggle.js",
        )
        css = {
            "all": ("modeltranslation/css/tabbed_translation_fields.css", "css/admin_translation.css",),
        }


@admin.register(models.News)
class NewsAdmin(SortableAdminMixinCustom, DescriptionMixin, AdminTranslation):
    list_display = ('image_tag', 'title', 'is_archived', 'is_active', 'created_at')
    list_display_links = ('image_tag', 'title')
    list_filter = ('is_active', 'is_archived', 'created_at')
    list_editable = ('is_archived',)
    search_fields = ('title', 'content')
    inlines = [NewsMediaInline]
    actions = ['mark_archived', 'mark_unarchived']

    @admin.action(description="Tanlangan yangiliklarni arxivlash")
    def mark_archived(self, request, queryset):
        count = queryset.update(is_archived=True)
        self.message_user(request, f"{count} ta yangilik arxivlandi.")

    @admin.action(description="Tanlangan yangiliklarni arxivdan chiqarish")
    def mark_unarchived(self, request, queryset):
        count = queryset.update(is_archived=False)
        self.message_user(request, f"{count} ta yangilik arxivdan chiqarildi.")


@admin.register(models.Supporter)
class SupporterAdmin(SortableAdminMixinCustom, AdminTranslation):
    list_display = ('logo_tag', 'company_name', 'is_active')
    list_display_links = ('logo_tag', 'company_name')
    list_filter = ('is_active',)
    search_fields = ('company_name',)


@admin.register(models.Sponsor)
class SponsorAdmin(SortableAdminMixinCustom, AdminTranslation):
    list_display = ('logo_tag', 'company_name', 'is_active')
    list_display_links = ('logo_tag', 'company_name')
    list_filter = ('is_active',)
    search_fields = ('company_name',)


@admin.register(models.FAQ)
class FAQAdmin(SortableAdminMixinCustom, AdminTranslation):
    list_display = ('question', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('question', 'answer')


@admin.register(models.Comment)
class CommentAdmin(SortableAdminMixinCustom, AdminTranslation):
    list_display = ('image_tag', 'full_name', 'profession', 'is_active', 'created_at')
    list_display_links = ('image_tag', 'full_name')
    list_filter = ('is_active', 'created_at')
    search_fields = ('full_name', 'comment')


@admin.register(models.PastForum)
class PastForumAdmin(SortableAdminMixinCustom, AdminTranslation):
    list_display = ('image_tag', 'name', 'is_active')
    list_display_links = ('image_tag', 'name')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(models.Speaker)
class SpeakerAdmin(SortableAdminMixinCustom, AdminTranslation):
    list_display = ('image_tag', 'full_name', 'event', 'profession', 'is_active')
    list_display_links = ('image_tag', 'full_name')
    list_filter = ('is_active', 'event')
    search_fields = ('full_name', 'profession')


@admin.register(models.EventMedia)
class EventMediaAdmin(SortableAdminMixinCustom, admin.ModelAdmin):
    list_display = ('name', 'event', 'type', 'date', 'is_active')
    list_display_links = ('name',)
    list_filter = ('is_active', 'type', 'event')
    search_fields = ('name',)


@admin.register(models.NewsMedia)
class NewsMediaAdmin(SortableAdminMixinCustom, admin.ModelAdmin):
    list_display = ('name', 'news', 'type', 'is_active')
    list_display_links = ('name',)
    list_filter = ('is_active', 'type', 'news')
    search_fields = ('name',)


# =============================================
# FORMS SECTION - Submissions (Read-only)
# =============================================

@admin.register(models.PresentationSubmission)
class PresentationSubmissionAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'organization_name', 'presentation_topic', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('full_name', 'organization_name', 'presentation_topic')
    readonly_fields = (
        'full_name', 'profession', 'organization_name', 'phone', 'email',
        'organization_website', 'presentation_topic', 'pdf_file', 'created_at', 'updated_at'
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(models.PartnerApplication)
class PartnerApplicationAdmin(admin.ModelAdmin):
    list_display = ('organization_name', 'contact_person', 'phone', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('organization_name', 'contact_person')
    readonly_fields = (
        'organization_name', 'contact_person', 'phone', 'email', 'created_at', 'updated_at'
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(models.Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'event_name', 'certificate_number', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('full_name', 'event_name', 'certificate_number')
    readonly_fields = ('full_name', 'event_name', 'certificate_number', 'file', 'created_at', 'updated_at')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
