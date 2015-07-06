Factories
=========

IMPORTANT: The following factories are still available, but no longer
maintained. We recommend to use https://github.com/klen/mixer for fixtures.

HvadFactoryMixin
++++++++++++++++

Writing factories for models under
`django-hvad <http://django-hvad.readthedocs.org/en/latest/index.html>`_
is a bit hard because for each object you also have to create a translation
object. This mixin takes care of this. Simply inherit from this mixin and
write your factory as if it was a normal model, but make sure to add a
``language_code`` field with the default language you would like to use::

    import factory
    from django_libs.tests.factories import HvadFactoryMixin

    from .. import models

    class NewsEntryFactory(HvadFactoryMixin, factory.DjangoModelFactory):
        language_code = 'en'  # This is important
        title = factory.Sequence(lambda x: 'A title {0}'.format(x))
        slug = factory.Sequence(lambda x: 'a-title-{0}'.format(x))
        is_published = True

        class Meta:
            model = models.NewsEntry


UserFactory
-----------

We use https://github.com/rbarrois/factory_boy to create fixtures for our
tests. Since Django comes with a User model that is needed by almost all tests
a ``UserFactory`` is useful for all Django projects.

Usage
+++++

Let's assume you want to write a view test and your view requires an
authenticated user. You can create the user using the ``UserFactory`` like so::

    from django.test import TestCase
    from django_libs.tests.factories import UserFactory

    class MyViewTest(TestCase):
        def setUp(self):
            self.user = UserFactory()

        def test_view(self):
            self.client.login(username=self.user.email, password='test123')
            resp = self.client.get('/')
            self.assertEqual(resp.status_code, 200)


UploadedImageFactory
--------------------

Are you also tired of having to deal with images in upload form tests?
Well here's help!
With the ``UploadedImageFactory`` you can create a ``SimpleUploadedFile`` with
just one line of code.

Example:

.. code:: python

    # Say your form has an image field
    from django import forms

    MyImageForm(forms.Form):
        avatar = forms.ImageField(...)
        ...  # other fields

    # Then you want to test this, so in your test case you do
    from django.test import TestCase

    from django_libs.tests.factories import UploadedImageFactory

    from ..forms import MyForm

    class MyImageFormTestCase(TestCase):
        def test_form(self):
            files = {'avatar': UploadedImageFactory()}
            data = {
                ...  # other data
            }
            form = MyForm(data=data, files=files)
            self.assertTrue(form.is_valid())
