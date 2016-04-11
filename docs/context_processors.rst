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
        ...
        'django_libs.context_processors.analytics',
    )

Use it in your template::

    <script>
      (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
      (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
      m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
      })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

      ga('create', '{{ ANALYTICS_TRACKING_ID }}', '{{ ANALYTICS_DOMAIN }}');
      ga('send', 'pageview');
    </script>
