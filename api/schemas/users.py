# Third party modules
from flask_restx import fields

# Local modules
from api import root_api as api


user = api.model('User', {
    'id': fields.Integer(required=False, readonly=True),
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'username': fields.String(required=True),
    'email': fields.String(required=True),
    'about': fields.String(required=False),
    'status': fields.String(
        required=False,
        attribute = lambda user: user.status.name
    ),
    'role': fields.String(
        required=False,
        attribute = lambda user: user.role.name
    ),
    'created_at': fields.DateTime(required=False),
    'updated_at': fields.DateTime(required=False),
})

users = api.model('Users response', {
    'users': fields.List(
        fields.Nested(user),
        description='List of users',
        attribute=lambda user: user
    ),
})

update_user = api.model('Update user', {
    'first_name': fields.String(required=False),
    'last_name': fields.String(required=False),
    'username': fields.String(required=False),
    'about': fields.String(required=False),
})
