import os, json
from flask import Flask, request, jsonify, make_response, abort
from flask_restful import Api, Resource, reqparse, fields, marshal
from database import db, User, Course, Link, ToDoList, Note
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
                points=0)
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(422)
        return user.to_dict()

class UserAPI(Resource):
    decorators = [auth.login_required]
    def __init__(self):
        super(UserAPI,self).__init__()

    def get(self,username):
        if username != auth.current_user().username:
            abort(401)
        return auth.current_user().to_dict()

class CourseListAPI(Resource):
    decorators = [auth.login_required]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name',type=str,required=True,
                help='No course name provided',location='json')
        super(CourseListAPI,self).__init__()

    def get(self,username):
        if username != auth.current_user().username:
            abort(401)
        return [course.to_dict() for course in auth.current_user().courses]

    def post(self,username):
        if username != auth.current_user().username:
            abort(401)
        args = self.reqparse.parse_args()
        try:
            user = auth.current_user()
            course = Course(name=args['name'],user_id=user.id)
            user.courses.append(course)
            db.session.add(course)
            db.session.commit()
            return course.to_dict()
        except SQLAlchemyError as e:
            abort(422)

class CourseAPI(Resource):
    decorators = [auth.login_required]
    def __init__(self):
        super(CourseAPI,self).__init__()

    def get(self,username,courseid):
        if username != auth.current_user().username:
            abort(401)
        user = auth.current_user()
        course = user.courses.filter_by(id=courseid).first()
        if not course:
            abort(404)
        return course.to_dict()

    def delete(self,username,courseid):
        if username != auth.current_user().username:
            abort(401)
        user = auth.current_user()
        course = user.courses.filter_by(id=courseid).first()
        if not course:
            abort(404)
        try:
            for link in course.links:
	            db.session.delete(link)
            for toDoItem in course.todos:
	            db.session.delete(toDoItem)
            for note in course.notes:
	            db.session.delete(note)
            db.session.delete(course)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(422)

class LinkListAPI(Resource):
    decorators = [auth.login_required]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('text',type=str,required=True,
                help='No text provided',location='json')
        self.reqparse.add_argument('url',type=str,required=True,
                help='No url provided',location='json')
        self.reqparse.add_argument('course_id',type=int,required=False,
                help='No course id provided',location='json')
        super(LinkListAPI,self).__init__()

    def get(self,username):
        if username != auth.current_user().username:
            abort(401)
        links = auth.current_user().links
        if 'course_id' in request.args:
            if request.args['course_id']=="none":
                links = links.filter_by(course_id=None)
            else:
                links = links.filter_by(course_id=request.args['course_id'])
        return [link.to_dict() for link in links]

    def post(self,username):
        if username != auth.current_user().username:
            abort(401)
        args = self.reqparse.parse_args()
        try:
            user = auth.current_user()
            course_id=args['course_id']
            print("Course id = ",course_id)
            if course_id is not None:
                course = user.courses.filter_by(id=course_id).first()
                if not course:
                    abort(422)
                print("Course found: ",course)
                link = Link(text=args['text'],url=args['url'],course=course,user_id=user.id)
            else:
                link = Link(text=args['text'],url=args['url'],user_id=user.id)
            user.links.append(link)    
            db.session.add(link)
            db.session.commit()
            return link.to_dict()
        except SQLAlchemyError as e:
            abort(422)

class LinkAPI(Resource):
    decorators = [auth.login_required]
    def __init__(self):
        super(LinkAPI,self).__init__()

    def get(self,username,linkid):
        if username != auth.current_user().username:
            abort(401)
        user = auth.current_user()
        link = user.links.filter_by(id=linkid).first()
        if not link:
            abort(404)
        return link.to_dict()

    def delete(self,username,linkid):
        if username != auth.current_user().username:
            abort(401)
        user = auth.current_user()
        link = user.links.filter_by(id=linkid).first()
        if not link:
            abort(404)
        try:
            db.session.delete(link)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(422)

class ToDoListAPI(Resource):
    decorators = [auth.login_required]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('text',type=str,required=True,
                help='No text provided',location='json')
        self.reqparse.add_argument('dueDate',type=str,required=True,
                help='No dueDate provided',location='json')
        self.reqparse.add_argument('course_id',type=int,required=False,
                help='No course id provided',location='json')
        super(ToDoListAPI,self).__init__()

    def get(self,username):
        if username != auth.current_user().username:
            abort(401)
        todos = auth.current_user().todos
        if 'course_id' in request.args:
            if request.args['course_id']=="none":
                todos = todos.filter_by(course_id=None)
            else:
                todos = todos.filter_by(course_id=request.args['course_id'])
        return [toDoItem.to_dict() for toDoItem in todos]

    def post(self,username):
        if username != auth.current_user().username:
            abort(401)
        args = self.reqparse.parse_args()
        try:
            user = auth.current_user()
            course_id=args['course_id']
            print("Course id = ",course_id)
            if course_id is not None:
                course = user.courses.filter_by(id=course_id).first()
                if not course:
                    abort(422)
                print("Course found: ",course)
                toDoItem = ToDoList(text=args['text'],dueDate=args['dueDate'],course=course,user_id=user.id)
            else:
                toDoItem = ToDoList(text=args['text'],dueDate=args['dueDate'],user_id=user.id)
            user.todos.append(toDoItem)    
            db.session.add(toDoItem)
            db.session.commit()
            return toDoItem.to_dict()
        except SQLAlchemyError as e:
            abort(422)
    

class ToDoItemAPI(Resource):
    decorators = [auth.login_required]
    def __init__(self):
        super(ToDoItemAPI,self).__init__()

    def get(self,username,toDoItemid):
        if username != auth.current_user().username:
            abort(401)
        user = auth.current_user()
        toDoItem = user.todos.filter_by(id=toDoItemid).first()
        if not toDoItem:
            abort(404)
        return toDoItem.to_dict()

    def post(self,username,toDoItemid):
        if username !=auth.current_user().username:
            abort(401)
        user = auth.current_user()
        toDoItem = user.todos.filter_by(id=toDoItemid).first()
        if not toDoItem:
            abort(404)
        toDoItem.completed = not toDoItem.completed
        db.session.commit()
        return toDoItem.to_dict()

    def delete(self,username,toDoItemid):
        if username != auth.current_user().username:
            abort(401)
        user = auth.current_user()
        toDoItem = user.todos.filter_by(id=toDoItemid).first()
        if not toDoItem:
            abort(404)
        try:
            db.session.delete(toDoItem)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(422)

class NoteListAPI(Resource):
    decorators = [auth.login_required]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('text',type=str,required=True,
                help='No text provided',location='json')
        self.reqparse.add_argument('course_id',type=int,required=False,
                help='No course id provided',location='json')
        super(NoteListAPI,self).__init__()

    def get(self,username):
        if username != auth.current_user().username:
            abort(401)
        notes = auth.current_user().notes
        if 'course_id' in request.args:
            if request.args['course_id']=="none":
                notes = notes.filter_by(course_id=None)
            else:
                notes = notes.filter_by(course_id=request.args['course_id'])
        return [note.to_dict() for note in notes]

    def post(self,username):
        if username != auth.current_user().username:
            abort(401)
        args = self.reqparse.parse_args()
        try:
            user = auth.current_user()
            course_id=args['course_id']
            print("Course id = ",course_id)
            if course_id is not None:
                course = user.courses.filter_by(id=course_id).first()
                if not course:
                    abort(422)
                print("Course found: ",course)
                note = Note(text=args['text'],course=course,user_id=user.id)
            else:
                note = Note(text=args['text'],user_id=user.id)
            user.notes.append(note)    
            db.session.add(note)
            db.session.commit()
            return note.to_dict()
        except SQLAlchemyError as e:
            abort(422)

class NoteAPI(Resource):
    decorators = [auth.login_required]
    def __init__(self):
        super(NoteAPI,self).__init__()

    def get(self,username,noteid):
        if username != auth.current_user().username:
            abort(401)
        user = auth.current_user()
        note = user.notes.filter_by(id=noteid).first()
        if not note:
            abort(404)
        return note.to_dict()

    def delete(self,username,noteid):
        if username != auth.current_user().username:
            abort(401)
        user = auth.current_user()
        note = user.notes.filter_by(id=noteid).first()
        if not note:
            abort(404)
        try:
            db.session.delete(note)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(422)

def initialize_routes(api):
    api.add_resource(UserListAPI,'/api/v2/users/',endpoint='users')
    api.add_resource(UserAPI,'/api/v2/users/<string:username>/',endpoint='user')
    api.add_resource(CourseListAPI,'/api/v2/users/<string:username>/courses/',endpoint='courses')
    api.add_resource(CourseAPI,'/api/v2/users/<string:username>/courses/<int:courseid>/',endpoint='course')
    api.add_resource(LinkListAPI,'/api/v2/users/<string:username>/links/',endpoint='links')
    api.add_resource(LinkAPI,'/api/v2/users/<string:username>/links/<int:linkid>/',endpoint='link')
    api.add_resource(ToDoListAPI,'/api/v2/users/<string:username>/todos/',endpoint='todos')
    api.add_resource(ToDoItemAPI,'/api/v2/users/<string:username>/todos/<int:toDoItemid>/',endpoint='toDoItem')
    api.add_resource(NoteListAPI,'/api/v2/users/<string:username>/notes/',endpoint='notes')
    api.add_resource(NoteAPI,'/api/v2/users/<string:username>/notes/<int:noteid>/',endpoint='note')
    