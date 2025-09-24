from .base import *
import os

DEBUG = False

# -----------------------------
# Core prod settings
# -----------------------------
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY must be set in production environment!")

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "")
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS.split(",") if host]

CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "")
CSRF_TRUSTED_ORIGINS = [url.strip() for url in CSRF_TRUSTED_ORIGINS.split(",") if url]

# -----------------------------
# Database
# -----------------------------
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL must be set in production environment!")
DATABASES = {"default": DATABASE_URL}

# -----------------------------
# Static & media (optional prod overrides)
# -----------------------------
STATIC_ROOT = os.path.join(BASE_DIR, "assets")

# -----------------------------
# Redis & Celery (production uses OS env only)
# -----------------------------
CELERY_BROKER_URL = os.environ.get("REDIS_AS_BROKER_URL")
CELERY_RESULT_BACKEND = os.environ.get("REDIS_AS_BROKER_URL")
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("REDIS_AS_CACHE_URL"),
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

# -----------------------------
# Security
# -----------------------------
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
