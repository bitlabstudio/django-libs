"""
Generally useful mixins for view tests (integration tests) of any project.

"""
from django.core.urlresolvers import reverse

from django_libs.tests.factories import UserFactory


class ViewTestMixin(object):
    """Mixin that provides commonly tested assertions."""

    def is_callable(self, method='get', data=None, message=None, kwargs=None,
                    user=None, anonymous=False):
        """
        A shortcut for an assertion on status code 200 or 302.

        :method: 'get' or 'post'. Default is 'get'.
        :data: Post data or get data payload.
        :message: Lets you override the assertion message.
        :kwargs: Lets you override the view kwargs.
        :user: If user argument is given, it logs it in first.
        :anonymous: If True, it logs out the user first. Default is False

        If no arguments are given, it makes the assertion according to the
        current test situation.

        """
        if user:
            self.login(user)
        if anonymous:
            self.client.logout()
        if method.lower() == 'get':
            resp = self.client.get(
                self.get_url(view_kwargs=kwargs or self.get_view_kwargs()),
                data=data or self.get_data_payload()
            )
            self.assertEqual(resp.status_code, 200, msg=(
                message or
                'If called with the correct data, the view should be callable.'
                ' Got status code of {0}'.format(resp.status_code)))
        elif method.lower() == 'post':
            resp = self.client.post(
                self.get_url(view_kwargs=kwargs or self.get_view_kwargs()),
                data=data or self.get_data_payload()
            )
            self.assertEqual(resp.status_code, 302, msg=(
                message or
                'If posted with the correct data, the view should be callable.'
                ' Got status code of {0}'.format(resp.status_code)))
        else:
            raise Exception('Not a valid request method: "{0}"'.format(method))
        return resp

    def is_not_callable(self, method='get', message=None, data=None,
                        kwargs=None, user=None, anonymous=False):
        """
        A shortcut for a common assertion on a 404 status code.

        :method: 'get' or 'post'. Default is 'get'.
        :message: The message to display if the assertion fails
        :data: Get data payload or post data.
        :kwargs: View kwargs can be overridden. This is e.g. necessary if
            you call is_not_callable for a deleted object, where the object.pk
            was assigned in get_view_kwargs.
        :user: If a user is given, it logs it in first.
        :anonymous: If True, it logs out the user first. Default is False

        If no arguments are given, it makes the assertion according to the
        current test situation.

        """
        if user:
            self.login(user)
        if anonymous:
            self.client.logout()
        if method.lower() == 'get':
            resp = self.client.get(
                self.get_url(view_kwargs=kwargs or self.get_view_kwargs()),
                data=data or self.get_data_payload()
            )
        elif method.lower() == 'post':
            resp = self.client.post(
                self.get_url(view_kwargs=kwargs or self.get_view_kwargs()),
                data=data or self.get_data_payload()
            )
        else:
            raise Exception('Not a valid request method: "{0}"'.format(method))
        self.assertEqual(resp.status_code, 404, msg=(
            message or
            'If called with the wrong data, the view should not be callable'
            ' Got status code of {0}'.format(resp.status_code)))
        return resp

    def get_data_payload(self):
        """
        Returns a dictionairy providing GET data payload sent to the view.

        If the view expects request.GET data to include this, you can override
        this method and return the proper data for the test.

        """
        if hasattr(self, 'data_payload'):
            return self.data_payload
        return {}

    def get_view_name(self):
        """
        Returns a string representing the view name as set in the ``urls.py``.

        You must implement this when inheriting this mixin. If your ``urls.py``
        looks like this::

            ...
            url(r'^$', HomeView.as_view(), name='home_view'

        Then you should simply return::

            return 'home_view'

        """
        return NotImplementedError

    def get_view_args(self):
        """
        Returns a list representing the view's args, if necessary.

        If the URL of this view is constructed via args, you can override this
        method and return the proper args for the test.

        """
        return None

    def get_view_kwargs(self):
        """
        Returns a dictionary representing the view's kwargs, if necessary.

        If the URL of this view is constructed via kwargs, you can override
        this method and return the proper args for the test.

        """
        return None

    def get_url(self, view_name=None, view_args=None, view_kwargs=None):
        """
        Returns the url to be consumed by ``self.client.get``.

        When calling ``self.client.get`` we usually need three parameter:

            * The URL, which we construct from the view name using ``reverse``
            * The args
            * The kwargs

        In most cases ``args`` and ``kwargs`` are ``None``, so this method will
        help to return the proper URL by calling instance methods that can
        be overridden where necessary.

        :param view_name: A string representing the view name. If ``None``,
          the return value of ``get_view_name()`` will be used.
        :param view_args: A list representing the view args. If ``None``,
          the return value of ``get_view_args()`` will be used.
        :param view_kwargs: A dict representing the view kwargs. If ``None``,
          the return value of ``get_view_kwargs()`` will be used.

        """
        if view_name is None:
            view_name = self.get_view_name()
        if view_args is None:
            view_args = self.get_view_args()
        if view_kwargs is None:
            view_kwargs = self.get_view_kwargs()
        return reverse(view_name, args=view_args, kwargs=view_kwargs)

    def login(self, user, password='test123'):
        """
        Performs a login for the given user.

        By convention we always use ``test123`` in our test fixutres. When you
        create your users with the UserFactory, that password will be set by
        default.

        If you must you can provide a password to this method in order to
        override the ``test123`` default.

        :param user: A ``User`` instance.
        :param password: A string if you want to login with another password
          than 'test123'.

        """
        self.client.login(username=user.username, password=password)

    def should_redirect_to_login_when_anonymous(self, url=None):
        """
        Tests if the view redirects to login when the user is anonymous.

        :param url: A string representing the URL to be called. If ``None``,
          the return value of ``get_url()`` will be used.

        """
        if not url:
            url = self.get_url()
        resp = self.client.get(url)
        self.assertRedirects(resp,
            '{0}?next={1}'.format(reverse('auth_login'), url))
        return resp

    def should_be_callable_when_anonymous(self, url=None):
        """
        Tests if the view returns 200 when the user is anonymous.

        :param url: A string representing the URL to be called. If ``None``,
          the return value of ``get_url()`` will be used.

        """
        if not url:
            url = self.get_url()
        resp = self.client.get(url, data=self.get_data_payload())
        self.assertEqual(resp.status_code, 200)
        return resp

    def should_be_callable_when_authenticated(self, user, url=None):
        """
        Tests if the view returns 200 when the user is logged in.

        :param user: A ``User`` instance.
        :param url: A string representing the URL to be called. If ``None``,
          the return value of ``get_url()`` will be used.

        """
        if not url:
            url = self.get_url()
        self.login(user)
        resp = self.client.get(url, data=self.get_data_payload())
        self.assertEqual(resp.status_code, 200)
        return resp

    def should_be_callable_when_has_correct_permissions(self, user, url=None):
        """
        Tests if the view returns 200 when the user has permissions.

        Also tests if the view redirects to login if the user is logged in but
        does not have the correct permissions.

        :param user: A ``User`` instance that has the correct permissions.
        :param url: A string representing the URL to be called. If ``None``,
          the return value of ``get_url()`` will be used.

        """
        if not url:
            url = self.get_url()
        user_no_permissions = UserFactory()
        self.login(user_no_permissions)
        resp = self.client.get(url, data=self.get_data_payload())
        self.assertRedirects(resp,
            '{0}?next={1}'.format(reverse('auth_login'), url))

        self.login(user)
        resp = self.client.get(url, data=self.get_data_payload())
        self.assertEqual(resp.status_code, 200)
