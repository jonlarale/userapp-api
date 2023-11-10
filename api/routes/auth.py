from flask_restx import Resource, Namespace
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

from api.database import db
from api.models.users import User as UserModel
from api.schemas import users as user_dto
from api.schemas import auth as auth_dto
from api.common.authentication import gen_access_token, decode_access_token
from api.common import enums

auth_ns = Namespace('auth', description='Authentication Endpoints')


@auth_ns.route('/login')
class UserLogin(Resource):
    @auth_ns.expect(auth_dto.login)
    @auth_ns.marshal_with(auth_dto.login_response)
    def post(self):
        """User login to get access token"""
        data = auth_ns.payload
        user = UserModel.query.filter_by(email=data['email']).first()
        if user and check_password_hash(user._password, data['password']):
            access_token = gen_access_token(user.id, user.role.name)
            return {
                'access_token': access_token, 'user_id':user.id,
                'role': user.role.name,
                'email': user.email
            }, 200
        else:
            auth_ns.abort(401, 'Invalid credentials')

@auth_ns.route('/signup')
class UserSignup(Resource):
    @auth_ns.expect(auth_dto.signup)
    @auth_ns.marshal_with(user_dto.user, skip_none=True)
    def post(self):
        """User signup"""
        data = auth_ns.payload
        if data['password'] != data['password_confirmation']:
            auth_ns.abort(
                400, 'Password and password confirmation must match.'
            )
        hashed_password = generate_password_hash(data['password'])
        new_user = UserModel(
            email=data['email'], _password=hashed_password,
            role=enums.Role.USER, 
            status=enums.Status.ACTIVE
        )
        db.session.add(new_user)
        try:
            db.session.commit()
            return new_user, 201
        except IntegrityError:
            db.session.rollback()
            auth_ns.abort(
                400, 'Email already in use.'
            )

@auth_ns.route('/refresh')
class TokenRefresh(Resource):
    @auth_ns.response(200, 'Token successfully refreshed.')
    @auth_ns.expect(auth_dto.token)
    @auth_ns.marshal_with(auth_dto.token)
    def post(self):
        """Refresh access token"""
        data = auth_ns.payload
        decoded_token = decode_access_token(data['access_token'])
        user = UserModel.query.get(decoded_token['user_id'])
        if not user:
            auth_ns.abort(401, 'Invalid token or user not found')

        new_access_token = gen_access_token(user.id, user.role.name)
        return {'access_token': new_access_token}, 200

@auth_ns.route('/reset-password')
class ResetPassword(Resource):
    @auth_ns.response(200, 'Password successfully reset.')
    @auth_ns.expect(auth_dto.get_reset_password_token)
    @auth_ns.marshal_with(auth_dto.reset_password_token)
    def post(self):
        """Get reset password token"""
        data = auth_ns.payload
        user = UserModel.query.filter_by(email=data['email']).first()
        if not user:
            auth_ns.abort(404, 'User not found')
        token = gen_access_token(user.id, user.role.name)
        return {'token': token}, 200
    
    @auth_ns.response(200, 'Password successfully updated.')
    @auth_ns.expect(auth_dto.update_password)
    @auth_ns.marshal_with(auth_dto.token)
    def patch(self):
        """Update password"""
        data = auth_ns.payload
        decoded_token = decode_access_token(data['token'])
        user = UserModel.query.get(decoded_token['user_id'])
        if not user:
            auth_ns.abort(401, 'Invalid token or user not found')
        if data['password'] != data['password_confirmation']:
            auth_ns.abort(
                400, 'Password and password confirmation must match.'
            )
        hashed_password = generate_password_hash(data['password'])
        user._password = hashed_password
        user.status = enums.Status.ACTIVE
        db.session.commit()
        new_access_token = gen_access_token(user.id, user.role.name)
        return {'access_token': new_access_token}, 200