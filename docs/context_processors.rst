Context Processors
==================

analytics
---------

Most projects have the Google Analytics tracking code in their base template.
If you like to put that code into a partial template or even re-use your whole
base template between projects, then it would be a good idea to set the
analytics code in your ``local_settings.py`` and add it to your template
context using this context processor.

Add the processor to your list of context processors::

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.tz',
        'django.contrib.messages.context_processors.messages',
        'django.core.context_processors.request',
        'django_libs.context_processors.analytics',
    )

Use it in your template::

    <script>
        var _gaq=[['_setAccount','{{ ANALYTICS_TRACKING_ID }}'],['_trackPageview']];
        (function(d,t){var g=d.createElement(t),s=d.getElementsByTagName(t)[0];
        g.src=('https:'==location.protocol?'//ssl':'//www')+'.google-analytics.com/ga.js';
        s.parentNode.insertBefore(g,s)}(document,'script'));
    </script>
