from django import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django_saml2_auth import signals, utils


class AppConfig(apps.AppConfig):
    name = 'django_saml2_auth_signout_slo'

    def ready(self):
        # import plugins
        # noinspection PyUnresolvedReferences
        from . import plugins

        if 'SLO' in settings.SAML2_AUTH.get('PLUGINS', {}).get('SIGNOUT', []):
            # NameID is required
            if settings.SAML2_AUTH.get('NAME_ID_FORMAT') in [None, 'None']:
                raise ImproperlyConfigured(
                    "django-saml2-auth-signout-slo requires a valid SAML2_AUTH.NAME_ID_FORMAT, not None"
                )

            # cache the NameID in the session
            signals.before_authenticated.attach(utils.store_name_id)
