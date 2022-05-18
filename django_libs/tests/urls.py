"""URLs to run the tests."""
from django.urls import include, path
from django.contrib import admin
from django.http import HttpResponse

admin.autodiscover()


urlpatterns = [
    path('index/test/', lambda x: HttpResponse('Success'), name='index'),
    path('admin/', admin.site.urls),
    path('', include('django_libs.tests.test_app.urls')),
]
