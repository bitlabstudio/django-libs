"""Useful context  processors for your projects."""
from django.conf import settings


def analytics(request):
    """Adds the setting ANALYTICS_TRACKING_ID to the template context."""
    return {
        'ANALYTICS_TRACKING_ID': getattr(
            settings, 'ANALYTICS_TRACKING_ID', 'UA-XXXXXXX-XX'),
        'ANALYTICS_DOMAIN': getattr(
            settings, 'ANALYTICS_DOMAIN', 'auto')
    }
