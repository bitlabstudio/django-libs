import os
from setuptools import setup, find_packages
import django_libs


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''


setup(
    name="django-libs",
    version=django_libs.__version__,
    description=read('DESCRIPTION'),
    long_description=read('README.rst'),
    license='The MIT License',
    platforms=['OS Independent'],
    keywords='django, common, reusable, kickstart',
    author='Martin Brochhaus',
    author_email='mbrochh@gmail.com',
    url="https://github.com/bitmazk/django-libs",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'factory_boy>2.0.0',
        'beautifulsoup4>4.0.0',
        'Pillow',
    ]
)
