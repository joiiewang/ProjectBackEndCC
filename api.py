import os, json
from flask import Flask, request, jsonify, make_response, abort
from flask.blueprints import Blueprint
from database import db, User, Course, Link

api_v1 = Blueprint('api_v1',__name__)

@api_v1.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Not found'}), 404)

'''Routes should always have start/end slash'''

@api_v1.route('/users/',methods=['GET'])
def get_users():
    response = {}
    response["users"] = [{"id":user.id,"username":user.username,"first_name":user.first_name} for user in User.query.all()]
    status = 200
    return jsonify(response), status

@api_v1.route('/users/',methods=['POST'])
def create_user():
    if not request.json or not 'username' in request.json:
        abort(400)
    user = User(username=request.json['username'],first_name=request.json.get('first_name',''))
    db.session.add(user)
    db.session.commit()

    response = {}
    response["user"] = {"id":user.id,"username":user.username,"first_name":user.first_name}
    status = 201
    return jsonify(response), status



@api_v1.route('/users/<username>/courses/',methods=['GET'])
def get_courses(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    response = {}
    response["courses"] = [{"id":course.id,"course_name":course.course_name} for course in user.courses]
    status = 200
    return jsonify(response), status 

@api_v1.route('/users/<username>/courses/',methods=['POST'])
def create_course(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    if not request.json or not 'course_name' in request.json:
        abort(400)
    course = Course(course_name=request.json['course_name'],user_id=user.id)
    user.courses.append(course)    
    db.session.add(course)
    db.session.commit()

    response = {}
    response["courses"] = {"id":course.id,"course_name":course.course_name}
    status = 201
    return jsonify(response), status

@api_v1.route('/users/<username>/courses/<course_id>/links/',methods=['GET'])
def get_course_links(username,course_id):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    course = user.courses.filter_by(id=course_id).first()
    if course is None:
        abort(404)

    response = {}
    response["links"]=[{"text":link.text,"url":link.url} for link in course.links]
    status = 200
    return jsonify(response), status 

@api_v1.route('/users/<username>/courses/<course_id>/links/',methods=['POST'])
def add_course_link(username,course_id):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    course = user.courses.filter_by(id=course_id).first()
    if course is None:
        abort(404)
    if not request.json or not 'url' in request.json:
        abort(400)
    link = Link(url=request.json['url'],text=request.json.get('text',request.json['url']),user_id=user.id,course_id=course.id)
    course.links.append(link)
    db.session.add(link)
    db.session.commit()

    response = {}
    response["links"]={"text":link.text,"url":link.url}
    status = 201
    return jsonify(response), status 

