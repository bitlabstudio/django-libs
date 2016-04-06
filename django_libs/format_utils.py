"""
Utility functions to get language specific formats.

These functions are taken from the original django implementation and updated
to fit our needs.

The original code can be found here:
https://github.com/django/django/blob/master/django/utils/formats.py

"""
from django.conf import settings
# when working with django versions prior to 1.5, we need to use smart_str
# instead of force_str
try:
    from django.utils.encoding import force_str as str_encode
except ImportError:
    from django.utils.encoding import smart_str as str_encode

try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module
from django.utils.translation import (
    check_for_language,
    get_language,
    to_locale
)

CUSTOM_FORMAT_MODULE_PATHS = getattr(settings, 'CUSTOM_FORMAT_MODULE_PATHS',
                                     ['localized_names.formats'])

# format_cache is a mapping from (format_type, lang) to the format string.
# By using the cache, it is possible to avoid running get_format_modules
# repeatedly.
_format_cache = {}
_format_modules_cache = {}

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


def iter_format_modules(lang):
    """
    Does the heavy lifting of finding format modules.

    """
    if check_for_language(lang):
        format_locations = []
        for path in CUSTOM_FORMAT_MODULE_PATHS:
            format_locations.append(path + '.%s')
        format_locations.append('django.conf.locale.%s')
        locale = to_locale(lang)
        locales = [locale]
        if '_' in locale:
            locales.append(locale.split('_')[0])
        for location in format_locations:
            for loc in locales:
                try:
                    yield import_module('.formats', location % loc)
                except ImportError:
                    pass


def get_format_modules(lang=None, reverse=False):
    """
    Returns a list of the format modules found

    """
    if lang is None:
        lang = get_language()
    modules = _format_modules_cache.setdefault(lang, list(
        iter_format_modules(lang)))
    if reverse:
        return list(reversed(modules))
    return modules


def get_format(format_type, lang=None, use_l10n=None):
    """
    For a specific format type, returns the format for the current
    language (locale), defaults to the format in the settings.
    format_type is the name of the format, e.g. 'DATE_FORMAT'

    If use_l10n is provided and is not None, that will force the value to
    be localized (or not), overriding the value of settings.USE_L10N.

    """
    format_type = str_encode(format_type)
    if use_l10n or (use_l10n is None and settings.USE_L10N):
        if lang is None:
            lang = get_language()
        cache_key = (format_type, lang)
        try:
            cached = _format_cache[cache_key]
            if cached is not None:
                return cached
            else:
                # Return the general setting by default
                return getattr(settings, format_type)
        except KeyError:
            for module in get_format_modules(lang):
                try:
                    val = getattr(module, format_type)
                    for iso_input in ISO_INPUT_FORMATS.get(format_type, ()):
                        if iso_input not in val:
                            if isinstance(val, tuple):
                                val = list(val)
                            val.append(iso_input)
                    _format_cache[cache_key] = val
                    return val
                except AttributeError:
                    pass
            _format_cache[cache_key] = None
    return getattr(settings, format_type)
