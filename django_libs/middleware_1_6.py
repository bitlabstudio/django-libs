"""Custom middleware for Django 1.6 projects."""


class CustomBrokenLinkEmailsMiddleware(object):
    """Custom version that adds the user to the error email."""
    def process_response(self, request, response):
        """
        Send broken link emails for relevant 404 NOT FOUND responses.
        """
        if response.status_code == 404 and not settings.DEBUG:
            domain = request.get_host()
            path = request.get_full_path()
            referer = force_text(request.META.get('HTTP_REFERER', ''), errors='replace')

            if not self.is_ignorable_request(request, path, domain, referer):
                ua = request.META.get('HTTP_USER_AGENT', '<none>')
                ip = request.META.get('REMOTE_ADDR', '<none>')

                user = None
                if request.user and hasattr(request.user, 'email'):
                    user = request.user.email
                content = (
                    "Referrer: %s\n"
                    "Requested URL: %s\n"
                    "User agent: %s\n"
                    "IP address: %s\n"
                    "User: %s\n"
                ) % (referer, path, ua, ip, user)

                mail_managers(
                    "Broken %slink on %s" % (
                        ('INTERNAL ' if self.is_internal_request(domain, referer) else ''),
                        domain
                    ),
                    content,
                    fail_silently=True)
        return response

    def is_internal_request(self, domain, referer):
        """
        Returns True if the referring URL is the same domain as the current request.
        """
        # Different subdomains are treated as different domains.
        return bool(re.match("^https?://%s/" % re.escape(domain), referer))

    def is_ignorable_request(self, request, uri, domain, referer):
        """
        Returns True if the given request *shouldn't* notify the site managers.
        """
        # '?' in referer is identified as search engine source
        if (not referer or
                (not self.is_internal_request(domain, referer) and '?' in referer)):
            return True
        return any(pattern.search(uri) for pattern in settings.IGNORABLE_404_URLS)
