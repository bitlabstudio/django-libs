Storage support
===============

Amazon S3
---------

If you want to store your media files in an Amazon S3 bucket we provide some
helpful files for you.

First of all, setup your Amazon stuff. This article will help you out:

    http://martinbrochhaus.com/s3.html

Then install ``django-storages`` (http://django-storages.readthedocs.org/) and
``boto`` (https://github.com/boto/boto). Add the following code to your
``local_settings.py``::

    USE_S3 = False
    AWS_ACCESS_KEY = 'XXXX'
    AWS_SECRET_ACCESS_KEY = 'XXXX'
    AWS_STORAGE_BUCKET_NAME = 'bucketname'
    AWS_QUERYSTRING_AUTH = False
    S3_URL = 'https://%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

    if USE_S3:
        DEFAULT_FILE_STORAGE = 'django_libs.s3.MediaRootS3BotoStorage'
        THUMBNAIL_DEFAULT_STORAGE = DEFAULT_FILE_STORAGE
        MEDIA_URL = S3_URL + '/media/'

        # Add this line, if you're using ``django-compressor``
        COMPRESS_STORAGE = 'django_libs.s3.CompressorS3BotoStorage'

    MEDIA_ROOT = os.path.join(PROJECT_ROOT, '../..',  'media')
    STATIC_ROOT = os.path.join(PROJECT_ROOT, '../..', 'static')

Test the upload. If you get a ``NoAuthHandlerFound`` exception, add the
following lines to ``$HOME/.boto``::

    [Credentials]
    aws_access_key_id = XXXX
    aws_secret_access_key = XXXX

If you're using ``django-compressor`` add the following settings::

    COMPRESS_PARSER = 'compressor.parser.HtmlParser'
    COMPRESS_CSS_FILTERS = [
        'django_libs.compress_filters.S3CssAbsoluteFilter',
    ]
    COMPRESS_ENABLED = True

Make sure to run ``./manage.py compress --force`` on every deployment. Also
check::

    http://martinbrochhaus.com/compressor.html
