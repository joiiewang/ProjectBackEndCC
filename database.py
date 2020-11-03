from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    first_name = db.Column(db.String(64), index=True, nullable=False)
    courses = db.relationship('Course',backref='student',lazy='dynamic')
    def __repr__(self):
        return f'<User {self.username}>'
    def to_dict(self):
        return {"id":self.id,"username":self.username,"first_name":self.first_name} 

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    links = db.relationship('Link',backref='course',lazy='dynamic')
    def __repr__(self):
        return f'<Course {self.name}>'
    def to_dict(self):
        return {"id":self.id,"name":self.name}
    def to_dict_long(self):
        return {"id":self.id,"name":self.name,"links":[link.to_dict() for link in self.links]}

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
