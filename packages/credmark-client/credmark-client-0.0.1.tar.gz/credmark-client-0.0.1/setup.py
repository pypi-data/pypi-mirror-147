#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup, find_namespace_packages as find_packages
except ImportError:
    from distutils.core import setup
    find_packages = None

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='credmark-client',
    version='0.0.1',
    description='Credmark client lib',
    long_description=readme + '\n\n' + history,
    author='Credmark',
    author_email='info@credmark.com',
    url='https://github.com/credmark/credmark-client-py',
    python_requires='>=3.7.0',
    packages=find_packages() if find_packages is not None else ['credmark'],
    package_dir={'credmark':
                 'credmark'},
    include_package_data=True,
    install_requires=[
        'requests>=2.27.1',
    ],
    entry_points={
        'console_scripts': [
            'credmark = credmark.client.cli:main'
        ]
    },
    license="MIT",
    zip_safe=False,
    keywords='Credmark crypto risk model client',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 3",
    ],
    tests_require=[
    ],
    test_suite='',
)
