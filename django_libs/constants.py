"""Commonly used constants."""
from pytz import common_timezones

TIMEZONE_CHOICES = [(tz, tz) for tz in common_timezones]
