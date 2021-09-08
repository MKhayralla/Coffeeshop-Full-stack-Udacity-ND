import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen



AUTH0_DOMAIN = 'dev-vy99-vnq.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'https://drinks.udacity.api'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code


## Auth Header

'''
@TODO implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''
def get_token_auth_header():
    auth_header = request.headers.get('Authorization', None)
    if auth_header is None:
        raise AuthError('No authorization header found', 401)
    auth_header_splitted = auth_header.split(sep = ' ')
    if auth_header_splitted[0].lower() != 'bearer':
        raise AuthError('Authorization header malformed', 401)
    try:
        token = auth_header_splitted[1]
        return token
    except :
        raise AuthError('Authorization header malformed', 401)

'''
@TODO implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''
def check_permissions(permission, payload:dict):
    if 'permissions' not in payload:
        raise AuthError('no permissions list present', 403)
    if permission not in payload['permissions']:
        raise AuthError('you don\'t have enough permissions to perform this action', 403 )
    return True

'''
@TODO implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''
def verify_decode_jwt(token):
    try:
        header = jwt.get_unverified_header(token)
        if 'kid' not in header:
            raise AuthError('malform token', 401)
        json_signature_data = urlopen('https://{}/.well-known/jwks.json'.format(AUTH0_DOMAIN)).read()
        data = json.loads(json_signature_data)
        rsa_key_list = list(filter(lambda x:x['kid'] == header['kid'], data['keys']))
        if len(rsa_key_list) < 1 :
            raise AuthError('kid not valid', 401)
        rsa_key = rsa_key_list[0]
        payload = jwt.decode(
            token,
            rsa_key,
            ALGORITHMS,
            audience=API_AUDIENCE,
            issuer='https://{}/'.format(AUTH0_DOMAIN)
            )
        return payload
    except jwt.JWTClaimsError :
        raise AuthError('invalid claims', 401)
    except jwt.ExpiredSignatureError:
        raise AuthError('expired token provided', 401)
    except :
        raise AuthError('Authentication failed',  401)

'''
@TODO implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            _request_ctx_stack.top.current_user = payload
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator