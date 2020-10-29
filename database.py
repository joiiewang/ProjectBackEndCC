from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(64), index=True, unique=True, nullable=False)
        first_name = db.Column(db.String(64), index=True, nullable=False)
        courses = db.relationship('Course',backref='student',lazy='dynamic')
        def __repr__(self):
                return f'<User {self.username}>'

class Course(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        course_name = db.Column(db.String(64), index=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        def __repr__(self):
                return f'<Course {self.name}>'

