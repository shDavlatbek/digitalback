# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Forum/Conference Management System** built with Django 5.2 + Django REST Framework. The backend is Uzbek-language oriented with i18n support for Uzbek (default), Russian, and English via `django-modeltranslation`.

## Development Commands

```bash
# Docker-based development (primary workflow)
docker compose -f dev.yml up -d --build     # Start dev environment (web on :8020, imgproxy on :8081)
docker compose -f dev.yml down               # Stop

# Django management (inside container or local venv)
python manage.py makemigrations              # Create migrations
python manage.py migrate                     # Apply migrations
python manage.py check                       # System check
python manage.py collectstatic --noinput     # Collect static files
python manage.py populate_site_settings      # Create default settings (MainSettings, Footer, Contact)

# Settings module
DJANGO_SETTINGS_MODULE=config.settings.develop   # Dev (default in manage.py)
DJANGO_SETTINGS_MODULE=config.settings.prod      # Production
```

## Architecture

### Key Mixins (apps/common/mixins.py):
- **`IsActiveFilterMixin`** — API views: filters `is_active=True` by default, staff can pass `?show_inactive=true`
- **`SlugifyMixin`** — Models: auto-generates slug from `slug_source` field on save
- **`AdminTranslation`** (extends `TabbedTranslationAdmin`) — Admin: tabbed translation UI with custom CSS
- **`DescriptionMixin`** — Admin: adds JS for description fields

### Base Model (apps/common/models.py)
All models inherit from `BaseModel` which provides `created_at`, `updated_at`, `is_active` fields and an `ActiveManager` that supports `.active()` / `.inactive()` querysets.

### Custom User Model
`apps/user/models.py` — `User` extends `AbstractUser`. `AUTH_USER_MODEL = 'user.User'`.

### App Responsibilities
- **common** — Base models, mixins, middleware, utilities, validators, image compression, TinyMCE image uploads
- **main** — All forum models organized in 3 sections:
  - **Settings (singletons):** MainSettings, Footer, Contact
  - **Content:** Event (with EventSchedule, Speaker, EventMedia inlines), News, Supporter, Sponsor, FAQ, Comment, PastForum
  - **Forms (submissions):** PresentationSubmission, PartnerApplication, CertificateCheck
- **user** — Custom user model

### API Structure
All APIs are under `/api/`:
- `/api/settings/`, `/api/footer/`, `/api/contact/` — Singleton settings
- `/api/events/`, `/api/events/<slug>/` — Events with schedules, speakers, media
- `/api/news/`, `/api/supporters/`, `/api/sponsors/`, `/api/faqs/`, `/api/comments/`, `/api/past-forums/` — Content
- `/api/forms/presentation/`, `/api/forms/partner/`, `/api/forms/certificate-check/` — Form submissions (POST)
- `/api/swagger/` — Swagger UI (drf-yasg)

## Key Patterns

1. **UniqueConstraint on slug fields** (never use `unique=True` on slug fields):
   - `UniqueConstraint(fields=['slug'], name='unique_modelname_slug')`
2. **Translation** — All user-facing text fields must be registered in `apps/main/translation.py` using `django-modeltranslation`
3. **File uploads** — Use `generate_upload_path` from `apps/common/utils.py`. Validate with `file_size` (5MB) or `file_size_50` (50MB) from `apps/common/validators.py`
4. **New features must follow established patterns** — model + translation + admin + serializer + view + URL
5. **Verbose names in Uzbek** — All model field `verbose_name` values should be in Uzbek
6. **Singleton models** — MainSettings, Footer, Contact allow only one instance (enforced in admin)
7. **Form submissions are read-only in admin** — PresentationSubmission, PartnerApplication, CertificateCheck cannot be added or edited via admin

## Deployment

CI/CD via GitHub Actions (`.github/workflows/deploy.yml`):
- Push to `main` → deploys with `prod.yml` (Docker Compose)
- Push to `dev` → deploys with `dev.yml` (Docker Compose)

Database: SQLite in dev (default), PostgreSQL in production. imgproxy runs as a Docker sidecar for image optimization.
