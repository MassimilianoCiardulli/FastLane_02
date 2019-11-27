from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)


db = SQLAlchemy(app)


class PrivateCustomer(db.Model):
    __tablename__ = 'private_costumer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    phone_num = db.Column(db.Integer, nullable=False, unique=True)
    country = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(64), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    type = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return '<Customer %s>' % self.username


class CompanyCustomer(db.Model):
    __tablename__ = 'company_customer'
    id_company = db.Column(db.Integer, primary_key=True)
    name_company = db.Column(db.String(64), nullable=True)
    country = db.Column(db.String(64), nullable=False)
    city = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(128), nullable=False)
    vat_code = db.Column(db.String(64), index=True, unique=True)
    web_site = db.Column(db.String(64), unique=True)
    phone_num = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(64), unique=True)
    email_amm = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(64), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    def __repr__(self):
        return '<Customer %s>' % self.username_company


class Rating(db.Model):
    __tablename__ = 'ratings'
    id_review = db.Column(db.Integer, primary_key=True)
    id_reviewer = db.Column(db.String(64), nullable=False)
    type = db.Column(db.String(64), nullable=False)
    review = db.Column(db.String(128))

    def __repr__(self):
        return '<Review %s>' % self.id_review


class Product(db.Model):
    _tablename_ = 'products'
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(64), nullable=False)
    product_quantity = db.Column(db.Integer, nullable=True, index=True)
    product_price = db.Column(db.Integer, nullable=False, index=True)
    product_type = db.Column(db.String, index=True)
    product_availability = db.Column(db.Boolean, default=False)

    def _repr_(self):
        return '<Product %s>' % self.product_name


class Order(db.Model):
    _tablename_ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_description = db.Column(db.String(64), nullable=False)
    order_delivery_date = db.Column(db.Date, nullable=False, index=True)
    order_delivery_time = db.Column(db.Time, nullable=False, index=True)
    order_delivery_type = db.Column(db.String(64), index=True)
    order_delivery_company = db.ForeignKey('company_customer.id_company')
    order_state = db.Column(db.String(64), nullable=False)
    order_private_customer = db.ForeignKey('private_customer.id')
    order_company_customer = db.ForeignKey('company_customer.id_company')

    def _repr_(self):
        return '<Order %s>' % self.order_id


class OrderProduct(db.Model):
    _tablename_ = 'order_product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.ForeignKey('orders.order_id')
    product_id = db.ForeignKey('products.product_id')

    def _repr_(self):
        return '<Order_Product %s>' % self.id


# class DeliveryCompany(db.Model):
#     _tablename_ = 'delivery_company'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(64), index=True, unique=True)
#     vat_code = db.Column(db.String(64), index=True, unique=True)
#     order = db.relationship('Order', backref='delivery_company')
#
#     def _repr_(self):
#         return '<Delivery company %s>' % self.id
#
