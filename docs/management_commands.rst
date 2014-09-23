Management Commands
===================

cleanup_mailer_messagelog
-------------------------

If you want to delete old message logs of the ``mailer`` app simple use:

    ./manage.py cleanup_mailer_messagelog

You can also add the command to your cronjobs:

    0 4 * * 4 $HOME/bin/django-cleanup-mailer-messagelog.sh > $HOME/mylogs/cron/django-cleanup-mailer-messagelog.log 2>&1

Logs younger than 122 days (~4 months) will be ignored, logs older than 122
days will be deleted.
