Decorators
==========

lockfile
--------

Very useful for custom admin commands. If your command is scheduled every minute
but might take longer than one minute, it would be good to prevent execution
of the command if the preceeding execution is still running. Lockfiles come
in handy here.

Note: This decorator requires the ``lockfile`` package to be installed.
Either add it to your requirements if not already in or to get the latest
version from pypi do:

.. code-block:: bash

    pip install lockfile



You should create a setting ``LOCKFILE_PATH`` which points to
``/home/username/tmp/``.

Usage::

    from django_libs.utils.decorators import lockfile
    ...

    LOCKFILE = os.path.join(
        settings.LOCKFILE_PATH, 'command_name')

    class Command(BaseCommand):

        @lockfile(LOCKFILE)
        def handle(self, *args, **kwargs):
            ...
