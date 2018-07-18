"""Views for testing 404 and 500 templates."""
import json
import datetime
import math
from functools import update_wrapper

from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
try:
    from django_comments.models import Comment
except ImportError:
    pass
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.template import loader, Context
from django.views.generic import TemplateView, View

from . import default_settings


class Http404TestView(TemplateView):
    """
    WARNING: This view is deprecated. Use the ``RapidPrototypingView`` instead.

    """
    template_name = '404.html'


class Http500TestView(TemplateView):
    """
    WARNING: This view is deprecated. Use the ``RapidPrototypingView`` instead.

    """
    template_name = '500.html'


class HybridView(View):
    """
    View that renders different views depending on wether the user is authed.

    If the user is authenticated, it will render ``authed_view``, otherwise
    it will render ``anonymous_view``.

    If you are passing in a function based view you can also define
    ``authed_view_kwargs`` and ``anonymous_view_kwargs`` which, of course,
    should be dictionaries.

    """
    authed_view = None
    authed_view_kwargs = None
    anonymous_view = None
    anonymous_view_kwargs = None

    @classmethod
    def as_view(cls, **initkwargs):
        """
        Main entry point for a request-response process.
        """
        # sanitize keyword arguments
        for key in initkwargs:
            if key in cls.http_method_names:
                raise TypeError("You tried to pass in the %s method name as a "
                                "keyword argument to %s(). Don't do that."
                                % (key, cls.__name__))
            if not hasattr(cls, key):
                raise TypeError("%s() received an invalid keyword %r. as_view "
                                "only accepts arguments that are already "
                                "attributes of the class." % (
                                    cls.__name__, key))

        def view(request, *args, **kwargs):
            self = cls(**initkwargs)
            if hasattr(self, 'get') and not hasattr(self, 'head'):
                self.head = self.get
            self.request = request
            self.args = args
            self.kwargs = kwargs
            self.authed_view = initkwargs.get('authed_view')
            self.authed_view_kwargs = initkwargs.get('authed_view_kwargs')
            self.anonymous_view = initkwargs.get('anonymous_view')
            self.anonymous_view_kwargs = initkwargs.get(
                'anonymous_view_kwargs')
            return self.dispatch(request, *args, **kwargs)
        # take name and docstring from class
        update_wrapper(view, cls, updated=())
        # and possible attributes set by decorators
        # like csrf_exempt from dispatch
        update_wrapper(view, cls.dispatch, assigned=())
        return view

    def dispatch(self, request, *args, **kwargs):
        is_authenticated = request.user.is_authenticated
        authenticated = is_authenticated if isinstance(is_authenticated, bool)\
            else is_authenticated()
        if authenticated:
            view_kwargs = self.authed_view_kwargs or {}
            return self.authed_view(request, **view_kwargs)

        view_kwargs = self.anonymous_view_kwargs or {}
        return self.anonymous_view(request, **view_kwargs)


class PaginatedCommentAJAXView(TemplateView):
    """Returns a page of comments for an object."""
    template_name = 'django_libs/partials/ajax_comments.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404

        self.comments = Comment.objects.filter(
            content_type__name=request.GET.get('ctype'),
            object_pk=request.GET.get('object_pk'))
        return super(PaginatedCommentAJAXView, self).dispatch(
            request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        template = loader.get_template(self.template_name)
        content = template.render(Context(self.get_context_data()))
        return HttpResponse(json.dumps({
            'data': content, 'page': self.page,
            'has_prev': self.page_obj.has_previous(),
            'has_next': self.page_obj.has_next()}),
            content_type="application/json")

    def get_context_data(self):
        ctx = super(PaginatedCommentAJAXView, self).get_context_data()

        # Let's try to figure out if a special comment was requested
        page = None
        comment_pk = self.request.GET.get('comment_pk')
        if comment_pk:
            try:
                self.comment = Comment.objects.get(
                    pk=comment_pk, is_public=True, is_removed=False)
            except Comment.DoesNotExist:
                self.comment = None
            if self.comment:
                index = 1
                for item in self.comments:
                    if item == self.comment:
                        # The special comment is indeed part of all comments,
                        # so let's calculate the page it should be on
                        page = math.ceil(
                            float(index) /
                            default_settings.COMMENTS_PAGINATE_BY)
                    index += 1

        if page:
            # If we had found a special comment, we ignore the ?page param
            # and jump to that comment's page instead
            self.page = page
        else:
            self.page = self.request.GET.get('page')

        # Now we know which page we want to show and we can start the paginator
        self.paginator = Paginator(
            self.comments, default_settings.COMMENTS_PAGINATE_BY)
        try:
            self.page_obj = self.paginator.page(self.page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            self.page_obj = self.paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999),
            # deliver last page of results.
            self.page_obj = self.paginator.page(self.paginator.num_pages)

        ctx.update({
            'comments': self.comments,
            'paginator': self.paginator,
            'page_obj': self.page_obj,
        })
        return ctx


class RapidPrototypingView(TemplateView):
    """
    View that can render any given template.

    This can be useful when you want your designers to be bale to go ahead and
    create templates although no views have been created for those templates,
    yet.

    """
    def dispatch(self, request, *args, **kwargs):
        self.template_name = kwargs.get('template_path')
        return super(RapidPrototypingView, self).dispatch(request, *args,
                                                          **kwargs)


class UpdateSessionAJAXView(View):
    """View to update a session variable in an AJAX post."""
    def dispatch(self, request, *args, **kwargs):
        if not (request.is_ajax() and request.method == 'POST'):
            return HttpResponseForbidden()
        if (request.POST.get('session_name') and request.POST.get(
                'session_value')):
            request.session[request.POST['session_name']] = request.POST[
                'session_value']
        return HttpResponse('done')


class UpdateCookieAJAXView(View):
    """View to update a cookie in an AJAX post."""
    def dispatch(self, request, *args, **kwargs):
        if not (request.is_ajax() and request.method == 'POST'):
            return HttpResponseForbidden()
        response = HttpResponse('done')
        days = int(request.POST.get('cookie_days', 100))
        date = datetime.datetime.utcnow() + datetime.timedelta(days=days)
        expires = datetime.datetime.strftime(date, "%a, %d-%b-%Y %H:%M:%S GMT")
        response.set_cookie(
            request.POST['cookie_key'],
            request.POST['cookie_value'],
            max_age=(days * 24 * 60 * 60),
            expires=expires,
            domain=settings.SESSION_COOKIE_DOMAIN,
            secure=settings.SESSION_COOKIE_SECURE or None,
        )
        return response
