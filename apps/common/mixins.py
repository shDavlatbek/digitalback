from django.utils.text import slugify
from modeltranslation.admin import TabbedTranslationAdmin
from django.db.models import QuerySet


class ActiveQuerySet(QuerySet):
    def active(self):
        return self.filter(is_active=True)


class ActiveModelMixin:
    """
    A mixin to filter out inactive records automatically.
    Must be used with models that inherit from BaseModel.
    """
    def get_queryset(self):
        qs = super().get_queryset()
        if hasattr(qs.model, 'is_active'):
            return qs.filter(is_active=True)
        return qs


class IsActiveFilterMixin:
    """
    A mixin for DRF views to handle is_active filtering.
    Allows clients to include inactive records if they have the right permissions.
    """
    def get_queryset(self):
        qs = super().get_queryset()
        
        # Check if model has is_active field
        if not hasattr(qs.model, 'is_active'):
            return qs
            
        # By default, only show active records
        show_inactive = self.request.query_params.get('show_inactive', 'false').lower() == 'true'
        
        # Only allow staff/admin to see inactive records
        if show_inactive and self.request.user.is_staff:
            return qs
        else:
            return qs.filter(is_active=True)


class SlugifyMixin:
    slug_field = 'slug'
    slug_source = 'name'
    
    def save(self, *args, **kwargs):
        if not getattr(self, self.slug_field):
            source_value = getattr(self, self.slug_source)
            setattr(self, self.slug_field, slugify(source_value))
        return super().save(*args, **kwargs) 
    

class DescriptionMixin:
    class Media:
        js = ("js/admin_description.js",)


class AdminTranslation(TabbedTranslationAdmin):
    class Media:
        css = {
            "all": ("css/admin_translation.css",),
        }