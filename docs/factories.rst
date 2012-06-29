Factories
=========

We use https://github.com/rbarrois/factory_boy to create fixtures for our
tests. Since Django comes with a User model that is needed by almost all tests
a ``UserFactory`` is useful for all Django projects.

Usage
-----

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
