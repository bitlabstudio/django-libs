"""Additional helpful utility functions."""
import random

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from bs4 import BeautifulSoup
from HTMLParser import HTMLParser

from .loaders import load_member_from_setting


class conditional_decorator(object):
    """
    Allows you to use decorators based on a condition.

    Useful to require login only if a setting is set::

        @conditional_decorator(method_decorator(login_required), settings.FOO)
        def dispatch(self, request, *args, **kwargs):
            return super(...).dispatch(...)

    """
    def __init__(self, dec, condition):
        self.decorator = dec
        self.condition = condition

    def __call__(self, func):
        if not self.condition:
            # Return the function unchanged, not decorated.
            return func
        return self.decorator(func)


def create_random_string(length=7, chars='ABCDEFGHJKMNPQRSTUVWXYZ23456789',
                         repetitions=False):
    """
    Returns a random string, based on the provided arguments.

    It returns capital letters and numbers by default.
    Ambiguous characters are left out, repetitions will be avoided.

    """
    if repetitions:
        return ''.join(random.choice(chars) for _ in range(length))
    return ''.join(random.sample(chars, length))


def get_profile(user):
    """
    Makes sure to always return a valid profile for the user.

    If none exists, it creates one.

    :user: A Django ``User`` instance.

    """
    # try if we get a profile via the regular method
    try:
        return user.get_profile()
    except ObjectDoesNotExist:
        pass

    # check if we set a custom method for profile fetching
    setting = getattr(settings, 'GET_PROFILE_METHOD', None)
    if setting:
        method = load_member_from_setting('GET_PROFILE_METHOD')
        return method(user)

    app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')

    # the models.get_model method allows to read load the model from the app's
    # model cache to allow the setting to be written as 'app_name.ModelName'
    profile_cls = models.get_model(app_label, model_name)
    return profile_cls.objects.create(user=user)


class HTML2PlainParser(HTMLParser):
    """Custom html parser to convert html code to plain text."""
    def __init__(self):
        self.reset()
        self.text = ''  # Used to push the results into a variable
        self.links = []  # List of aggregated links

        # Settings
        self.ignored_elements = getattr(
            settings, 'HTML2PLAINTEXT_IGNORED_ELEMENTS',
            ['html', 'head', 'style', 'meta', 'title', 'img']
        )
        self.newline_before_elements = getattr(
            settings, 'HTML2PLAINTEXT_NEWLINE_BEFORE_ELEMENTS',
            ['br', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'p', 'li']
        )
        self.newline_after_elements = getattr(
            settings, 'HTML2PLAINTEXT_NEWLINE_AFTER_ELEMENTS',
            ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'p', 'td']
        )
        self.stroke_before_elements = getattr(
            settings, 'HTML2PLAINTEXT_STROKE_BEFORE_ELEMENTS',
            ['tr']
        )
        self.stroke_after_elements = getattr(
            settings, 'HTML2PLAINTEXT_STROKE_AFTER_ELEMENTS',
            ['tr']
        )
        self.stroke_text = getattr(settings, 'HTML2PLAINTEXT_STROKE_TEXT',
                                   '------------------------------\n')

    def handle_starttag(self, tag, attrs):
        """Handles every start tag like e.g. <p>."""
        if (tag in self.newline_before_elements):
            self.text += '\n'
        if (tag in self.stroke_before_elements
                and not self.text.endswith(self.stroke_text)):
            # Put a stroke in front of every relevant element, if there is some
            # content between it and its predecessor
            self.text += self.stroke_text
        if tag == 'a':
            # If it's a link, append it to the link list
            for attr in attrs:
                if attr[0] == 'href':
                    self.links.append((len(self.links) + 1, attr[1]))

    def handle_data(self, data):
        """Handles data between tags."""
        # Only proceed with unignored elements
        if not self.lasttag in self.ignored_elements:
            # Remove any predefined linebreaks
            text = data.replace('\n', '')
            # If there's some text left, proceed!
            if text:
                if self.lasttag == 'li':
                    # Use a special prefix for list elements
                    self.text += '  * '
                self.text += text
                if self.lasttag in self.newline_after_elements:
                    # Add a linebreak at the end of the content
                    self.text += '\n'

    def handle_endtag(self, tag):
        """Handles every end tag like e.g. </p>."""
        if tag in self.stroke_after_elements:
            if self.text.endswith(self.stroke_text):
                # Only add a stroke if there isn't already a stroke posted
                # In this case, there was no content between the tags, so
                # remove the starting stroke
                self.text = self.text[:-len(self.stroke_text)]
            else:
                # If there's no linebreak before the stroke, add one!
                if not self.text.endswith('\n'):
                    self.text += '\n'
                self.text += self.stroke_text
        if tag == 'a':
            # If it's a link, add a footnote
            self.text += '[{}]'.format(len(self.links))
        elif tag == 'br' and self.text and not self.text.endswith('\n'):
            # If it's a break, check if there's no break at the end of the
            # content. If there's none, add one!
            self.text += '\n'
        # Reset the lasttag, otherwise this parse can geht confused, if the
        # next element is not wrapped in a new tag.
        if tag == self.lasttag:
            self.lasttag = None


def html_to_plain_text(html):
    """Converts html code into formatted plain text."""
    # Use BeautifulSoup to normalize the html
    soup = BeautifulSoup(html)
    # Init the parser
    parser = HTML2PlainParser()
    parser.feed(str(soup))
    # Strip the end of the plain text
    result = parser.text.rstrip()
    # Add footnotes
    if parser.links:
        result += '\n\n'
        for link in parser.links:
            result += '[{}]: {}\n'.format(link[0], link[1])
    return result
