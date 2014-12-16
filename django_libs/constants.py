"""Commonly used constants."""
from pytz import common_timezones

TIMEZONE_CHOICES = [(tz, tz) for tz in common_timezones]

ISO_INPUT_FORMATS = {
    'DATE_INPUT_FORMATS': ('%Y-%m-%d',),
    'TIME_INPUT_FORMATS': ('%H:%M:%S', '%H:%M:%S.%f', '%H:%M'),
    'DATETIME_INPUT_FORMATS': (
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M:%S.%f',
        '%Y-%m-%d %H:%M',
        '%Y-%m-%d'
    ),
}
