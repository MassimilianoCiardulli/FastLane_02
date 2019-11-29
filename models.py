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
    order_id = db.relationship('Order', backref='private_costumer')

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
    supplier = db.Column(db.Boolean, index=True)
    customer = db.Column(db.Boolean, index=True)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    order_id = db.relationship('Order', backref='company_costumer')
    employee = db.relationship('CompanyUser', backref='company_customer')

    def __repr__(self):
        return '<Customer %s>' % self.name_company


class CompanyUser(db.Model):
    __tablename__='company_employee'
    username = db.Column(db.String(64), primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company_customer.id_company'))
    name = db.Column(db.String(64), nullable=False)
    surname = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(64), nullable=False)
    department = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return '<CompanyUser %s>' % self.username


class CompanyDelivery(db.Model):
    __tablename__ = 'company_delivery'
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
    order_id = db.relationship('Order', backref='company_delivery')

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
    __tablename__ = 'products'
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(64), nullable=False)
    product_quantity = db.Column(db.Integer, nullable=True, index=True)
    product_price = db.Column(db.Integer, nullable=False, index=True)
    product_type = db.Column(db.String, index=True) #raw material, ecc
    product_availability = db.Column(db.Boolean, default=False)
    order_product_id = db.Column(db.Integer, db.ForeignKey('order_product.id'))

    def __repr__(self):
        return '<Product %s>' % self.product_name


class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_description = db.Column(db.String(64), nullable=False)
    order_delivery_date = db.Column(db.Date, nullable=False, index=True)
    order_delivery_time = db.Column(db.Time, nullable=False, index=True)
    order_delivery_type = db.Column(db.String(64), index=True)
    order_delivery_company = db.Column(db.Integer, db.ForeignKey('company_delivery.id_company'))
    order_state = db.Column(db.String(64), nullable=False)
    order_private_customer = db.Column(db.Integer, db.ForeignKey('private_costumer.id'))
    order_company_customer = db.Column(db.Integer, db.ForeignKey('company_customer.id_company'))
    departments = db.Column(db.String(64), nullable=False)
    user = db.Column(db.String(64), nullable=False)
    date_insert = db.Column(db.DateTime, nullable=False)
    date_request = db.Column(db.DateTime, nullable=False)
    order_product_id = db.Column(db.Integer, db.ForeignKey('order_product.id'))

    def __repr__(self):
        return '<Order %s>' % self.order_id


class OrderProduct(db.Model):
    __tablename__ = 'order_product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.relationship('Order', backref='order_product')
    product_id = db.relationship('Product', backref='order_product')

    def __repr__(self):
        return '<Order_Product %s>' % self.id


class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department_name = db.Column(db.String(64), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company_customer.id_company'))

    def __repr__(self):
        return '<Department %s>' %self.id