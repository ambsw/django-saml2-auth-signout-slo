"""The setup module for django_saml2_auth_signout_slo.
See:
https://github.com/ambsw/django_saml2_auth_signout_slo
"""

from codecs import open
from os import path

from setuptools import (setup, find_packages)

import django_saml2_auth_signout_slo

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django_saml2_auth_signout_slo',

    version=django_saml2_auth_signout_slo.__version__,

    description='Single LogOut (SLO) plugin for django_saml2_auth',
    # requires unix line endings
    long_description=long_description,
    long_description_content_type="text/markdown",

    url='https://github.com/ambsw/django-saml2-auth-signout-slo',

    author='Clayton Daley',
    author_email='technology+saml2_signout_slo@gmail.com',

    license='Apache 2.0',

    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'License :: OSI Approved :: Apache Software License',

        'Framework :: Django :: 1.5',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='Django SAML2 Plugin for Single LogOut (SLO)',

    packages=find_packages(),

    install_requires=[
        'django_saml2_auth',
    ],
    include_package_data=True,
)
