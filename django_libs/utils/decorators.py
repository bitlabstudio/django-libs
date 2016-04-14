"""Useful decorators."""


class conditional_decorator(object):
    """
    Allows you to use decorators based on a condition.

    Useful to require login only if a setting is set::

        @conditional_decorator(method_decorator(login_required), settings.FOO)
        def dispatch(self, request, *args, **kwargs):
            return super(...).dispatch(...)

    """
    def __init__(self, dec, condition):
        self.decorator = dec
        self.condition = condition

    def __call__(self, func):
        if not self.condition:
            # Return the function unchanged, not decorated.
            return func
        return self.decorator(func)
