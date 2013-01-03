"""Useful decorators for Django projects."""
import functools
from lockfile import FileLock, AlreadyLocked, LockTimeout


def lockfile(lockfile_name, lock_wait_timeout=-1):
    """
    Only runs the method if the lockfile is not acquired.

    :lockfile_name: A unique name for a lockfile that belongs to the wrapped
      method.
    :lock_wait_timeout: Seconds to wait if lockfile is acquired. If ``-1`` we
      will not wait and just quit.

    """
    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            lock = FileLock(lockfile_name)
            try:
                lock.acquire(lock_wait_timeout)
            except AlreadyLocked:
                return
            except LockTimeout:
                return
            result = func(*args, **kwargs)
            lock.release()
            return result

        return wrapper
    return decorator
