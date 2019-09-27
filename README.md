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
        # django_saml2_auth doesn't support these natively so the package injects them
        'SIGNOUT_SLO': {
            'CERT': <tbd>
            'KEY': <tbd>
        }
    }

# Microsoft AD FS

WARNING:  ADFS SLO will not work with unsigned requests.  This means that you must provide a key and a cert and upload 
the cert to the ADFS Relaying Party Trust.  If you cannot -- or do not want to -- provide a certificate, see the 
`-django-saml2-auth-signout-redirect` plugin.  Instead of a true Single SingOut, this plugin will redirect the user to
the `idpinitiatedsignon` page, permitting the user to complete the signout manually. 

There are several issues using this package with ADFS:

 - ADFS does not provide a NameID by default.  NameID is required (at least by PySAML2) for SLO.
 - ADFS does not expose an SLO endpoint by default.
 
The following are one way to address these issues (but use at your own risk).  The Name ID strategy was taken from 
[this article](https://blogs.msdn.microsoft.com/card/2010/02/17/name-identifiers-in-saml-assertions/).  The SLO 
endpoint was taken from [this article](https://help.mulesoft.com/s/article/Configuring-ADFS-SLO-endpoint).  

 - In your SAMLConfig, add the line:
      
       'NAME_ID_FORMAT': 'urn:oasis:names:tc:SAML:2.0:nameid-format:persistent',
       
 - In your ADFS Claim Rules, add a custom rule ("Send Claims Using a Custom Rule"):

       c:[Type == "http://schemas.microsoft.com/ws/2008/06/identity/claims/windowsaccountname"]
       => add(
           store = "_OpaqueIdStore",
           types = ("http://mycompany/internal/persistentId"),
           query = "{0};{1};{2}",
           param = "ppid",
           param = c.Value,
           param = c.OriginalIssuer
       );

 - In your ADFS Claim Rules, add a Transform Rule:
    - Incoming claim type:  `http://mycompany/internal/persistentId` (literally this, don't change mycompany)
    - Outgoing claim type:  `NameID`
    - Outgoing name ID format:  `Persistent Identifier`

 - Under the Relaying Party Trust's `Properties` -> `Endpoints` tab, add a SAML Logout Endpoint:
 
    - Binding:  `POST`
    - Trusted URL:  Your ADFS endpoint, something like `https://<my.adfs.com>/adfs/ls`
    - Response URL:  empty
    
 - Under the Relaying Party Trust's `Properties` -> `Endpoints` tab