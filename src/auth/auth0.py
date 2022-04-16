import os
import json
from flask import request
from functools import wraps
from jose import jwt
from urllib.request import urlopen


ALGORITHMS = ['RS256']

'''
Authentication Error
Exception

'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


'''
Authentication Header

'''


def get_token_auth_header():
    if 'Authorization' not in request.headers:
        raise AuthError({
            "code": "authorization_header_missing",
            "description": "Authorization header is expected"}, 401)

    auth_header = request.headers['Authorization']
    headers_parts = auth_header.split(' ')

    if headers_parts[0].lower() != 'bearer':
        raise AuthError({
            "code": "invalid_header",
            "description": "Authorization header must start with Bearer"}, 401)

    elif len(headers_parts) == 1:
        raise AuthError({
            "code": "invalid_header",
            "description": "Token not found"}, 401)

    elif len(headers_parts) > 2:
        raise AuthError({
            "code": "invalid_header",
            "description": "Authorization header must be Bearer token"}, 401)

    token = headers_parts[1]

    return token


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            "code": "Bad Request",
            "description": "Permissions not included"}, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            "code": "Unauthorized",
            "description": "You don't have access to this resource"}, 403)

    return True


def verify_decode_jwt(token):
    jsonurl = urlopen(os.environ['AUTH0_DOMAIN'])
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}

    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed'}, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        try:
            issuer = os.environ['AUTH0_DOMAIN']
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=os.environ['AUTH0_AUDIENCE'],
                issuer=issuer[0:-21],
                options={'verify_exp': False}
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired'}, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer'}, 401)

        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token'}, 400)

    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key'}, 400)


'''
Auth Decorator

'''


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()

            try:
                payload = verify_decode_jwt(token)

            except():
                raise AuthError({
                    "code": "Unauthorized",
                    "description": "Unauthorized"}, 401)

            check_permissions(permission, payload)

            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator

