from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect
from django_saml2_auth import utils
from django_saml2_auth.plugins import SignoutPlugin
from django_saml2_auth.views import _get_saml_client, _idp_error
from saml2 import entity
from saml2.client_base import LogoutError
from saml2.httputil import Response
from saml2.ident import decode


class SingleLogOutSignoutHandler(SignoutPlugin):
    KEY = 'SLO'

    @classmethod
    def signout(cls, request):
        """Logs the user out of the local system and redirects them to the SLO URL in the SAML Metadata"""
        name_id = decode(request.session['name_id'])
        logout(request)

        # from pysaml2/example/sp-wsgi/sp.py
        try:
            saml_client = _get_saml_client(utils.get_current_domain(request))
            data = saml_client.global_logout(name_id)
            # following example flow control (with Django responses) at:
            #    https://github.com/IdentityPython/pysaml2/blob/aed2ed41814b6b9f3d80121d42290ff0a2767cb2/example/sp-wsgi/sp.py#L742
            for entity_id, logout_info in data.items():
                if isinstance(logout_info, tuple):
                    binding, http_info = logout_info

                    if binding == entity.BINDING_HTTP_POST:
                        body = "".join(http_info["data"])
                        return HttpResponse(body)
                    elif binding == entity.BINDING_HTTP_REDIRECT:
                        for key, value in http_info["headers"]:
                            if key.lower() == "location":
                                return HttpResponseRedirect(value)
                        return _idp_error(ValueError("Missing Location Header"))
                    else:
                        return _idp_error(ValueError("Unknown Logout Binding: %s", binding))
                else:  # result from SOAP logout, should be OK
                    pass
            # in pysaml2 example, this is found in `finish_logout`
            saml_client.local_logout(name_id)
        except LogoutError as e:
            cls.logger.warn("LogoutError:  {}".format(e.args))
