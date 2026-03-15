from django.contrib.admin import widgets as admin_widgets
from django.db import models

from tinymce import widgets as tinymce_widgets


class MiniTinyMCE(tinymce_widgets.TinyMCE):
    """
    A compact TinyMCE widget for short HTML texts.
    Only provides basic formatting: bold, italic, underline, links, colors.
    """

    def __init__(self, attrs=None, mce_attrs=None, **kwargs):
        default_mce_attrs = {
            'menubar': False,
            'statusbar': False,
            'plugins': 'link lists',
            'toolbar': (
                'bold italic underline | '
                # 'forecolor backcolor | '
                # 'link | '
                # 'bullist numlist | '
                'removeformat'
            ),
            'height': 150,
            'width': '100%',
            'branding': False,
            'content_style': 'body { font-size: 14px; }',
        }
        if mce_attrs:
            default_mce_attrs.update(mce_attrs)
        super().__init__(attrs=attrs, mce_attrs=default_mce_attrs, **kwargs)


class AdminMiniTinyMCE(MiniTinyMCE, admin_widgets.AdminTextareaWidget):
    pass


class MiniHTMLField(models.TextField):
    """
    A TextField that uses a compact TinyMCE widget in forms.
    Ideal for short HTML-enabled texts like titles, short descriptions, quotes.
    """

    def formfield(self, **kwargs):
        defaults = {'widget': MiniTinyMCE}
        defaults.update(kwargs)

        if defaults['widget'] == admin_widgets.AdminTextareaWidget:
            defaults['widget'] = AdminMiniTinyMCE

        return super().formfield(**defaults)
