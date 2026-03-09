# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BMSB is a **single-tenant school management system** built with Django 5.2 + Django REST Framework. The backend is Uzbek-language oriented with i18n support for Uzbek (default), Russian, and English via `django-modeltranslation`.

## Development Commands

```bash
# Docker-based development (primary workflow)
docker compose -f dev.yml up -d --build     # Start dev environment (web on :8020, imgproxy on :8081)
docker compose -f dev.yml down               # Stop

# Django management (inside container or local venv)
python manage.py makemigrations              # Create migrations (never specify migration names)
python manage.py migrate                     # Apply migrations
python manage.py check                       # System check
python manage.py collectstatic --noinput     # Collect static files
python manage.py populate_site_settings      # Create default SiteSettings singleton
python manage.py add_timetables              # Create default timetable entries

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
- **common** — Base models, mixins, middleware, utilities, validators, image compression, custom DRF exception handler
- **main** — Core models: Teacher, Direction, FAQ, Vacancy, Staff, Leader, Banner, Menu (MPTT), TimeTable, Document, Honors, Comments, ContactForm, SiteSettings, EduInfo
- **news** — News articles and announcements
- **media** — Media collections (images, videos)
- **service** — Cultural/art services
- **resource** — Educational resources (YouTube links, PDF files)

### API Structure
All APIs are under `/api/` with per-app URL routing:
- `/api/` — main + common apps
- `/api/news/`, `/api/media/`, `/api/resources/`, `/api/services/`
- `/api/swagger/` — Swagger UI (drf-yasg)

## Key Patterns

1. **UniqueConstraint on slug fields** (never use `unique=True` on slug fields):
   - `UniqueConstraint(fields=['slug'], name='unique_modelname_slug')`
2. **Translation** — All user-facing text fields must be registered in each app's `translation.py` using `django-modeltranslation`
3. **File uploads** — Use `generate_upload_path` from `apps/common/utils.py` (auto-handles duplicates with UUID suffix). Validate with `file_size` (5MB) or `file_size_50` (50MB) from `apps/common/validators.py`
4. **New features must follow established patterns** — model + translation + admin + serializer + view + URL. See existing apps (e.g., FAQ, Vacancy, Staff) as templates
5. **Verbose names in Uzbek** — All model field `verbose_name` values should be in Uzbek
6. **SiteSettings** is a singleton — only one instance should exist

## Deployment

CI/CD via GitHub Actions (`.github/workflows/deploy.yml`):
- Push to `main` → deploys with `prod.yml` (Docker Compose)
- Push to `dev` → deploys with `dev.yml` (Docker Compose)

Database: SQLite in dev (default), PostgreSQL in production. imgproxy runs as a Docker sidecar for image optimization.
