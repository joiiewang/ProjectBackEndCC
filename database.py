from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    courses = db.relationship('Course',backref='user',lazy='dynamic')
    links = db.relationship('Link',backref='user',lazy='dynamic')
    todos = db.relationship('ToDoList',backref='user',lazy='dynamic')
    notes = db.relationship('Note',backref='user',lazy='dynamic')

    points = db.Column(db.Integer, index=True, nullable=False)
    trees = db.Column(db.Integer, index=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
    def to_dict(self):
        return {"id":self.id,"username":self.username,"points":self.points, "trees":self.trees}

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    links = db.relationship('Link',backref='course',lazy='dynamic')
    todos = db.relationship('ToDoList',backref='course',lazy='dynamic')
    notes = db.relationship('Note',backref='course',lazy='dynamic')

    def __repr__(self):
        return f'<Course {self.name}>'
    def to_dict(self):
        return {"id":self.id,"name":self.name,"links":[link.to_dict() for link in self.links],
                "todos":[toDoItem.to_dict() for toDoItem in self.todos],"notes":[note.to_dict() for note in self.notes]}

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(64), index=True)
    url = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    def __repr__(self):
        return f'<Link {self.text}>'
    def to_dict(self):
        return {"id":self.id,"text":self.text,"url":self.url} 

class ToDoList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), index=True)
    dueDate = db.Column(db.String(16), index=True)
    completed = db.Column(db.Boolean, unique=False, default=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    def __repr__(self):
        return f'<ToDoList {self.text}>'
    def to_dict(self):
        return {"id":self.id,"text":self.text,"dueDate":self.dueDate, "completed":self.completed}

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    def __repr__(self):
        return f'<Note {self.text}>'
    def to_dict(self):
        return {"id":self.id,"text":self.text} 
