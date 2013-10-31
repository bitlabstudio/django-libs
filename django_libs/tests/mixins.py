"""
Generally useful mixins for view tests (integration tests) of any project.

"""
import sys

from django.core.urlresolvers import reverse

from django_libs.tests.factories import UserFactory


class ViewTestMixin(object):
    """Mixin that provides commonly tested assertions."""
    longMessage = True

    def _check_callable(self, method='get', data=None, message=None,
                        kwargs=None, user=None, anonymous=False,
                        and_redirects_to=None, status_code=None,
                        called_by='is_callable', ajax=False, extra={}):
        """
        The method that does the actual assertions for ``is_callable`` and
        ``is_not_callable``.

        :method: 'get' or 'post'. Default is 'get'.
        :data: Post data or get data payload.
        :message: Lets you override the assertion message.
        :kwargs: Lets you override the view kwargs.
        :user: If user argument is given, it logs it in first.
        :anonymous: If True, it logs out the user first. Default is False
        :and_redirects_to: If set, it additionally makes an assertRedirect on
            whatever string is given. This can be either a relative url or a
            name.
        :status_code: Overrides the expected status code. Default is 200.
            Can either be a list of status codes or a single integer.
        :called_by: A string that is either 'is_callable' or 'is_not_callable'.
        :extra: Additional parameters to be passed to the client GET/POST. For
            example, follow = True if you want the client to follow redirects.


        """
        # Setting up defaults if not overwritten.
        if called_by == 'is_not_callable':
            message_addin = ' not'
        elif called_by == 'is_callable':
            message_addin = ''
        if user:
            self.login(user)
        if anonymous:
            self.client.logout()
        if not status_code and and_redirects_to:
            status_code = 302
        if not status_code and called_by == 'is_callable':
            status_code = 200
        if not status_code and called_by == 'is_not_callable':
            status_code = 404
        client_args = (
            self.get_url(view_kwargs=kwargs or self.get_view_kwargs()),
            data or self.get_data_payload(),
        )
        if ajax:
            extra.update({'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})

        # making the request
        if method.lower() == 'get':
            resp = self.client.get(*client_args, **extra)
        elif method.lower() == 'post':
            resp = self.client.post(*client_args, **extra)
        else:
            raise Exception('Not a valid request method: "{0}"'.format(method))

        # usage validation
        if resp.status_code == 302 and not and_redirects_to and not (
                status_code in [200, 404]):
            # TODO change the defaults and remove this warning
            sys.stderr.write(
                '\n\033[1;31mDeprecationWarning:\033[1;m'
                ' Your response status code'
                ' was 302, although ``and_redirects_to`` was not set.\n'
                'Please use ``and_redirects_to`` for a test on redirects since'
                ' the callable methods will default to 200 or 404 in the'
                ' future.\n'
            )

        # assertions
        if and_redirects_to:
            self.assertRedirects(
                resp, and_redirects_to, status_code=status_code,
                msg_prefix=('The view did not redirect as expected.'))

        else:
            self.assertIn(resp.status_code, [status_code, 302], msg=(
                message or
                'The view should{0} be callable'.format(message_addin)))

        return resp

    def is_callable(self, method='get', data=None, message=None, kwargs=None,
                    user=None, anonymous=False, and_redirects_to=None,
                    status_code=None, code=None, ajax=False, extra={}):
        """
        A shortcut for an assertion on status code 200 or 302.

        :method: 'get' or 'post'. Default is 'get'.
        :data: Post data or get data payload.
        :message: Lets you override the assertion message.
        :kwargs: Lets you override the view kwargs.
        :user: If user argument is given, it logs it in first.
        :anonymous: If True, it logs out the user first. Default is False
        :and_redirects_to: If set, it additionally makes an assertRedirect on
            whatever string is given. This can be either a relative url or a
            name.
        :status_code: Overrides the expected status code. Default is 200.
            Can either be a list of status codes or a single integer.
        :extra: Additional parameters to be passed to the client GET/POST. For
            example, follow = True if you want the client to follow redirects.

        If no arguments are given, it makes the assertion according to the
        current test situation.

        """
        if not status_code:
            status_code = code
        # TODO change the parameter and remove this warning
        if code:
            sys.stderr.write(
                '\n\033[1;31mDeprecationWarning:\033[1;m'
                ' The ``code`` parameter of ``is_(not_)callable()`` will be'
                ' changed to ``status_code`` in future versions.\n'
            )
        return self._check_callable(
            method=method, data=data, message=message, kwargs=kwargs,
            user=user, anonymous=anonymous, and_redirects_to=and_redirects_to,
            status_code=status_code, ajax=ajax, called_by='is_callable',
            extra=extra)

    def is_not_callable(self, method='get', message=None, data=None,
                        kwargs=None, user=None, anonymous=False,
                        and_redirects_to=None, status_code=None, code=None,
                        ajax=False):
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
            :status_code: Overrides the expected status code. Default is 404.
            Can either be a list of status codes or a single integer.

        If no arguments are given, it makes the assertion according to the
        current test situation.

        """
        status_code = code
        # TODO change the parameter and remove this warning
        if code:
            sys.stderr.write(
                '\n\033[1;31mDeprecationWarning:\033[1;m'
                ' The ``code`` parameter of ``is_(not_)callable()`` will be'
                ' changed to ``status_code`` in future versions.\n'
            )
        return self._check_callable(
            method=method, data=data, message=message, kwargs=kwargs,
            user=user, anonymous=anonymous, and_redirects_to=and_redirects_to,
            status_code=status_code, ajax=ajax, called_by='is_not_callable')

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

    def get_login_url(self):
        """
        Returns the URL when testing the redirect for anonymous users to the login page.
        Can be overwritten if you do not use the auth_login as default or configure your
        urls.py file in a specific way.
        """
        return reverse('auth_login')

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
                             '{0}?next={1}'.format(self.get_login_url(), url))
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
