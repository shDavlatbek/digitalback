from django.contrib import admin
from apps.common.mixins import DescriptionMixin, AdminTranslation
from modeltranslation.admin import TranslationTabularInline
from modeltranslation import settings as mt_settings
from django.utils.safestring import mark_safe
from . import models


# =============================================
# MAIN SECTION - Settings (Singletons)
# =============================================

@admin.register(models.MainSettings)
class MainSettingsAdmin(AdminTranslation):
    exclude = ('is_active',)
    list_display = ('__str__', 'created_at')

    def has_add_permission(self, request):
        if models.MainSettings.objects.exists():
            return False
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(models.Footer)
class FooterAdmin(AdminTranslation):
    exclude = ('is_active',)
    list_display = ('__str__', 'created_at')

    def has_add_permission(self, request):
        if models.Footer.objects.exists():
            return False
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(models.Contact)
class ContactAdmin(AdminTranslation):
    exclude = ('is_active',)
    list_display = ('__str__', 'tel_phone', 'email', 'created_at')

    def has_add_permission(self, request):
        if models.Contact.objects.exists():
            return False
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


# =============================================
# WEB SECTION - Content
# =============================================

class EventScheduleInline(TranslationTabularInline):
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


class SpeakerInline(TranslationTabularInline):
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


class EventMediaInline(admin.TabularInline):
    model = models.EventMedia
    extra = 0


@admin.register(models.Event)
class EventAdmin(DescriptionMixin, AdminTranslation):
    list_display = ('image_tag', 'title', 'start_date', 'end_date', 'location', 'is_active')
    list_display_links = ('image_tag', 'title')
    list_filter = ('is_active', 'start_date')
    search_fields = ('title', 'content', 'location')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [EventScheduleInline, SpeakerInline, EventMediaInline]


@admin.register(models.News)
class NewsAdmin(DescriptionMixin, AdminTranslation):
    list_display = ('image_tag', 'title', 'is_active', 'created_at')
    list_display_links = ('image_tag', 'title')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'content')


@admin.register(models.Supporter)
class SupporterAdmin(AdminTranslation):
    list_display = ('logo_tag', 'company_name', 'is_active')
    list_display_links = ('logo_tag', 'company_name')
    list_filter = ('is_active',)
    search_fields = ('company_name',)


@admin.register(models.Sponsor)
class SponsorAdmin(AdminTranslation):
    list_display = ('logo_tag', 'company_name', 'is_active')
    list_display_links = ('logo_tag', 'company_name')
    list_filter = ('is_active',)
    search_fields = ('company_name',)


@admin.register(models.FAQ)
class FAQAdmin(AdminTranslation):
    list_display = ('question', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('question', 'answer')


@admin.register(models.Comment)
class CommentAdmin(AdminTranslation):
    list_display = ('image_tag', 'full_name', 'job', 'is_active', 'created_at')
    list_display_links = ('image_tag', 'full_name')
    list_filter = ('is_active', 'created_at')
    search_fields = ('full_name', 'comment')


@admin.register(models.PastForum)
class PastForumAdmin(AdminTranslation):
    list_display = ('image_tag', 'name', 'is_active')
    list_display_links = ('image_tag', 'name')
    list_filter = ('is_active',)
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
        'full_name', 'position', 'organization_name', 'phone', 'email',
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


@admin.register(models.CertificateCheck)
class CertificateCheckAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'certificate_number', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('full_name', 'certificate_number')
    readonly_fields = ('full_name', 'certificate_number', 'created_at', 'updated_at')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
