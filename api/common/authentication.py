"""Function definitions for authentication purposes."""

# Python libraries
import datetime as dt
from typing import Any, Callable

# Project dependencies
import jwt
from flask import request, abort
from flask_restx import Resource

# Local imports
from conf import cfg




def _gen_jwt(payload: dict[str, str], expiration_time: dt.timedelta) -> str:
    now = dt.datetime.utcnow()
    return jwt.encode(
        payload={
            'iat': now,
            'exp': now + expiration_time,
            **payload,
        },
        key=cfg.SECRET_KEY,
        algorithm='HS256'
    )


def gen_access_token(user_id: str, role: str) -> str:
    """Generate a JWT that contains the identification info of a user."""

    return _gen_jwt(
        payload={
            'user_id': user_id,
            'role': role,
        },
        expiration_time=dt.timedelta(
            hours=int(cfg.TOKEN_EXPIRE_HOURS),
            minutes=int(cfg.TOKEN_EXPIRE_MINUTES)
        )
    )


def gen_password_token(user_id: str) -> str:

    return _gen_jwt(
        payload={'user_id': user_id},
        expiration_time=dt.timedelta(
            hours=int(cfg.TOKEN_EXPIRE_HOURS),
            minutes=int(cfg.TOKEN_EXPIRE_MINUTES)
        )
    )


def decode_access_token(token: str) -> dict:
    """Decode a JWT. Raise an error if token is invalid or expired."""
    return jwt.decode(
        jwt=token, key=cfg.SECRET_KEY, algorithms=['HS256']
    )



def token_required(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Any:
        access_token: str = request.headers.get('Authorization')
        
        if not access_token:
            abort(401, 'Access token required')  
        try:
            access_token = access_token.replace('Bearer ', '')
            request._user_data = decode_access_token(access_token)
        except jwt.ExpiredSignatureError:
            abort(401, 'Token has expired')
        except jwt.InvalidTokenError:
            abort(401, 'Invalid token')

        return func(*args, **kwargs)

    return wrapper



class TokenProtectedResource(Resource):
    method_decorators = (token_required,)





