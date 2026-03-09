from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.common.mixins import DescriptionMixin, AdminTranslation
from mptt.admin import DraggableMPTTAdmin
from modeltranslation.admin import TranslationTabularInline, TranslationStackedInline
from modeltranslation import settings as mt_settings
from django.utils.translation import gettext_lazy as _
from . import models
from django.utils.safestring import mark_safe
from django import forms


@admin.register(models.Menu)
class MenuAdmin(AdminTranslation, DraggableMPTTAdmin):
    class Media:
        css = {
            'screen': ('css/admin_menu.css',),
        }


@admin.register(models.Banner)
class BannerAdmin(AdminTranslation):
    list_display = ('image_tag', 'title', 'is_active')
    search_fields = ('title',)
    list_filter = ('is_active',)
    list_display_links = ('image_tag', 'title')


@admin.register(models.SchoolLife)
class SchoolLifeAdmin(DescriptionMixin, AdminTranslation):
    list_display = ('image_tag', 'title', 'is_active')
    search_fields = ('title',)
    list_filter = ('is_active',)
    list_display_links = ('image_tag', 'title')


@admin.register(models.Direction)
class DirectionAdmin(DescriptionMixin, AdminTranslation):
    list_display = ('name', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)
    list_display_links = ('name',)
    prepopulated_fields = {
        'slug': ('name',),
    }


@admin.register(models.Subject)
class SubjectAdmin(DescriptionMixin, AdminTranslation):
    list_display = ('name', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)
    list_display_links = ('name',)
    prepopulated_fields = {
        'slug': ('name',),
    }


@admin.register(models.MusicalInstrument)
class MusicalInstrumentAdmin(DescriptionMixin, AdminTranslation):
    list_display = ('name', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)
    list_display_links = ('name',)
    prepopulated_fields = {
        'slug': ('name',),
    }


class TeacherExperienceInline(TranslationTabularInline):
    model = models.TeacherExperience
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


@admin.register(models.Teacher)
class TeacherAdmin(DescriptionMixin, admin.ModelAdmin):
    list_display = ('full_name', 'is_active')
    search_fields = ('full_name',)
    list_filter = ('is_active',)
    list_display_links = ('full_name',)
    inlines = [TeacherExperienceInline]
    prepopulated_fields = {
        'slug': ('full_name',),
    }


class DirectionSchoolForm(forms.ModelForm):
    class Meta:
        model  = models.DirectionSchool
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        # Exclude already-used directions (except the current instance)
        taken_qs = models.DirectionSchool.objects.all()
        if self.instance and self.instance.pk:
            taken_qs = taken_qs.exclude(pk=self.instance.pk)
        taken_ids = taken_qs.values_list("direction_id", flat=True)

        if "direction" in self.fields:
            self.fields["direction"].queryset = models.Direction.objects.exclude(id__in=taken_ids)


class DirectionImageInline(admin.TabularInline):
    model = models.DirectionImage
    extra = 0


class DirectionVideoInline(admin.TabularInline):
    model = models.DirectionVideo
    extra = 0


@admin.register(models.DirectionSchool)
class DirectionSchoolAdmin(DescriptionMixin, AdminTranslation):
    form = DirectionSchoolForm
    list_display = ("direction", "founded_year", "student_count", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("direction__name", "description")
    inlines = [DirectionImageInline, DirectionVideoInline]

    def get_form(self, request, obj=None, **kwargs):
        form_class = super().get_form(request, obj, **kwargs)

        class RequestForm(form_class):
            def __init__(self, *args, **kwargs):
                kwargs['request'] = request
                super().__init__(*args, **kwargs)

        return RequestForm


@admin.register(models.FAQ)
class FAQAdmin(AdminTranslation):
    list_display = ('title', 'is_active',)
    list_filter = ('is_active',)
    search_fields = ('title', 'description',)


@admin.register(models.Vacancy)
class VacancyAdmin(AdminTranslation):
    list_display = ('title', 'type', 'salary', 'location', 'is_active', 'created_at')
    list_filter = ('is_active', 'type', 'created_at')
    search_fields = ('title', 'description', 'requirements', 'location')
    prepopulated_fields = {'slug': ('title',)}

    def get_form(self, request, obj=None, **kwargs):
        """Override form to show choice labels in admin"""
        form = super().get_form(request, obj, **kwargs)
        return form


@admin.register(models.Document)
class DocumentAdmin(AdminTranslation):
    list_display = ('title', 'category', 'is_active', 'created_at')
    list_filter = ('is_active', 'category', 'created_at')
    search_fields = ('title',)


@admin.register(models.TimeTable)
class TimeTableAdmin(AdminTranslation):
    list_display = ('title', 'file', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(models.DocumentCategory)
class DocumentCategoryAdmin(AdminTranslation):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {
        'slug': ('name',),
    }


@admin.register(models.Staff)
class StaffAdmin(AdminTranslation):
    list_display = ('full_name', 'position', 'experience_years', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('full_name', 'position')
    prepopulated_fields = {'slug': ('full_name',)}


@admin.register(models.Leader)
class LeaderAdmin(AdminTranslation):
    list_display = ('full_name', 'position', 'working_days', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('full_name', 'position', 'description')
    prepopulated_fields = {'slug': ('full_name',)}


class HonorAchievementsInline(TranslationTabularInline):
    model = models.HonorAchievements
    extra = 0
    fields = ('year', 'description', 'address', 'is_active')

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


@admin.register(models.Honors)
class HonorsAdmin(DescriptionMixin, AdminTranslation):
    list_display = ('full_name', 'type', 'image_preview', 'is_active', 'created_at')
    list_filter = ('is_active', 'type', 'created_at')
    search_fields = ('full_name', 'description')
    prepopulated_fields = {'slug': ('full_name',)}
    inlines = [HonorAchievementsInline]

    def image_preview(self, obj):
        """Display image thumbnail in list view"""
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="height: 50px; width: 50px; object-fit: cover; border-radius: 4px;" />')
        return ""
    image_preview.short_description = "Rasm"


@admin.register(models.EduInfo)
class EduInfoAdmin(AdminTranslation):
    list_display = ('title', 'is_active')
    search_fields = ('title', 'description')


@admin.register(models.SiteSettings)
class SiteSettingsAdmin(AdminTranslation):
    exclude = ('is_active',)
    list_display = ('__str__', 'created_at')

    def has_add_permission(self, request):
        # Only allow one SiteSettings instance
        if models.SiteSettings.objects.exists():
            return False
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(models.ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('full_name', 'phone_number', 'message')
    readonly_fields = ('full_name', 'phone_number', 'message', 'created_at', 'updated_at')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(models.Comments)
class CommentsAdmin(AdminTranslation):
    list_display = ('full_name', 'rating', 'image_preview', 'is_active', 'created_at')
    list_filter = ('is_active', 'rating', 'created_at')
    search_fields = ('full_name', 'comment')

    def image_preview(self, obj):
        """Display image thumbnail in list view"""
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="height: 50px; width: 50px; object-fit: cover; border-radius: 4px;" />')
        return ""
    image_preview.short_description = "Rasm"


@admin.register(models.EmailSubscription)
class EmailSubscriptionAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
