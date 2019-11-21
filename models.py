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