"""Useful default settings that you might want to use in all your projects."""
import re


IGNORABLE_404_URLS = [
    re.compile(r'\..*$'),
    re.compile(r'^/media/'),
    re.compile(r'^/static/'),
]


IGNORABLE_404_USER_AGENTS = [
    re.compile(r'AhrefsBot', re.I),
    re.compile(r'BacklinkCrawler', re.I),
    re.compile(r'Baiduspider', re.I),
    re.compile(r'bingbot', re.I),
    re.compile(r'BLEXBot', re.I),
    re.compile(r'Cliqzbot', re.I),
    re.compile(r'coccoc', re.I),
    re.compile(r'DotBot', re.I),
    re.compile(r'EasouSpider', re.I),
    re.compile(r'Exabot', re.I),
    re.compile(r'FacebookBot', re.I),
    re.compile(r'Feedfetcher-Google', re.I),
    re.compile(r'Googlebot', re.I),
    re.compile(r'Jorgee', re.I),
    re.compile(r'Mail.RU_Bot', re.I),
    re.compile(r'mindUpBot', re.I),
    re.compile(r'MJ12bot', re.I),
    re.compile(r'msnbot', re.I),
    re.compile(r'publiclibraryarchive.org', re.I),
    re.compile(r'RU_Bot', re.I),
    re.compile(r'savetheworldheritage.org', re.I),
    re.compile(r'seoscanners', re.I),
    re.compile(r'spbot', re.I),
    re.compile(r'Test Certificate Info', re.I),
    re.compile(r'Twitterbot', re.I),
    re.compile(r'WinHttp.WinHttpRequest.5', re.I),
    re.compile(r'XoviBot', re.I),
    re.compile(r'Yahoo! Slurp', re.I),
    re.compile(r'YandexBot', re.I),
]
