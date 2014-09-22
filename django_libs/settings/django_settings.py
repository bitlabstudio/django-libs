"""Useful defualt settings that you might want to use in all your projects."""
import re


IGNORABLE_404_URLS = [
    re.compile(r'\..*$'),
    re.compile(r'^/media/'),
    re.compile(r'^/static/'),
]
