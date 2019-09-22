# django-saml2-auth-signout-slo
A plugin to support Single LogOff (SLO) in django-saml2-auth

# Introduction

By default, django-saml2-auth only signs out users in the local Django application.  For security reasons,
the logout needs to be passed to the IdP (identity provider).  Otherwise, a user who clicks the login
button will be logged in again without providing a password (or otherwise).

# Example

In settings.py:

    INSTALLED_APPS += (
        ...
        'django_saml2_auth',
        # ensure the plugin is loaded
        'django_saml2_auth_signout_slo',
        ...
    )
    
    # this is the "usual" config object from django-saml2-auth
    SAML2_AUTH = {
        'DEFAULT_NEXT_URL': '/',
        'PLUGINS': {
            # use this package in lieu of DEFAULT signout plugin 
            'SINGOUT': ['SLO'],
        }
    }
