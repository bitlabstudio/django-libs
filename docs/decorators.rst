Decorators
==========

lockfile
--------

Very useful for custom admin commands. I your command is scheduled every minute
but might take longer than one minute, it would be good to prevent execution
of the command if the preceeding execution is still running. Lockfiles come
in handy here.

Usage::

    from django_libs.decorators import lockfile
    ...

    class Command(BaseCommand):

        @lockfile('your_command_name')
        def handle(self, *args, **kwargs):
            ...
