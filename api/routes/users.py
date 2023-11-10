# Project dependencies
from flask_restx import Resource, Namespace, abort
from sqlalchemy.orm.exc import NoResultFound
from flask import request

#Local imports
from api.database import db
from api.models.users import User as UserModel
from api.schemas import users as dto
from api.common import enums
from api.common.authentication import TokenProtectedResource


users_ns = Namespace(
    name='users', 
    description='Users Endpoints'
)

@users_ns.route('/')
class ListUsers(TokenProtectedResource):

    @users_ns.doc(security='BearerAuth')
    @users_ns.marshal_with(dto.user, as_list=True)
    def get(self):
        """Get all users"""
        if request._user_data['role'] == enums.Role.USER.name:
            abort(403, message='Forbidden')
        users = UserModel.query.filter(UserModel.status != enums.Status.DELETED).all()
        return users, 200

    

@users_ns.route('/<int:user_id>')
class User(TokenProtectedResource):

    @users_ns.marshal_with(dto.user)
    def get(self, user_id):
        """Get user"""
        try:
            if request._user_data['role'] == enums.Role.USER.name and request._user_data['user_id'] != user_id:
                abort(403, message='You can only get your own user')
            user = UserModel.query.filter(UserModel.id == user_id, UserModel.status != enums.Status.DELETED).one()
            return user, 200
        except NoResultFound:
            abort(404, message='User not found')

    def delete(self, user_id):
        """Delete user"""
        try:
            if request._user_data['role'] == enums.Role.USER.name:
                abort(403, message='Forbidden')
            user = UserModel.query.filter(UserModel.id == user_id).one()
            user.status = enums.Status.DELETED
            db.session.commit()
            return '', 204
        except NoResultFound:
            abort(404, message='User not found')

    @users_ns.expect(dto.update_user, validate=True)
    @users_ns.marshal_with(dto.update_user)
    def patch(self, user_id):
        """Update user"""
        try:
            if request._user_data['role'] == enums.Role.USER.name and request._user_data['user_id'] != user_id:
                abort(403, message='You can only update your own user')
            user = UserModel.query.filter(
                UserModel.id == user_id,
                UserModel.status != enums.Status.DELETED                           
            ).one()
            user_data = users_ns.payload
            for key, value in user_data.items():
                setattr(user, key, value)
            db.session.commit()
            return user, 200
        except NoResultFound:
            abort(404, message='User not found')
