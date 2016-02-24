"""URLs to run the tests."""
from django.conf.urls import include, url
from django.contrib import admin
from django.http import HttpResponse

admin.autodiscover()


urlpatterns = [
    url(r'^index/test/$', lambda x: HttpResponse('Success'), name='index'),
    url(r'^admin-.+/', include(admin.site.urls)),
    url(r'^', include('django_libs.tests.test_app.urls')),
]
