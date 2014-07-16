"""Default settings for the CustomRaven404CatchMiddleware"""
RAVEN_IGNORABLE_USER_AGENTS = [
    r'^.*EasouSpider.*$',
    r'^.*Googlebot.*$',
    r'^.*bingbot.*$',
    r'^.*Twitterbot.*$',
    r'^.*Yahoo! Slurp.*$',
]
