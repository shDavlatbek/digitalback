from django.urls import path
from .views.settings import MainSettingsView, FooterView, ContactView
from .views.event import EventListView, EventDetailView
from .views.content import (
    NewsListView, SupporterListView, SponsorListView,
    FAQListView, CommentListView, PastForumListView,
)
from .views.forms import (
    PresentationSubmissionCreateView,
    PartnerApplicationCreateView,
    CertificateCheckCreateView,
)

urlpatterns = [
    # Settings endpoints (singletons)
    path('settings/', MainSettingsView.as_view(), name='main-settings'),
    path('footer/', FooterView.as_view(), name='footer'),
    path('contact/', ContactView.as_view(), name='contact'),

    # Event endpoints
    path('events/', EventListView.as_view(), name='event-list'),
    path('events/<slug:slug>/', EventDetailView.as_view(), name='event-detail'),

    # Content endpoints
    path('news/', NewsListView.as_view(), name='news-list'),
    path('supporters/', SupporterListView.as_view(), name='supporter-list'),
    path('sponsors/', SponsorListView.as_view(), name='sponsor-list'),
    path('faqs/', FAQListView.as_view(), name='faq-list'),
    path('comments/', CommentListView.as_view(), name='comment-list'),
    path('past-forums/', PastForumListView.as_view(), name='past-forum-list'),

    # Form submission endpoints
    path('forms/presentation/', PresentationSubmissionCreateView.as_view(), name='presentation-submit'),
    path('forms/partner/', PartnerApplicationCreateView.as_view(), name='partner-apply'),
    path('forms/certificate-check/', CertificateCheckCreateView.as_view(), name='certificate-check'),
]
