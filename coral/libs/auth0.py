# -*- coding:utf-8 -*-
"""
Reference: https://github.com/auth0-samples/auth0-python-api-samples/tree/master/00-Starter-Seed
"""

import json

from six.moves.urllib.request import urlopen
from jose import jwt


options = {
    "verify_aud": False,
    "verify_exp": True,
    "verify_iss": True
}

class TokenExpiredException(Exception):
    message = 'token is expired'
    def __init__(self):
        super(TokenExpiredException, self).__init__(self.message)

class Auth0Connector(object):
    """A connector between auth0 and current requests"""
    def __init__(
        self,
        domain,
        api_identifier,
        algorithms=None,
        jwks_cache_timeout=0,
        **kwargs
    ):
        self.cache = None
        self.domain = domain
        self.api_identifier = api_identifier
        self.algorithms = algorithms or ['RS256']
        self.jwks_cache_timeout = jwks_cache_timeout
        self.jwks_cache_key = 'https://{}/.well-known/jwks.json'.format(self.domain)

    def set_cache(self, cache):
        """Set a cache object, which has get(key)/set(key, value, timeout) interface"""
        self.cache = cache

    def is_cache_enabled(self):
        return self.jwks_cache_timeout > 0 and self.cache

    def fetch_jwks(self):
        cache_enabled = self.is_cache_enabled()

        if cache_enabled:
            jwks = self.cache.get(self.jwks_cache_key)
            if jwks:
                return jwks

        jsonurl = urlopen('https://{}/.well-known/jwks.json'.format(self.domain))
        jwks = json.loads(jsonurl.read())

        if cache_enabled:
            self.cache.set(self.jwks_cache_key, jwks, self.jwks_cache_timeout)

        return jwks

    def verify_with_access_token(self, auth):
        """Get valid access token from the Authorization header"""
        # g.user = None

        # auth = request.headers.get('Authorization', None)
        # if not auth:
        #     return None

        auth = auth.split()
        if not (auth and auth[0].lower() == 'bearer'):
            return None

        if len(auth) == 1 or len(auth) > 2:
            raise Exception('Invalid token header.')

        raw_token = auth[1]

        try:
            unverified_header = jwt.get_unverified_header(raw_token)
        except jwt.JWTError:
            raise Exception('Invalid header. Use an RS256 signed JWT Access Token')
        if unverified_header['alg'] == 'HS256':
            raise Exception('Invalid header. Use an RS256 signed JWT Access Token')

        jwks = self.fetch_jwks()
        rsa_key = None

        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    raw_token,
                    rsa_key,
                    algorithms=self.algorithms,
                    options=options,
                    issuer="https://{0}/".format(self.domain)
                )
                xtp_attrs = payload['https://auth.xtalpi.com/Metadata']
                appmeta = xtp_attrs.get('app_metadata', dict())
                authorization_data = appmeta.get('authorization', dict())
            except jwt.ExpiredSignatureError:
                raise TokenExpiredException()
            except jwt.JWTClaimsError:
                raise Exception("incorrect claims, please check the audience and issuer")
            except Exception:
                raise Exception("Unable to parse authentication token.")


        return dict(
            is_authenticated=True,
            id=payload['sub'],
            name=xtp_attrs.get('userPrincipalName', None),
            email=xtp_attrs.get('userPrincipalName', None),
            groups=authorization_data.get('groups', []),
            roles=authorization_data.get('roles', []),
            is_active=True,
        )
        # g.auth0_access_token = raw_token
        # g.auth0_access_token_payload = payload
        # g.user = User(
        #     is_authenticated=True,
        #     id=payload['sub'],
        #     name=xtp_attrs['userPrincipalName'],
        #     email=xtp_attrs['userPrincipalName'],
        #     groups=appmeta['authorization']['groups'],
        #     roles=appmeta['authorization']['roles'],
        #     is_active=True,
        # )

    def hook_auth_on_each_request(self, app):
        """should be called only once for a single flask app"""
        app.before_request(self.verify_with_access_token)
