"""Additional helpful utility functions."""
import sys

from django.conf import settings

try:
    from html.parser import HTMLParser
except ImportError:
    from HTMLParser import HTMLParser

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma: nocover
    sys.stderr.write('Warning: BeautifulSoup could not be imported! Created'
                     ' fallback for tests to work.')

    def BeautifulSoup(x, y):
        return x


class HTML2PlainParser(HTMLParser):
    """Custom html parser to convert html code to plain text."""
    def __init__(self):
        try:
            super(HTML2PlainParser, self).__init__()
        except TypeError:
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
        if (tag in self.stroke_before_elements and not
                self.text.endswith(self.stroke_text)):
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
        if self.lasttag not in self.ignored_elements:
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
    soup = BeautifulSoup(html, "html.parser")
    # Init the parser
    parser = HTML2PlainParser()
    parser.feed(str(soup.encode('utf-8')))
    # Strip the end of the plain text
    result = parser.text.rstrip()
    # Add footnotes
    if parser.links:
        result += '\n\n'
        for link in parser.links:
            result += '[{}]: {}\n'.format(link[0], link[1])
    return result
