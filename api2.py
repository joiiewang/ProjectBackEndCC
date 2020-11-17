import os, json
from flask import Flask, request, jsonify, make_response, abort
from flask_restful import Api, Resource, reqparse, fields, marshal
from database import db, User, Course, Link
from sqlalchemy.exc import SQLAlchemyError
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context

auth = HTTPBasicAuth()


#@api_v2.errorhandler(404)
#def not_found(error):
#    return make_response(jsonify({'error':'Not found'}), 404)

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and pwd_context.verify(password, user.password_hash):
        return user

'''Routes should always have start/end slash'''

class UserListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username',type=str,required=True,
                help='No username provided',location='json')
        self.reqparse.add_argument('password',type=str,required=True,
                help='No password provided',location='json')
        super(UserListAPI,self).__init__()

    def get(self):
        return [user.to_dict() for user in User.query.all()]

    def post(self):
        args = self.reqparse.parse_args()
        user = User(username=args['username'],password_hash=pwd_context.encrypt(args['password']),
                first_name='',points=0)
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(422)
        return user.to_dict()

class UserAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username',type=str,required=True,
                help='No username provided',location='json')
        self.reqparse.add_argument('password',type=str,required=True,
                help='No password provided',location='json')
        super(UserAPI,self).__init__()

    @auth.login_required
    def get(self,username):
        if username != auth.current_user().username:
            abort(401)
        return auth.current_user().to_dict()

def initialize_routes(api):
    api.add_resource(UserListAPI,'/api/v2/users/',endpoint='users')
    api.add_resource(UserAPI,'/api/v2/users/<string:username>/',endpoint='user')

