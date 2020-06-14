from test_api import db

from datetime import datetime


class Instructor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(20), nullable=False)
    # uselist = False (for one to one relationship) and set foreign key in another db to True to make it safe
    courses = db.relationship('Course', backref='instructor', lazy=True)


# class StudentCourse(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     student_id = db.Column('student_id', db.Integer, db.ForeignKey("student.id"), nullable=False)
#     course_id = db.Column('course_id', db.Integer, db.ForeignKey("course.id"), nullable=False)

StudentCourse = db.Table('student_course',
                              db.Column('id',
                                        db.Integer,
                                        primary_key=True),
                              db.Column('student_id',
                                        db.Integer,
                                        db.ForeignKey('student.id', ondelete="cascade")),
                              db.Column('course_id',
                                        db.Integer,
                                        db.ForeignKey('course.id', ondelete="cascade")))

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    program = db.Column(db.String(20), nullable=False)
    courses = db.relationship('Course', secondary=StudentCourse, backref='students', lazy=True)

    # def __repr__(self):
    #     return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    course_level = db.Column(db.String(20), nullable=False)
    max_capacity = db.Column(db.Integer, nullable=False)
    current_students = db.Column(db.Integer, default=0)
    instructor_id = db.Column('instructor_id', db.Integer, db.ForeignKey("instructor.id",ondelete='CASCADE'), nullable=True)
    #course_students = db.relationship('Student', secondary=StudentCourse, backref='courses', lazy=True)
    #instructor = db.relationship('Instructor', backref='instructor', lazy=True)


#obj.query.order_by(obj.name).all()
#obj.query.filter(db.or_(Obj.name == "haris", Obj.id > 2)).all()
#obj.query.filter(Obj.name == "haris", Obj.id > 2).all()   THIS WILL BE AND
#obj.query.limit(2).all()
#obj.query.offset(2).limit(3).all()   SKIPS OVER 2
#Course_model.query.filter_by(instructor_id=id).update({Course_model.instructor_id: None})  UPDATE multiple value (delete would delete multiple values)
# http://www.leeladharan.com/sqlalchemy-query-with-or-and-like-common-filters  (filters)

#db.engine.execute('<SQL QUERY>')

