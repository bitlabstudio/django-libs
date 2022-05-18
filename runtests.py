#!/usr/bin/env python
"""
This script is used to run tests, create a coverage report and output the
statistics at the end of the tox run.
To run this script just execute ``tox``
"""
import re

from fabric.api import local, warn
from fabric.colors import green, red


if __name__ == '__main__':
    # Kept some files for backwards compatibility. If support is dropped,
    # remove it here
    deprecated_files = '*utils_email*,*utils_log*'

    local('flake8 --statistics .')
    local('coverage run --source="django_libs" manage.py test -v 2'
          ' --traceback --failfast --settings=django_libs.tests.settings'
          ' --pattern="*_tests.py"')
    local('coverage html -d coverage'
          ' --omit="*__init__*,*/settings/*,*/migrations/*,*/tests/*,'
          '*admin*,{}"'.format(deprecated_files))
    total_line = local('grep -n pc_cov coverage/index.html', capture=True)
    percentage = float(re.findall(r'(\d+)%', total_line)[-1])
    if percentage < 100:
        warn(red('Coverage is {0}%'.format(percentage)))
    else:
        print(green('Coverage is {0}%'.format(percentage)))
