"""Default settings for the CustomRaven404CatchMiddleware"""
RAVEN_IGNORABLE_USER_AGENTS = [
    r'^.*EasouSpider.*$',
    r'^.*Feedfetcher-Google.*$',
    r'^.*Googlebot.*$',
    r'^.*Twitterbot.*$',
    r'^.*Yahoo! Slurp.*$',
    r'^.*YandexBot.*$',
    r'^.*bingbot.*$',
]
