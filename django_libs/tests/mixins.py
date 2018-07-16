"""
Generally useful mixins for view tests (integration tests) of any project.

"""
import sys

from django.conf import settings

from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import Http404
from django.test import RequestFactory

try:  # django <= 1.6
    from django.core.urlresolvers import resolve, reverse
except ImportError:  # >= django 1.7
    from django.urls import resolve, reverse


class ViewTestMixin(object):
    """Mixin that provides commonly tested assertions."""
    longMessage = True

    def _check_callable(self,
                        method='get',
                        data=None,
                        message=None,
                        kwargs=None,
                        user=None,
                        anonymous=False,
                        and_redirects_to=None,
                        status_code=None,
                        called_by='is_callable',
                        ajax=False,
                        no_redirect=False,
                        extra=None):
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
        if extra is None:
            extra = {}
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
                ' future.\n')

        # assertions
        if and_redirects_to:
            self.assertRedirects(
                resp,
                and_redirects_to,
                status_code=status_code,
                msg_prefix=('The view did not redirect as expected.'))

        else:
            self.assertIn(
                resp.status_code, [status_code, 302],
                msg=(message or
                     'The view should{0} be callable'.format(message_addin)))

        return resp

    def is_callable(self,
                    method='get',
                    data=None,
                    message=None,
                    kwargs=None,
                    user=None,
                    anonymous=False,
                    and_redirects_to=None,
                    status_code=None,
                    ajax=False,
                    no_redirect=False,
                    extra=None):
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
        return self._check_callable(
            method=method,
            data=data,
            message=message,
            kwargs=kwargs,
            user=user,
            anonymous=anonymous,
            and_redirects_to=and_redirects_to,
            status_code=status_code,
            ajax=ajax,
            no_redirect=no_redirect,
            called_by='is_callable',
            extra=extra)

    def is_not_callable(self,
                        method='get',
                        message=None,
                        data=None,
                        kwargs=None,
                        user=None,
                        anonymous=False,
                        and_redirects_to=None,
                        status_code=None,
                        ajax=False,
                        no_redirect=False,
                        extra=None):
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
        :extra: Additional parameters to be passed to the client GET/POST. For
            example, follow = True if you want the client to follow redirects.

        If no arguments are given, it makes the assertion according to the
        current test situation.

        """
        return self._check_callable(
            method=method,
            data=data,
            message=message,
            kwargs=kwargs,
            user=user,
            anonymous=anonymous,
            and_redirects_to=and_redirects_to,
            status_code=status_code,
            ajax=ajax,
            no_redirect=no_redirect,
            called_by='is_not_callable',
            extra=extra)

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
        Returns the URL when testing the redirect for anonymous users to the
        login page.
        Can be overwritten if you do not use the auth_login as default or
        configure your urls.py file in a specific way.
        """
        login_url = getattr(settings, 'LOGIN_URL')
        if login_url is None:
            return reverse('auth_login')
        return login_url

    def should_redirect_to_login_when_anonymous(self, url=None):
        """
        Tests if the view redirects to login when the user is anonymous.

        :param url: A string representing the URL to be called. If ``None``,
          the return value of ``get_url()`` will be used.

        """
        if not url:
            url = self.get_url()
        resp = self.client.get(url)
        self.assertRedirects(resp, '{0}?next={1}'.format(
            self.get_login_url(), url))
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
        user_no_permissions = AnonymousUser()
        self.login(user_no_permissions)
        resp = self.client.get(url, data=self.get_data_payload())
        self.assertRedirects(resp, '{0}?next={1}'.format(
            reverse('auth_login'), url))

        self.login(user)
        resp = self.client.get(url, data=self.get_data_payload())
        self.assertEqual(resp.status_code, 200)


class ViewRequestFactoryTestMixin(object):
    longMessage = True
    _logged_in_user = None
    view_class = None

    def assertRedirects(self, resp, redirect_url, msg=None):
        """
        Overrides the method that comes with Django's TestCase.

        This is necessary because the original method relies on self.client
        which we are not using here.

        """
        self.assertIn(
            resp.status_code, [301, 302], msg=msg or ('Should redirect'))
        self.assertEqual(
            resp._headers['location'][1],
            redirect_url,
            msg=msg or ('Should redirect to correct url.'))

    def get_request(self,
                    method=RequestFactory().get,
                    ajax=False,
                    no_redirect=False,
                    data=None,
                    user=AnonymousUser(),
                    add_session=False,
                    session_dict={},
                    view_kwargs=None,
                    **kwargs):
        if data is not None:
            kwargs.update({'data': data})
        req = method(self.get_url(view_kwargs=view_kwargs), **kwargs)
        req.user = user
        req._dont_enforce_csrf_checks = True
        # the messages framework only works with the FallbackStorage in case of
        # requestfactory tests
        if add_session:
            middleware = SessionMiddleware()
            middleware.process_request(req)
            req.session.save()
        else:
            setattr(req, 'session', {})
        if session_dict:
            for var in session_dict:
                req.session[var] = session_dict[var]
        messages = FallbackStorage(req)
        setattr(req, '_messages', messages)
        if ajax:
            req.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        req = self.setUpRequest(req)
        if req is None:
            raise RuntimeError(
                'The request has become None. You probably forgot to return'
                ' the request again, when implementing `setUpRequest`.')
        return req

    def get_get_request(self,
                        ajax=False,
                        no_redirect=False,
                        data=None,
                        user=None,
                        add_session=False,
                        session_dict={},
                        view_kwargs=None,
                        **kwargs):
        if user is None:
            user = self.get_user()
        return self.get_request(
            ajax=ajax,
            no_redirect=no_redirect,
            data=data,
            user=user,
            add_session=add_session,
            session_dict=session_dict,
            view_kwargs=view_kwargs,
            **kwargs)

    def get_post_request(self,
                         ajax=False,
                         no_redirect=False,
                         data=None,
                         user=None,
                         add_session=False,
                         session_dict={},
                         **kwargs):
        method = RequestFactory().post
        if user is None:
            user = self.get_user()
        return self.get_request(
            method=method,
            ajax=ajax,
            no_redirect=no_redirect,
            data=data,
            user=user,
            add_session=add_session,
            session_dict=session_dict,
            **kwargs)

    def get_user(self):
        if self._logged_in_user is None:
            return AnonymousUser()
        return self._logged_in_user

    def get_login_url(self):
        """
        Returns the URL when testing the redirect for anonymous users to the
        login page.

        Can be overwritten if you do not use the auth_login as default or
        configure your urls.py file in a specific way.

        """
        login_url = getattr(settings, 'LOGIN_URL', None)
        if login_url is None:
            return reverse('auth_login')
        return login_url

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
        raise NotImplementedError

    def get_view_args(self):
        """
        Returns a list representing the view's args, if necessary.

        If the URL of this view is constructed via args, you can override this
        method and return the proper args for the test.

        """
        return ()

    def get_view_kwargs(self):
        """
        Returns a dictionary representing the view's kwargs, if necessary.

        If the URL of this view is constructed via kwargs, you can override
        this method and return the proper args for the test.

        """
        return {}

    def get_url(self, view_kwargs=None):
        """
        Returns the url to be used in the request factory.

        Going the "old" way of implementing `get_view_name` is entirely
        optional. If you just leave it out, the url will fall back to '/'.

        """
        try:
            view_name = self.get_view_name()
        except NotImplementedError:
            # if the above is not implemented, we don't need the exact view, or
            # just don't care and return '/', which in most cases is enough
            return '/'
        view_args = self.get_view_args()
        view_kwargs = view_kwargs or self.get_view_kwargs()
        return reverse(view_name, args=view_args, kwargs=view_kwargs)

    def get_view_class(self):
        """Returns the view class."""
        return self.view_class

    def get_view(self):
        """Returns the view ``.as_view()``"""
        view_class = self.get_view_class()
        if view_class is None:
            if hasattr(self, 'view') and self.view:
                return self.view
            raise NotImplementedError('You need to define a view class.')
        return view_class.as_view()

    def get(self,
            user=None,
            data=None,
            ajax=False,
            no_redirect=False,
            add_session=False,
            session_dict={},
            kwargs=None):
        """Creates a response from a GET request."""
        req = self.get_get_request(
            user=user,
            data=data,
            ajax=ajax,
            no_redirect=no_redirect,
            add_session=add_session,
            session_dict=session_dict,
            view_kwargs=kwargs)
        view = self.get_view()
        if kwargs is None:
            kwargs = {}
            kwargs.update(self.get_view_kwargs())
        args = self.get_view_args()
        resp = view(req, *args, **kwargs)
        return resp

    def post(self,
             user=None,
             data=None,
             ajax=False,
             no_redirect=False,
             add_session=False,
             session_dict={},
             kwargs=None):
        """Creates a response from a POST request."""
        req = self.get_post_request(
            user=user,
            data=data,
            ajax=ajax,
            no_redirect=no_redirect,
            session_dict=session_dict,
            add_session=add_session)
        view = self.get_view()
        if kwargs is None:
            kwargs = {}
            kwargs.update(self.get_view_kwargs())
        args = self.get_view_args()
        resp = view(req, *args, **kwargs)
        return resp

    def login(self, user):
        """Sets the user as permanently logged in for all tests."""
        self._logged_in_user = user

    def logout(self):
        """'Logs out' the currently set default user."""
        self._logged_in_user = None

    def assert200(self, resp, user=None, msg=None):
        """Asserts if a response has returnd a status code of 200."""
        user_msg = user or self.get_user()
        if self.get_view_class() is not None:
            # if it's a view class, we can append it to the message as class
            # name
            view_msg = self.get_view_class()
        else:
            # if no view class is set, we assume function based view
            view_msg = self.get_view()
        if msg is None:
            msg = ('The `{0}` view should have been callable for'
                   ' user `{1}`.').format(view_msg, user_msg)
            if resp.status_code in [301, 302]:
                msg = msg + ' The view redirected to "{0}".'.format(resp.url)
        self.assertEqual(resp.status_code, 200, msg=msg)
        return resp

    def is_callable(self,
                    user=None,
                    data=None,
                    ajax=False,
                    no_redirect=False,
                    add_session=False,
                    session_dict={},
                    kwargs=None,
                    msg=None):
        """Checks if the view can be called view GET."""
        resp = self.get(
            user=user,
            data=data,
            ajax=ajax,
            no_redirect=no_redirect,
            add_session=add_session,
            session_dict=session_dict,
            kwargs=kwargs)
        self.assert200(resp, user, msg=msg)
        return resp

    def is_forbidden(self,
                     user=None,
                     data=None,
                     ajax=False,
                     no_redirect=False,
                     add_session=False,
                     post=False,
                     kwargs=None,
                     msg=None):
        """Checks if the view is not allowed to be called."""
        resp = self.get(
            user=user,
            data=data,
            ajax=ajax,
            no_redirect=no_redirect,
            add_session=add_session,
            kwargs=kwargs)
        user_msg = user or self.get_user()
        if self.get_view_class() is not None:
            # if it's a view class, we can append it to the message as class
            # name
            view_msg = self.get_view_class()
        else:
            # if no view class is set, we assume function based view
            view_msg = self.get_view()
        if not msg:
            msg = ('The `{0}` view should have been forbidden for'
                   ' user `{1}`.').format(view_msg, user_msg)
        self.assertEqual(resp.status_code, 403, msg=msg)
        return resp

    def is_not_callable(self,
                        user=None,
                        data=None,
                        ajax=False,
                        no_redirect=False,
                        add_session=False,
                        session_dict={},
                        post=False,
                        kwargs=None,
                        msg=None):
        """Checks if the view can not be called."""
        if post:
            call_obj = self.post
        else:
            call_obj = self.get
        self.assertRaises(
            Http404,
            call_obj,
            user=user,
            data=data,
            ajax=ajax,
            no_redirect=no_redirect,
            add_session=add_session,
            session_dict=session_dict,
            kwargs=kwargs)

    def is_postable(self,
                    user=None,
                    data=None,
                    ajax=False,
                    no_redirect=False,
                    to=None,
                    to_url_name=None,
                    next_url='',
                    add_session=False,
                    session_dict={},
                    kwargs=None,
                    msg=None):
        """Checks if the view handles POST correctly."""
        resp = self.post(
            user=user,
            data=data,
            add_session=add_session,
            session_dict=session_dict,
            kwargs=kwargs,
            ajax=ajax,
            no_redirect=no_redirect)
        if not (ajax or no_redirect) or to or to_url_name:
            if next_url:
                next_url = '?next={0}'.format(next_url)
            if to_url_name:
                try:
                    self.assertEqual(
                        resolve(resp.url).url_name, to_url_name, msg=msg)
                except AttributeError:
                    raise AssertionError(
                        'The response returned with a status code {}'.format(
                            resp.status_code))
            else:
                redirect_url = '{0}{1}'.format(to, next_url)
                self.assertRedirects(resp, redirect_url, msg=msg)
        else:
            self.assert200(resp, user, msg=msg)
        return resp

    def redirects(self,
                  to=None,
                  to_url_name=None,
                  next_url='',
                  user=None,
                  add_session=False,
                  session_dict={},
                  kwargs=None,
                  msg=None,
                  data=None):
        """Checks for redirects from a GET request."""
        resp = self.get(
            user=user,
            add_session=add_session,
            kwargs=kwargs,
            session_dict=session_dict,
            data=data)
        if to or to_url_name:
            if next_url:
                next_url = '?next={0}'.format(next_url)
            if to_url_name:
                if msg is None:
                    msg = (
                        'Should redirect to correct to view with correct name.'
                    )
                self.assertEqual(
                    resolve(resp.url).url_name, to_url_name, msg=msg)
            else:
                redirect_url = '{0}{1}'.format(to, next_url)
                self.assertRedirects(resp, redirect_url, msg=msg)
        return resp

    def setUpRequest(self, request):
        """
        The request is passed through this method on each run to allow
        adding additional attributes to it or change certain values.

        """
        return request

    def should_redirect_to_login_when_anonymous(self, add_session=False):
        resp = self.redirects(
            to=self.get_login_url(),
            next_url=self.get_url(),
            add_session=add_session)
        return resp
