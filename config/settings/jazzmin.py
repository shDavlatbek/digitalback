JAZZMIN_SETTINGS: dict = {
    'site_title': 'Forum Admin',
    'site_header': 'Forum Admin',
    'site_brand': 'Forum Admin',
    'welcome_sign': 'Xalqaro Ilmiy-Amaliy Forum',
    'copyright': 'Forum',
    'search_model': '',
    'topmenu_links': [],
    'usermenu_links': [{'model': 'auth.user'}],
    'show_sidebar': True,
    'navigation_expanded': True,
    'hide_apps': [],
    'hide_models': [],

    'order_with_respect_to': [
        'auth', 'user',
        'main',
        'main.mainsettings', 'main.footer', 'main.contact',
        'main.event', 'main.news',
        'main.supporter', 'main.sponsor',
        'main.faq', 'main.comment', 'main.pastforum',
        'main.presentationsubmission', 'main.partnerapplication', 'main.certificatecheck',
        'common', 'common.tinymceimage',
    ],

    'icons': {
        # Apps
        'auth': 'fas fa-users-cog',
        'main': 'fas fa-globe',
        'user': 'fas fa-user-shield',
        'common': 'fas fa-cogs',

        # Auth models
        'auth.Group': 'fas fa-users',

        # User models
        'user.user': 'fas fa-user-tie',

        # Main app - Settings
        'main.mainsettings': 'fas fa-sliders-h',
        'main.footer': 'fas fa-shoe-prints',
        'main.contact': 'fas fa-address-book',

        # Main app - Content
        'main.event': 'fas fa-calendar-alt',
        'main.news': 'fas fa-newspaper',
        'main.supporter': 'fas fa-hands-helping',
        'main.sponsor': 'fas fa-handshake',
        'main.faq': 'fas fa-question-circle',
        'main.comment': 'fas fa-comments',
        'main.pastforum': 'fas fa-history',

        # Main app - Forms
        'main.presentationsubmission': 'fas fa-file-powerpoint',
        'main.partnerapplication': 'fas fa-briefcase',
        'main.certificatecheck': 'fas fa-certificate',

        # Common app models
        'common.tinymceimage': 'fas fa-image',
    },
    'default_icon_parents': 'fas fa-chevron-circle-right',
    'default_icon_children': 'fas fa-circle',
    'related_modal_active': False,
    'show_ui_builder': False,
    'changeform_format': 'horizontal_tabs',
    'changeform_format_overrides': {
        'auth.user': 'collapsible',
        'auth.group': 'vertical_tabs',
        'main.event': 'horizontal_tabs',
    },
    'language_chooser': True,
}
