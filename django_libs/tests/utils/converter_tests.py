"""Tests for the converter utils of ``django_libs``."""
import os

from django.test import TestCase

from ...utils.converter import html_to_plain_text


class HTMLToPlainTextTestCase(TestCase):
    """Tests for the ``html_to_plain_text`` function."""
    longMessage = True

    def test_html_to_plain_text(self):
        html = (
            """
            <html>
                    <head></head>
                    <body>
                        <ul>
                            <li>List element</li>
                            <li>List element</li>
                            <li>List element</li>
                        </ul>
                    </body>
                </html>
            """
        )
        self.assertEqual(
            html_to_plain_text(html),
            (
                '* List element                            '
                '\n  * List element                            '
                '\n  * List element'
            ),
            msg='Should return a formatted plain text.')
        path = os.path.dirname(os.path.abspath(__file__)) + ('/../test_app/templates/html_email.html')
        with open(path, 'r') as file:
            self.assertIn('[1]: *|ARCHIVE|*\n', html_to_plain_text(file.readlines()), msg=(
                'Should return a formatted plain text.'))

    def test_replace_links(self):
        html = (
            """
            <span>T1<span> <a href="www.example.com">link</a> <span>T2</span>
            <br />
            <span>T3</span>
            """
        )
        expected = "T1 link[1] T2            \n            T3\n\n[1]: www.example.com\n"
        result = html_to_plain_text(html)
        self.assertEqual(result, expected, msg=('Should replace links nicely'))

    def test_replace_br(self):
        html = (
            """
            <span>Text1<br>Text2</span>
            <br /><br />
            <span>Text3</span>
            """
        )
        result = html_to_plain_text(html)
        self.assertEqual(result, 'Text1\nText2            \n\n            Text3', msg=(
            'Should replace <br/> nicely'))
