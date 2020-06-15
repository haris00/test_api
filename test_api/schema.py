from test_api import ma
from marshmallow import fields, validate
from test_api.constants import  VALID_ORDER_STATUS

class CustomerSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    email = fields.Email(required=True)
    phone = fields.String(required=True)
    joining_date = fields.Date()

class CustomerEditSchema(ma.Schema):
    name = fields.String()
    email = fields.Email()
    phone = fields.String()


class BookSchema(ma.Schema):
    id = fields.Integer()
    author = fields.String(required=True)
    price = fields.Integer(required=True)
    stock = fields.Integer(required=True)
    year_written = fields.Integer(required=True)


class BookEditSchema(ma.Schema):
    author = fields.String()
    price = fields.Integer()
    stock = fields.Integer()

class BookOrderSchema (ma.Schema):
    id = fields.Integer(required=True)
    stock = fields.Integer(required=True)


class CustomerOrder(ma.Schema):
    #status = fields.String(required=True,validate=validate.OneOf(VALID_ORDER_STATUS))
    id = fields.Integer()
    books = fields.Nested("BookOrderSchema", many=True, required=True)
    date_created = fields.Date()


class CustomerOrderList(ma.Schema):
    orders = fields.Nested("CustomerOrder", many=True)
