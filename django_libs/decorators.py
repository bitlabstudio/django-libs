"""Useful decorators for Django projects."""
from functools import wraps
import re

from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from lockfile import FileLock, AlreadyLocked, LockTimeout


def lockfile(lockfile_name, lock_wait_timeout=-1):
    """
    Only runs the method if the lockfile is not acquired.

    You should create a setting ``LOCKFILE_PATH`` which points to
    ``/home/username/tmp/``.

    In your management command, use it like so::

        LOCKFILE = os.path.join(
            settings.LOCKFILE_FOLDER, 'command_name')

        class Command(NoArgsCommand):
            @lockfile(LOCKFILE)
            def handle_noargs(self, **options):
                # your command here

    :lockfile_name: A unique name for a lockfile that belongs to the wrapped
      method.
    :lock_wait_timeout: Seconds to wait if lockfile is acquired. If ``-1`` we
      will not wait and just quit.

    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            lock = FileLock(lockfile_name)
            try:
                lock.acquire(lock_wait_timeout)
            except AlreadyLocked:
                return
            except LockTimeout:
                return
            try:
                result = func(*args, **kwargs)
            finally:
                lock.release()
            return result

        return wrapper
    return decorator


def get_username(identifier):
    """Checks if a string is a email adress or not."""
    pattern = re.compile('.+@\w+\..+')
    if pattern.match(identifier):
        try:
            user = User.objects.get(email=identifier)
        except:
            raise Http404
        else:
            return user.username
    else:
        return identifier


def http_auth(func):
    @wraps(func)
    def _decorator(request, *args, **kwargs):
        """Decorator to handle http authorizations."""
        is_authenticated = request.user.is_authenticated
        authenticated = is_authenticated if isinstance(is_authenticated, bool)\
            else is_authenticated()
        if authenticated:
            return func(request, *args, **kwargs)
        if 'HTTP_AUTHORIZATION' in request.META.keys():
            authmeth, auth = request.META['HTTP_AUTHORIZATION'].split(' ', 1)
            if authmeth.lower() == 'basic':
                auth = auth.strip().decode('base64')
                identifier, password = auth.split(':', 1)
                username = get_username(identifier)
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    return func(request, *args, **kwargs)
        raise Http404
    return _decorator
