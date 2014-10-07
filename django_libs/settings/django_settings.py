"""Useful defualt settings that you might want to use in all your projects."""
import re


IGNORABLE_404_URLS = [
    re.compile(r'\..*$'),
    re.compile(r'^/media/'),
    re.compile(r'^/static/'),
]


IGNORABLE_404_USER_AGENTS = [
    re.compile(r'AhrefsBot', re.I),
    re.compile(r'EasouSpider', re.I),
    re.compile(r'FacebookBot', re.I),
    re.compile(r'Feedfetcher-Google', re.I),
    re.compile(r'Googlebot', re.I),
    re.compile(r'Mail.RU_Bot', re.I),
    re.compile(r'MJ12bot', re.I),
    re.compile(r'Test Certificate Info', re.I),
    re.compile(r'Twitterbot', re.I),
    re.compile(r'Yahoo! Slurp', re.I),
    re.compile(r'YandexBot', re.I),
    re.compile(r'bingbot', re.I),
    re.compile(r'coccoc', re.I),
    re.compile(r'crawl@publiclibraryarchive.org', re.I),
    re.compile(r'Baiduspider', re.I),
    re.compile(r'msnbot', re.I),
]
