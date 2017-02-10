Test Mixins
===========

ViewRequestFactoryTestMixin
---------------------------

In order to use the ``ViewRequestFactoryTestMixin`` you need to import it and
add a few methods on your test case. A typical test case looks like this::

    from django.test import TestCase

    from django_libs.tests.mixins import ViewRequestFactoryTestMixin
    from mixer.backend.django import mixer

    from .. import views


    class InvoiceDetailViewTestCase(ViewTestMixin, TestCase):
        """Tests for the ``InvoiceDetailView`` generic class based view."""
        view_class = views.InvoiceDetailView

        def setUp(self):
            self.invoice = mixer.blend('invoices.Invoice')
            self.user = self.invoice.user

        def get_view_kwargs(self):
            return {'pk': self.invoice.pk}

        def test_view(self):
            self.is_not_callable()  # anonymous
            self.is_callable(user=self.user)
            self.is_postable(user=self.user, data={'amount': 1},
                             to_url_name='invoice_list')
            self.is_postable(user=self.user, data={'amount': 1}, ajax=True)


    class InvoiceViewTestCase(ViewTestMixin, TestCase):
        """Tests for the ``invoice`` (non-class-based) view."""

        def setUp(self):
            self.view = views.invoice
            self.invoice = mixer.blend('invoices.Invoice')
            self.user = self.invoice.user

        def get_view_args(self):
            return (self.invoice.pk, )

        def test_view(self):
            self.is_not_callable()  # anonymous
            self.is_callable(user=self.user)
            self.is_postable(user=self.user, data={'amount': 1},
                             to_url_name='invoice_list')
            self.is_postable(user=self.user, data={'amount': 1}, ajax=True)

Have a look at the docstrings in the code for further explanations:
https://github.com/bitmazk/django-libs/blob/master/django_libs/tests/mixins.py

ViewTestMixin
-------------

In order to use the ``ViewTestMixin`` you need to import it and implement
a few methods on your test case. A typical test case looks like this::

    from django.test import TestCase
    from django_libs.tests.mixins import ViewTestMixin
    from your_invoice_app.tests.factories import InvoiceFactory

    class InvoiceDetailViewTestCase(ViewTestMixin, TestCase):
        """Tests for the ``InvoiceDetailView`` generic class based view."""
        def setUp(self):
            self.invoice = InvoiceFactory()
            self.user = self.invoice.user

        def get_view_name(self):
            return 'invoice_detail'

        def get_view_kwargs(self):
            return {'pk': self.invoice.pk}

        def test_view(self):
            self.should_redirect_to_login_when_anonymous()
            self.should_be_callable_when_authenticated(self.user)
            # your own tests here

For a slightly longer explanation on why the test looks like this, please read
on...

Tutorial
--------

It is a good idea to write a test that calls your view before you actually
write the view. And when you are at it, you might just as well test if a view
that is protected by ``login_required``, actually *does* require the user to
be logged in. Walking down that road, you might also just as well try to call
the view and manipulate the URL so that this user tries to access another
user's objects. And so on, and so forth...

Fact is: You will be calling ``self.client.get`` and ``self.client.post`` a lot
in your integration tests (don't confuse these tests with your unit tests).

Let's assume that you have defined your ``urls.py`` like this::

    ...
    url(r'^invoice/(?P<pk>\d+)/', InvoiceDetailView.as_view(), name='invoice_detail'),
    ...

In order to test such a view, you would create an
``integration_tests/views_tests.py`` file and create a test case for this
view::

    from django.test import TestCase

    class InvoiceDetailViewTestCase(TestCase):
        def test_view(self):
            resp = self.client.get('/invoice/1/')

Writing the test this way is flawed because if you ever change that URL your
test will fail. It would be much better to use the view name instead::

    from django.core.urlresolvers import reverse
    ...
    class InvoiceDetailViewTestCase(TestCase):
        def test_view(self):
            resp = self.client.get(reverse('invoice_detail'))

If your view is just slightly complex, you will have to call
``self.client.get`` several times and it is probably not a good idea to repeat
the string ``invoice_detail`` over and over again, because that might change as
well. So let's centralize the view name::

    class InvoiceDetailViewTestCase(TestCase):
        def get_view_name(self):
            return 'invoice_detail'

        def test_view(self):
            resp = self.client.get(reverse(self.get_view_name()))

The code above was simplified. The ``reverse`` calls would fail because the
view actually needs some kwargs. A proper call would look like this::

        invoice = InvoiceFactory()
        resp = self.client.get(reverse(self.get_view_name(), kwargs={
            'pk': invoice.pk}))

This can get annoying when you need to call the view many times because most
of the time you might call the view with the same kwargs. So let's centralize
the kwargs as well::

    class InvoiceDetailViewTestCase(TestCase):
        def setUp(self):
            self.invoice = InvoiceFactory()

        def get_view_name(self):
            ...

        def get_view_kwargs(self):
            return {'pk': self.invoice.pk}

        def test_view(self):
            resp = self.client.get(reverse(self.get_view_name(),
                self.get_view_kwargs()))

This is much better. Someone who looks at your test, can easily identify the
view name and the expected view kwargs that are needed to get a positive
response from the view. When writing tests you don't have to think about
the view name or about constructing the view kwargs any more, which will speed
up your workflow.

But this is still an awful lot of code to type. Which is why we created
the ViewTestMixin::

    class InvoiceDetailViewTestCase(ViewTestMixin, TestCase):
        def setUp(self):
            ...

        def get_view_name(self):
            ...

        def get_view_kwargs(self):
            ...

        def test_view(self):
            resp = self.client.get(self.get_url())

Now we have got it down to a one-liner to call ``self.client.get`` in a future
proof and maintainable way. After writing a few hundred tests with this
approach new patterns emerge. You will want to test almost all views if they
are accessible by anonymous or the opposite: If they are *not* accessible by
anonymous but by a logged in user.

For this reason the ``ViewTestMixin`` provides a few convenience methods::

    class InvoiceDetailViewTestCase(ViewTestMixin, TestCase):
        ...
        def test_view(self):
            user = UserFactory()
            self.should_redirect_to_login_view_when_anonymous()
            self.should_be_callable_when_authenticated(user)

If your view expectes some data payload (either POST or GET data), then you
can set ``self.data_payload`` in your test. If all your tests need the same
data, you can override the ``get_data_payload()`` method::

    class InvoiceDetailViewTestCase(ViewTestMixin, TestCase):
        ...
        def get_data_payload(self):
            # If you stick to this implementation, you can still change the
            # data payload for ``some`` of your tests.
            if hasattr(self, 'data_payload'):
                return self.data_payload
            return {'foo': 'bar', }

        def test_view(self):
            user = UserFactory()
            self.should_redirect_to_login_view_when_anonymous()

            # Now your view will be called with the given data payload
            self.should_be_callable_when_authenticated(user)

            self.data_payload = {'foobar': 'barfoo'}
            # Now you have changed the standard payload to be returned by
            # ``get_data_payload``
            self.should_be_callable_when_authenticated(user)


"is_callable" and "is_not_callable"
-----------------------------------

If a view becomes more complex, you might end up with rather many assertions
for many different situations. If you take all these cases into account when
testing, which you probably should, you will write a lot of::

    def test_view(self):
        # case 1
        resp = self.client.get(self.get_url())
        self.assertEqual(resp.status_code, 200, msg=(
            'If this then that, because foo is bar.'))
        # case 2
        resp = ...
        self.assertEqual(...)
        # case 3
        ...

``is_callable`` and ``is_not_callable`` let you quickly assign different values
to customize your actual assertion case in one method call.
``is_callable`` by default makes an assertion on status code 200.
``is_not_callable`` defaults to an assertion on status code 404.

.. warning:: Note if you used previous versions, that ``is_callable`` will only
    default to 200 in the future.
    It's best to use ``and_redirects_to`` for a redirect assertion or if you
    only want to make sure to get the right code set ``status_code`` to 302.

    Also the ``code`` parameter changed into ``status_code``.

    They can still be used, but you will get annoying warnings. So, you might
    as well change it right away.


+----------------------+-----------------------------------------------------------+
| Argument             | Definition                                                |
+======================+===========================================================+
| ``method``           | String that defines if either 'post' or 'get' is used.    |
+----------------------+-----------------------------------------------------------+
| ``data``             | dictionary with GET data payload or POST data. If not     |
|                      | provided it calls ``self.get_data_payload()`` instead.    |
+----------------------+-----------------------------------------------------------+
| ``kwargs``           | dictionary to overwrite view kwargs. If not provided, it  |
|                      | calls ``self.get_view_kwargs()`` instead.                 |
+----------------------+-----------------------------------------------------------+
| ``user``             | Assign a user instance to log this user in first. As in   |
|                      | ``self.should_be_callable_when_authenticated()`` the      |
|                      | password is expected to be 'test123'.                     |
+----------------------+-----------------------------------------------------------+
| ``anonymous``        | If this is assigned ``True``, the user is logged out      |
|                      | before the assertion. So basically you test with an       |
|                      | anonymous user. Default is ``False``.                     |
+----------------------+-----------------------------------------------------------+
| ``and_redirects_to`` | If set, it performs an ``assertRedirects`` assertion.     |
|                      | Note that, of course this will overwrite the              |
|                      | ``status_code`` to 302.                                   |
+----------------------+-----------------------------------------------------------+
| ``status_code``      | If set, it overrides the status code, the assertion is    |
|                      | made with.                                                |
+----------------------+-----------------------------------------------------------+
| ``ajax``             | If ``True`` it will automatically set                     |
|                      | ``HTTP_X_REQUESTED_WITH='XMLHttpRequest'`` to simulate    |
|                      | an ajax call. Defaults to ``False``.                      |
+----------------------+-----------------------------------------------------------+

You can also define no arguments to test according to your current situation.
Then still, it is a handy shortcut.


**Further methods are:**

* should_be_callable_when_anonymous
* should_be_callable_when_has_correct_permissions

Have a look at the docstrings in the code for further explanations:
https://github.com/bitmazk/django-libs/blob/master/django_libs/tests/mixins.py
