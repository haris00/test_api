from test_api import ma
from marshmallow import fields, validate

class InstructorSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    title = fields.String(required=True,validate=validate.OneOf(['dr','prof','associate']))
    #courses = fields.Nested("CourseSchema", many=True)
    # class Meta:
    #     # model = Instructor
    #     fields = ('id','name')

class InstructorCoursesSchema(InstructorSchema):
    courses = fields.Nested("CourseSchema", many=True)

class StudentSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    program = fields.String(required=True,validate=validate.OneOf(['bachelors','masters','phd']))
    # class Meta:
    #     # model = Instructor
    #     fields = ('id','name','program')


class CourseSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    course_level = fields.String(required=True,validate=validate.OneOf(['bachelors','masters','phd']))
    max_capacity = fields.Integer()
    current_students = fields.Integer()
    # Can have the these too only=("name", "username", "roles", "image"), many=True
    #instructor = fields.Nested("InstructorSchema")


class CourseInstructorSchema(CourseSchema):
    # Can have the these too only=("name", "username", "roles", "image"), many=True
    instructor = fields.Nested("InstructorSchema")


# class StudentCoursesCourse(ma.Schema):
#     course = fields.Nested("CourseSchema")
#

class StudentCoursesSchema(StudentSchema):
    courses = fields.Nested("CourseSchema", many=True)