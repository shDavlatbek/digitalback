from modeltranslation.translator import translator, TranslationOptions
from .models import (
    MainSettings,
    Event, EventSchedule, Speaker, EventMedia, News,
    Supporter, Sponsor, FAQ, Comment, PastForum,
)


class MainSettingsTranslationOptions(TranslationOptions):
    fields = ('title', 'short_description', 'quote', 'address')
    required_languages = ('uz',)


class EventTranslationOptions(TranslationOptions):
    fields = ('title', 'address', 'content', 'short_description')
    required_languages = ('uz',)


class EventScheduleTranslationOptions(TranslationOptions):
    fields = ('name',)
    required_languages = ('uz',)


class SpeakerTranslationOptions(TranslationOptions):
    fields = ('full_name', 'profession', 'content')
    required_languages = ('uz',)


class EventMediaTranslationOptions(TranslationOptions):
    fields = ('name',)
    required_languages = ('uz',)


class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'content')
    required_languages = ('uz',)


class SupporterTranslationOptions(TranslationOptions):
    fields = ('company_name',)
    required_languages = ('uz',)


class SponsorTranslationOptions(TranslationOptions):
    fields = ('company_name',)
    required_languages = ('uz',)


class FAQTranslationOptions(TranslationOptions):
    fields = ('question', 'answer')
    required_languages = ('uz',)


class CommentTranslationOptions(TranslationOptions):
    fields = ('full_name', 'profession', 'comment')
    required_languages = ('uz',)


class PastForumTranslationOptions(TranslationOptions):
    fields = ('name',)
    required_languages = ('uz',)


translator.register(MainSettings, MainSettingsTranslationOptions)
translator.register(Event, EventTranslationOptions)
translator.register(EventSchedule, EventScheduleTranslationOptions)
translator.register(Speaker, SpeakerTranslationOptions)
translator.register(EventMedia, EventMediaTranslationOptions)
translator.register(News, NewsTranslationOptions)
translator.register(Supporter, SupporterTranslationOptions)
translator.register(Sponsor, SponsorTranslationOptions)
translator.register(FAQ, FAQTranslationOptions)
translator.register(Comment, CommentTranslationOptions)
translator.register(PastForum, PastForumTranslationOptions)
