import os, json
from flask import Flask, request, jsonify, make_response, abort
from flask.blueprints import Blueprint
from database import db, User, Course, Link
from sqlalchemy.exc import SQLAlchemyError
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context

auth = HTTPBasicAuth()

api_v1 = Blueprint('api_v1',__name__)

#@api_v1.errorhandler(404)
#def not_found(error):
#    return make_response(jsonify({'error':'Not found'}), 404)

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    return user and pwd_context.verify(password, user.password_hash)

'''Routes should always have start/end slash'''

@api_v1.route('/users/',methods=['GET'])
def get_users():
    response = [user.to_dict() for user in User.query.all()]
    status = 200
    return jsonify(response), status

@api_v1.route('/users/',methods=['POST'])
def create_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)

    user = User(username=username,points=0,password_hash=pwd_context.encrypt(password))
    try:
        db.session.add(user)
        db.session.commit()
    except SQLAlchemyError as e:
        abort(422)
    response = user.to_dict()
    status = 201
    return jsonify(response), status


@api_v1.route('/users/<username>/courses/',methods=['GET'])
@auth.login_required
def get_courses(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    response = [course.to_dict() for course in user.courses]
    status = 200
    return jsonify(response), status 

@api_v1.route('/users/<username>/courses/',methods=['POST'])
@auth.login_required
def create_course(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    if not request.json or not 'name' in request.json:
        abort(400)
    try:
        course = Course(name=request.json['name'],user_id=user.id)
        user.courses.append(course)    
        db.session.add(course)
        db.session.commit()
    except SQLAlchemyError as e:
        abort(422)
    
    response = course.to_dict()
    status = 201
    return jsonify(response), status

@api_v1.route('/users/<username>/courses/<course_id>/',methods=['GET'])
@auth.login_required
def get_course(username,course_id):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    course = user.courses.filter_by(id=course_id).first()
    if course is None:
        abort(404)

    response = course.to_dict()
    status = 200
    return jsonify(response), status 

@api_v1.route('/users/<username>/courses/<course_id>/links/',methods=['GET'])
@auth.login_required
def get_course_links(username,course_id):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    course = user.courses.filter_by(id=course_id).first()
    if course is None:
        abort(404)

    response = [link.to_dict() for link in course.links]
    status = 200
    return jsonify(response), status 

@api_v1.route('/users/<username>/courses/<course_id>/links/',methods=['POST'])
@auth.login_required
def add_course_link(username,course_id):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    course = user.courses.filter_by(id=course_id).first()
    if course is None:
        abort(404)
    if not request.json or not 'url' in request.json:
        abort(400)
    try:
        url = request.json['url']
        text = request.json.get('text',url)
        link = Link(url=url,text=text,user_id=user.id,course_id=course.id)
        course.links.append(link)
        db.session.add(link)
        db.session.commit()
    except SQLAlchemyError as e:
        abort(422)

    response = {}
    response["links"] = link.to_dict()
    status = 201
    return jsonify(response), status 

