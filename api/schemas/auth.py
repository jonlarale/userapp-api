# Third party modules
from flask_restx import fields

# Local modules
from api import root_api as api

get_reset_password_token = api.model('Get reset password token', {
    'email': fields.String(required=True, description='User email')
})

login = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

signup = api.model('Signup', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
    'password_confirmation': fields.String(required=True, description='User password confirmation')
})

token = api.model('Token', {
    'access_token': fields.String(description='JWT access token')
})

login_response = api.model('Login response', {
    'access_token': fields.String(description='JWT access token'),
    'user_id': fields.Integer(description='User id'),
    'role': fields.String(description='User role'),
    'email': fields.String(description='User email')
})

update_password = api.model('Update password', {
    'password': fields.String(required=True, description='User password'),
    'password_confirmation': fields.String(required=True, description='User password confirmation'),
    'token': fields.String(required=True, description='Reset password token')
})

reset_password_token = api.model('Reset password token', {
    'token': fields.String(required=True, description='Reset password token')
})