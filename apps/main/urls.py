from django.urls import path
from .views.settings import MainSettingsView
from .views.event import (
    EventListView, EventDetailView, SpeakerListView, SpeakerDetailView, EventMediaListView,
    ArchiveYearsView, ArchiveByYearView,
)
from .views.content import (
    NewsListView, NewsDetailView, SupporterListView, SponsorListView,
    FAQListView, CommentListView, PastForumListView,
)
from .views.forms import (
    PresentationSubmissionCreateView,
    PartnerApplicationCreateView,
    CertificateCreateView,
)

urlpatterns = [
    # Settings endpoints (singletons)
    path('settings/', MainSettingsView.as_view(), name='main-settings'),

    # Event endpoints
    path('events/', EventListView.as_view(), name='event-list'),
    path('events/<slug:slug>/', EventDetailView.as_view(), name='event-detail'),

    # Speaker & Media endpoints
    path('speakers/', SpeakerListView.as_view(), name='speaker-list'),
    path('speakers/<int:pk>/', SpeakerDetailView.as_view(), name='speaker-detail'),
    path('event-media/', EventMediaListView.as_view(), name='event-media-list'),

    # Archive endpoints
    path('archive/years/', ArchiveYearsView.as_view(), name='archive-years'),
    path('archive/<int:year>/', ArchiveByYearView.as_view(), name='archive-by-year'),

    # Content endpoints
    path('news/', NewsListView.as_view(), name='news-list'),
    path('news/<slug:slug>/', NewsDetailView.as_view(), name='news-detail'),
    path('supporters/', SupporterListView.as_view(), name='supporter-list'),
    path('sponsors/', SponsorListView.as_view(), name='sponsor-list'),
    path('faqs/', FAQListView.as_view(), name='faq-list'),
    path('comments/', CommentListView.as_view(), name='comment-list'),
    path('past-forums/', PastForumListView.as_view(), name='past-forum-list'),

    # Form submission endpoints
    path('forms/presentation/', PresentationSubmissionCreateView.as_view(), name='presentation-submit'),
    path('forms/partner/', PartnerApplicationCreateView.as_view(), name='partner-apply'),
    path('forms/certificate-check/', CertificateCreateView.as_view(), name='certificate-check'),
]
