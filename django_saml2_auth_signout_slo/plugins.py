from django.contrib.auth import logout
from django_saml2_auth import utils
from django_saml2_auth.plugins import SignoutPlugin
from django_saml2_auth.views import _get_saml_client
from saml2.client_base import LogoutError


class SingleLogOutSignoutHandler(SignoutPlugin):
    KEY = 'SLO'

    @classmethod
    def signout(cls, request):
        """Logs the user out of the local system and redirects them to the SLO URL in the SAML Metadata"""
        name_id = request.session['name_id']
        logout(request)

        # from pysaml2/example/sp-wsgi/sp.py
        try:
            saml_client = _get_saml_client(utils.get_current_domain(request))
            responses = saml_client.global_logout(name_id).items()
            return responses[0]
        except LogoutError:
            pass
