Decorators
==========

lockfile
--------

Very useful for custom admin commands. I your command is scheduled every minute
but might take longer than one minute, it would be good to prevent execution
of the command if the preceeding execution is still running. Lockfiles come
in handy here.

You should create a setting ``LOCKFILE_PATH`` which points to
``/home/username/tmp/``.

Usage::

    from django_libs.decorators import lockfile
    ...

    LOCKFILE = os.path.join(
        settings.LOCKFILE_FOLDER, 'command_name')

    class Command(BaseCommand):

        @lockfile(LOCKFILE)
        def handle(self, *args, **kwargs):
            ...
