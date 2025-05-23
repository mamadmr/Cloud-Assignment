from .celery import app as celery_app

# Ensure Celery runs with Django
__all__ = ("celery_app",)
