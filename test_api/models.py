from test_api import db
from datetime import datetime


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(40), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    joining_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    orders = db.relationship('Order', backref='customer', lazy=True)


OrderBook = db.Table('order_book',
                              db.Column('id',
                                        db.Integer,
                                        primary_key=True),
                              db.Column('order_id',
                                        db.Integer,
                                        db.ForeignKey('order.id', ondelete="cascade")),
                              db.Column('book_id',
                                        db.Integer,
                                        db.ForeignKey('book.id', ondelete="cascade")))


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    customer_id = db.Column('customer_id', db.Integer, db.ForeignKey("customer.id", ondelete='CASCADE'), nullable=True)
    books = db.relationship('Book', secondary=OrderBook, backref='orders', lazy=True)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(20), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    year_written = db.Column(db.Integer, nullable=False)
    #orders = db.relationship('Order', backref='customer', lazy=True)