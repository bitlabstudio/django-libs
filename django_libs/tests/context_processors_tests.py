"""Tests for the context processors of ``django_libs``."""
from django.test import TestCase

from ..context_processors import analytics


class AnalyticsTestCase(TestCase):
    """Tests for the ``analytics`` context processor."""
    longMessage = True

    def test_analytics(self):
        self.assertEqual(
            analytics(''), {
                'ANALYTICS_TRACKING_ID': 'UA-THISISNOREAL-ID',
                'ANALYTICS_DOMAIN': 'auto'})
