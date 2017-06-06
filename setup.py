#!/usr/bin/env python

"""
Package setup script.

Copyright 2017 ICTU

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from builtins import str
from pip.download import PipSession
from pip.req import parse_requirements
from setuptools import setup, find_packages
from bigboat import __version__

setup(name='bigboat',
      version=__version__,
      description='BigBoat docker dashboard API',
      long_description='''Python wrapper library for the BigBoat API.
Support for v2 and the deprecated v1 is included.
This API can create, retrieve, update and delete application definitions,
do similar operations for instances and poll for status''',
      author='ICTU',
      author_email='leon.helwerda@ictu.nl',
      url='https://github.com/ICTU/bigboat-python-api',
      license='Apache License, Version 2.0',
      packages=find_packages(),
      scripts=[],
      include_package_data=True,
      install_requires=[
          str(requirement.req)
          for requirement in parse_requirements('requirements.txt',
                                                session=PipSession())
      ],
      test_suite='tests',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.6',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Software Development :: Build Tools'],
      keywords=['docker', 'dashboard', 'bigboat', 'api'])
