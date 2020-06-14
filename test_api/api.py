from test_api import rest_api
from test_api.models import Instructor as Instructor_model, Student as Student_model,\
    Course as Course_model
from test_api.schema import InstructorSchema, CourseSchema, CourseInstructorSchema, \
    StudentSchema, StudentCoursesSchema, InstructorCoursesSchema
from test_api import db
from flask import request
from flask_restplus import Resource, fields, reqparse
from datetime import date, datetime


@rest_api.route('/instructors')
class InstructorsList(Resource):
    def post(self):
        data = request.get_json(force=True)
        errors = InstructorSchema().validate(data)
        if errors:
            return errors, 422
        instructor = Instructor_model.query.filter_by(name=data['name']).first()
        if instructor:
            return {'message': 'Instructor already exists'}, 400
        new_instructor = Instructor_model(name=data['name'], title=data['title'])
        db.session.add(new_instructor)
        db.session.commit()
        result = InstructorSchema().dump(new_instructor)
        return result, 201

    def get(self):
        instructors = Instructor_model.query.all()
        result = InstructorSchema(many=True).dump(instructors)
        return result, 200

# instructor_model = rest_api.model('Create Instructor',
#                              {'name': fields.String(),
#                               'title': fields.String() }
#                              )

@rest_api.route('/instructors/<int:id>')
class Instructors(Resource):

#   @rest_api.expect(instructor_model, validate=True)
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('title', type=str)

        args = parser.parse_args()
        instructor = Instructor_model.query.filter_by(id=id).first()
        if not instructor:
            return {'message': 'Instructor not found'}, 404
        for k, v in args.items():
            if v is not None:
                setattr(instructor, k, v)
        db.session.add(instructor)
        db.session.commit()
        result = InstructorSchema().dump(instructor)
        return result, 200

    def get(self, id):
        instructor = Instructor_model.query.filter_by(id=id).first()
        if not instructor:
            return {'message': 'Instructor not found'}, 404
        result = InstructorSchema().dump(instructor)
        return result, 200

    def delete(self, id):
        instructor = Instructor_model.query.filter_by(id=id).first()
        if not instructor:
            return {'message': 'Instructor not found'}, 404
        Course_model.query.filter_by(instructor_id=id).update({Course_model.instructor_id: None})
        Instructor_model.query.filter_by(id=id).delete()
        db.session.commit()
        return '', 204


@rest_api.route('/students')
class StudentsList(Resource):
    def post(self):
        data = request.get_json(force=True)
        errors = StudentSchema().validate(data)
        if errors:
            return errors, 422
        student = Student_model.query.filter_by(name=data['name']).first()
        if student:
            return {'message': 'Student already exists'}, 400
        new_student = Student_model(name=data['name'], program=data['program'])
        db.session.add(new_student)
        db.session.commit()
        result = StudentSchema().dump(new_student)
        return result, 201

    def get(self):
        students = Student_model.query.all()
        result = StudentSchema(many=True).dump(students)
        return result, 200




@rest_api.route('/students/<int:id>')
class Students(Resource):

#   @rest_api.expect(student_model, validate=True)
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('program', type=str)

        args = parser.parse_args()
        student = Student_model.query.filter_by(id=id).first()
        if not student:
            return {'message': 'Student not found'}, 404
        for k, v in args.items():
            if v is not None:
                setattr(student, k, v)
        db.session.add(student)
        db.session.commit()
        result = StudentSchema().dump(student)
        return result, 200

    def get(self, id):
        student = Student_model.query.filter_by(id=id).first()
        if not student:
            return {'message': 'Student not found'}, 404
        result = StudentSchema().dump(student)
        return result, 200

    def delete(self, id):
        student = Student_model.query.filter_by(id=id).first()
        if not student:
            return {'message': 'Student not found'}, 404
        Course_model.query.filter_by(id=id).delete()
        db.session.commit()
        return '', 204


#################### Courses ##############

@rest_api.route('/courses')
class CoursesList(Resource):
    def post(self):
        data = request.get_json(force=True)
        errors = CourseSchema().validate(data)
        if errors:
            return errors, 422
        course = Course_model.query.filter_by(name=data['name']).first()
        if course:
            return {'message': 'Course already exists'}, 400
        new_course = Course_model(name=data['name'], start_date=data['start_date'], end_date=data['end_date'], course_level=data['course_level'],
                                  max_capacity= data['max_capacity'])
        db.session.add(new_course)
        db.session.commit()
        result = CourseSchema().dump(new_course)
        return result, 201

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('start_date', type=lambda x: datetime.strptime(x, '%Y-%m-%d').date(), location='args')

        args = parser.parse_args()
        if 'start_date' in args and args['start_date'] is not None:
            courses = Course_model.query.filter(Course_model.start_date > args['start_date'])
        else:
            courses = Course_model.query.all()
        result = CourseInstructorSchema(many=True).dump(courses)
        return result, 200




@rest_api.route('/courses/<int:id>')
class Courses(Resource):

#   @rest_api.expect(course_model, validate=True)
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('course_level', type=str, choices=['bachelors', 'masters', 'phd'])
        parser.add_argument('max_capacity', type=int)
        parser.add_argument('start_date', type=lambda x: datetime.strptime(x, '%Y-%m-%d').date())
        parser.add_argument('end_date', type=lambda x: datetime.strptime(x, '%Y-%m-%d').date())

        args = parser.parse_args()
        course = Course_model.query.filter_by(id=id).first()
        if not course:
            return {'message': 'Course not found'}, 404
        for k, v in args.items():
            if v is not None:
                setattr(course, k, v)
        db.session.add(course)
        db.session.commit()
        result = CourseSchema().dump(course)
        return result, 200

    def get(self, id):
        course = Course_model.query.filter_by(id=id).first()
        if not course:
            return {'message': 'Course not found'}, 404
        result = CourseSchema().dump(course)
        return result, 200

    def delete(self, id):
        course = Course_model.query.filter_by(id=id).first()
        if not course:
            return {'message': 'Course not found'}, 404
        Course_model.query.filter_by(id=id).delete()
        db.session.commit()
        return '', 204

@rest_api.route('/students/<int:student_id>/courses/')
class StudentCoursesList(Resource):
    def get(self, student_id):
        student = Student_model.query.filter_by(id=student_id).first()
        result = StudentCoursesSchema().dump(student)
        return result, 200

@rest_api.route('/students/<int:student_id>/courses/<int:course_id>')
class StudentCourses(Resource):
    def put(self, student_id, course_id):
        student = Student_model.query.filter_by(id=student_id).first()
        if not student:
            return {'message': 'Student not found'}, 404
        course = Course_model.query.filter_by(id=course_id).first()
        if not course:
            return {'message': 'Course not found'}, 404

        if course in student.courses:
            return {'message': 'Student already registered for the course'}, 200
        student.courses.append(course)
        #student_course = StudentCourse_model(student_id=student_id, course_id= course_id)
        #db.session.add(student_course)
        db.session.commit()
        return {'message': 'Course Registered'}, 204

@rest_api.route('/instructors/<int:instructor_id>/courses/')
class InstructorCourses(Resource):
    def get(self, instructor_id):
        instructor = Instructor_model.query.filter_by(id=instructor_id).first()
        if not instructor:
            return {'message': 'Instructor not found'}, 404
        result = InstructorCoursesSchema().dump(instructor)
        return result, 200


@rest_api.route('/instructors/<int:instructor_id>/courses/<int:course_id>')
class InstructorCourses(Resource):
    def put(self, instructor_id, course_id):
        instructor = Instructor_model.query.filter_by(id=instructor_id).first()
        if not instructor:
            return {'message': 'Instructor not found'}, 404
        course = Course_model.query.filter_by(id=course_id).first()
        if not course:
            return {'message': 'Course not found'}, 404
        course.instructor_id = instructor_id
        db.session.commit()
        return {'message': 'Course Assigned'}, 200
