Utils
=====

conditional_decorator
---------------------

Allows you to decorate a function based on a condition.

This can be useful if you want to require login for a view only if a certain
setting is set::

    from django.conf import settings
    from django.contrib.auth.decorators import login_required
    from django.utils.decorators import method_decorator
    from django_libs.utils import conditional_decorator
    class MyView(ListView):
        @conditional_decorator(method_decorator(login_required), settings.LOGIN_REQUIRED)
        def dispatch(self, request, *args, **kwargs):
            return super(MyView, self).dispatch(request, *args, **kwargs)
