Factories
=========

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

    class NewsEntryFactory(HvadFactoryMixin, factory.DjangoModelFactory):
        FACTORY_FOR = NewsEntry

        language_code = 'en'  # This is important
        title = factory.Sequence(lambda x: 'A title {0}'.format(x))
        slug = factory.Sequence(lambda x: 'a-title-{0}'.format(x))
        is_published = True


SimpleTranslationMixin
++++++++++++++++++++++

Writing factories for models under
`simple-translation <https://github.com/fivethreeo/simple-translation>`_ is
a bit annoying because you always have to override the ``_prepare`` method
in order to create the translation object for the main object that you want
to create.

By using this mixin, we suggest the following pattern to ease the process of
writing factories for translateable objects::

    import factory
    from django_libs.tests.factories import SimpleTranslationMixin

    class PersonFactory(SimpleTranslationMixin, factory.Factory):
        """Factory for ``Person`` objects."""
        FACTORY_FOR = Person

        @staticmethod
        def _get_translation_factory_and_field():
            # 'person' is the name of the ForeignKey field on the translation
            # model
            return (PersonTranslationFactory, 'person')

    class PersonTranslationFactory(factory.Factory):
        """Factory for ``PersonTranslation`` objects."""
        FACTORY_FOR = PersonTranslation

        first_name = 'First name'
        person = factory.SubFactory(PersonFactory)
        language = 'en'

This allows you to use the ``PersonTranslationFactory`` which will create
a ``Person`` as well via the sub factory but sometimes it is just more
intuitive to use the ``Person`` factory (because you want to test something on
the ``Person`` model), so now you can do that as well and you will still get
a translation object created in the background. This is often important because
simple-translation relies on the fact that there is ALWAYS at least one
translation available.


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

..code-block:: python

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
