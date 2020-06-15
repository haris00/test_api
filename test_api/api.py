from test_api import rest_api
from test_api.models import Customer as customer_model, Order as order_model, Book as book_model
from test_api.schema import CustomerSchema as customer_schema, CustomerEditSchema as customer_edit_schema, \
    BookSchema as book_schema, BookEditSchema as book_edit_schema, CustomerOrder as customer_order_schema, \
    CustomerOrderList as customer_order_list_schema
from test_api import db
from flask import request
from flask_restplus import Resource, fields, reqparse, inputs
from sqlalchemy.orm import load_only
from functools import wraps
import re
from datetime import date, datetime


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = None

        if 'X-API-KEY' in request.headers:
            token = request.headers['X-API-KEY']

        if not token:
            return {'message' : 'Token is missing.'}, 401

        if token != 'mytoken':
            return {'message' : 'Your token is wrong, wrong, wrong!!!'}, 401

        print('TOKEN: {}'.format(token))
        return f(*args, **kwargs)

    return decorated


@rest_api.route('/customers')
class CustomersList(Resource):
    def post(self):
        data = request.get_json(force=True)
        errors = customer_schema().validate(data)
        if errors:
            return errors, 422
        customer = customer_model.query.filter_by(name=data['name']).first()
        if customer:
            return {'message': 'Customer already exists'}, 400
        new_customer = customer_model()
        for k, v in data.items():
            if v is not None:
                setattr(new_customer, k, v)
        db.session.add(new_customer)
        db.session.commit()
        result = customer_schema().dump(new_customer)
        return result, 201

    @token_required
    def get(self):
        instructors = customer_model.query.all()
        result = customer_schema(many=True).dump(instructors)
        return result, 200


@rest_api.route('/customers/<int:id>')
class Customers(Resource):

    def put(self, id):
        data = request.get_json(force=True)
        errors = customer_edit_schema().validate(data)
        if errors:
            return errors, 422
        customer = customer_model.query.filter_by(id=id).first()
        if not customer:
            return {'message': 'Customer not found'}, 404
        for k, v in data.items():
            if v is not None:
                setattr(customer, k, v)
        db.session.add(customer)
        db.session.commit()
        result = customer_schema().dump(customer)
        return result, 200

    def get(self, id):
        customer = customer_model.query.filter_by(id=id).first()
        if not customer:
            return {'message': 'Customer not found'}, 404
        result = customer_schema().dump(customer)
        return result, 200

    def delete(self, id):
        customer = customer_model.query.filter_by(id=id).first()
        if not customer:
            return {'message': 'Customer not found'}, 404
        customer_model.query.filter_by(id=id).delete()
        db.session.commit()
        return '', 204




#################################################################33

@rest_api.route('/books')
class BooksList(Resource):
    def post(self):
        data = request.get_json(force=True)
        errors = book_schema().validate(data)
        if errors:
            return errors, 422
        book = book_model.query.filter_by(author=data['author']).first()
        if book:
            return {'message': 'Customer already exists'}, 400
        new_book = book_model()
        for k, v in data.items():
            if v is not None:
                setattr(new_book, k, v)
        db.session.add(new_book)
        db.session.commit()
        result = book_schema().dump(new_book)
        return result, 201

    def get(self):
        parser = reqparse.RequestParser()
        allowed_fields = ["id", "author"]
        parser.add_argument('fields', type=str, action="split", location='args',default=None)
                            #choices=allowed_fields)
        parser.add_argument('limit', type=int, location='args',default=3)
        parser.add_argument('offset', type=int, location='args',default=0)
        parser.add_argument('sort', type=str, location='args',default=None, choices=allowed_fields)

        args = parser.parse_args()
        limit = args['limit']
        offset = args['offset']
        sort = args['sort']
        all_fields = args['fields']
        books = book_model.query.offset(offset).limit(limit)
        if all_fields:
            books = books.options(load_only("id", "author"))

        if sort:
            books = book_model.query.order_by(sort)
            #.order_by("name desc")
        result = book_schema(many=True).dump(books.all())
        return result, 200


@rest_api.route('/books/<int:id>')
class Books(Resource):

    def put(self, id):
        data = request.get_json(force=True)
        errors = book_edit_schema().validate(data)
        if errors:
            return errors, 422
        book = book_model.query.filter_by(id=id).first()
        if not book:
            return {'message': 'Book not found'}, 404
        for k, v in data.items():
            if v is not None:
                setattr(book, k, v)
        db.session.add(book)
        db.session.commit()
        result = book_schema().dump(book)
        return result, 200

    def get(self, id):
        book = book_model.query.filter_by(id=id).first()
        if not book:
            return {'message': 'Book not found'}, 404
        result = book_schema().dump(book)
        return result, 200

    def delete(self, id):
        book = book_model.query.filter_by(id=id).first()
        if not book:
            return {'message': 'Book not found'}, 404
        book_model.query.filter_by(id=id).delete()
        db.session.commit()
        return '', 204


##############################################################
@rest_api.route('/customers/<int:customer_id>/orders')
class CustomerOrdersList(Resource):

    def post (self, customer_id):
        data = request.get_json(force=True)
        errors = customer_order_schema().validate(data)
        if errors:
            return errors, 422
        customer = customer_model.query.filter_by(id=customer_id).first()
        if not customer:
            return {'message': 'Customer not found'}, 404
        new_order = order_model(customer_id=customer_id)
        for requested_book in data['books']:
            book = book_model.query.filter_by(id=requested_book['id']).first()
            if not book:
                return {'message': 'Book id {0} not found'.format(requested_book['id'])}, 404
            if book.stock < requested_book['stock']:
                return {'message': 'Book id {0} not enough books available'.format(book['book_id'])}, 404
            book.stock = book.stock - requested_book['stock']
            db.session.add(book)
            new_order.books.append(book)

        db.session.add(new_order)
        db.session.commit()
        result = customer_order_schema().dump(new_order)
        return result, 200

    def get(self, customer_id):
        customer = customer_model.query.filter_by(id=customer_id).first()
        if not customer:
            return {'message': 'Customer not found'}, 404
        result = customer_order_list_schema().dump(customer)
        return result, 200


@rest_api.route('/orders')
class OrdersList(Resource):
    def get(self):
        orders = order_model.query.all()
        result = customer_order_schema(many=True).dump(orders)
        return result, 200

@rest_api.route('/orders/<int:order_id>')
class Orders(Resource):
    def delete(self, order_id):
        order = order_model.query.filter_by(id=order_id)
        if not order:
            return {'message': 'Order not found'}, 404
        order.delete()
        db.session.commit()
        return '',204

# @rest_api.route('/customers/<int:customer_id>/orders/<int:order_id>')
# class CustomerOrders(Resource):
#     # def get(self, customer_id, order_id):
#     #     customer = customer_model.query.filter_by(id=customer_id).first()
#     #     if not customer:
#     #         return {'message': 'Customer not found'}, 404
#     #     customer = customer_model.query.filter_by(id=customer_id).first()
#     #     if not customer:
#     #         return {'message': 'Customer not found'}, 404
#
#     def delete(self, customer_id, order_id):
#         customer = customer_model.query.filter_by(id=customer_id).first()
#         if not customer:
#             return {'message': 'Customer not found'}, 404
#         order = order_model.query.filter_by(id=order_id).first()
#

# @rest_api.route('/students/<int:student_id>/courses/<int:course_id>')
# class StudentCourses(Resource):
#     def put(self, student_id, course_id):
#         student = Student_model.query.filter_by(id=student_id).first()
#         if not student:
#             return {'message': 'Student not found'}, 404
#         course = Course_model.query.filter_by(id=course_id).first()
#         if not course:
#             return {'message': 'Course not found'}, 404
#
#         if course in student.courses:
#             return {'message': 'Student already registered for the course'}, 200
#         student.courses.append(course)
#         #student_course = StudentCourse_model(student_id=student_id, course_id= course_id)
#         #db.session.add(student_course)
#         db.session.commit()
#         return {'message': 'Course Registered'}, 204
