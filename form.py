from flask import request
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, ValidationError, IntegerField, SelectField, \
    TextAreaField, FloatField, BooleanField, FileField
from wtforms.fields.html5 import EmailField, URLField, DateTimeField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Email, Optional
from app import PrivateCustomer, CompanyCustomer
from models import Product
from utilities import COUNTRIES, TYPES


def load_company_customer(id_company):
    return CompanyCustomer.query.get(int(id_company))


class RegistrationFormPrivate(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=4, max=20)])
    email = EmailField('Email address', validators=[DataRequired(), Email()])
    phone = IntegerField('Phone number', validators=[DataRequired()])
    country = SelectField(choices=COUNTRIES)
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = PrivateCustomer.query.filter_by(username=self.username.data).first()
        if user:
            raise ValidationError('"%s" already exist, please select new username' % username.data)


class RegistrationFormCompany(FlaskForm):
    name_company = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=4, max=20)])
    email = EmailField('Email address', validators=[DataRequired(), Email()])
    email_admin = EmailField('Administrator email address', validators=[DataRequired(), Email()])
    phone = IntegerField('Phone number', validators=[DataRequired()])
    country = SelectField(choices=COUNTRIES)
    city = StringField('City', validators=[DataRequired()])
    vat_code = StringField('VAT code', validators=[DataRequired()])
    web_site = URLField('Web site', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    supplier = BooleanField('Are you a supplier?', validators=[Optional()])
    customer = BooleanField('Are you a buyer?', validators=[Optional()])
    submit = SubmitField('Register')

    def validate_username(self, name_company):
        name_company = CompanyCustomer.query.filter_by(name_company=self.name_company.data).first()
        if name_company:
            raise ValidationError('"%s" already exist, please select new username' % name_company.data)

    # def validate_email(self, email):
    #     email = CompanyCustomer.query.filter_by(email=self.email.data).first()
    #     if email:
    #         raise ValidationError('This email is already associated to another account.')
    #
    # def validate_email_admin(self, email_admin):
    #     email_admin = CompanyCustomer.query.filter_by(email_admin=self.email_admin.data).first()
    #     if email_admin:
    #         raise ValidationError('This email is already associated to another account.')

    def validate_checkbox(self):
        if request.form.get('supplier') is False and request.form.get('customer') is False:
            raise ValidationError("Please select if you're a seller or a buyer or both")



class loginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=20)])
    submit = SubmitField('Login')


class loginEmployeeForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=20)])
    submit = SubmitField('Login')

class subRegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=20)])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), Length(min=4, max=20)])
    role = SelectField(choices=[('Manager', 'Manager'), ('Employee', 'Employee')])
    department = SelectField(choices=[('Production', 'Production'), ('Design', 'Design'), ('Prototype', 'Prototype')])
    submit = SubmitField('Sign up')


class RatingForm(FlaskForm):
    review = TextAreaField()
    id_reviewer = StringField("Your name (if you're a Company) or username (if you're a private customer):", validators=[DataRequired()])
    type = SelectField('You are a...', choices=TYPES)
    submit = SubmitField('Give us a feedback')

    def validate_reviewer(self, id_reviewer):
        if not PrivateCustomer.query.filter_by(username=self.id_reviewer.data).first() and not CompanyCustomer.query.filter_by(name_company=self.id_reviewer.data).first():
            ValidationError('"%s" does not exist, please insert a valid name or username' % id_reviewer.data)


class RegistrationProduct(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    type = StringField('Type', validators=[DataRequired()])
    availability = StringField('Availability', validators=[DataRequired()])
    price = FloatField('Price',validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_product(self, name):
        if Product.query.filter_by(username=self.name.data).first():
            ValidationError('"%s" already exists' % name.data)


class OrderCreation(FlaskForm):
    product_name = StringField('Product name', validators=[DataRequired()])
    product_id = StringField('Product id', validators=[DataRequired()])
    customer_id = StringField('Customer id', validators=[DataRequired()])
    departments = StringField('Insert departments', validators=[DataRequired()])
    order_description = TextAreaField('Insert a brief order description', validators=[DataRequired()])
    date_insert = DateField('This order has been added in the date', validators=[DataRequired()])
    date_request = DateField('This order has been required in the date', validators=[DataRequired()])
    date_delivery = DateField('Delivery day', validators=[DataRequired()])
    time_delivery = TimeField('Delivery time', validators=[DataRequired()])
    order_delivery_type = StringField('Delivery type')
    delivery_company = StringField('Delivery Company')
    submit = SubmitField('Create a new order')


class UploadForm(FlaskForm):
    file = FileField('file',validators=[DataRequired()])
    upload=SubmitField('upload')

#
# class UpdateAccountFormPrivate(FlaskForm):
#     name = StringField('Name', validators=[DataRequired()])
#     username = StringField('Username', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=20)])
#     confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=4, max=20)])
#     email = EmailField('Email address', validators=[DataRequired(), Email()])
#     phone = IntegerField('Phone number', validators=[DataRequired()])
#     country = SelectField(choices=COUNTRIES)
#     address = StringField('Address', validators=[DataRequired()])
#     submit = SubmitField('Update')
#
#     def validate_username(self, username):
#         if username.data != current_user.username:
#             user = PrivateCustomer.query.filter_by(username=self.username.data).first()
#             if user:
#                 raise ValidationError('"%s" already exist, please select new username' % username.data)
#
#     def validate_email(self, email):
#         if email.data != current_user.email:
#             email = PrivateCustomer.query.filter_by(email=self.email.data).first()
#             if email != current_user.email:
#                 raise ValidationError('This email is already associated to another account.')
#
#
# class UpdateAccountFormCompany(FlaskForm):
#     name_company = StringField('Name', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=20)])
#     confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=4, max=20)])
#     email = EmailField('Email address', validators=[DataRequired(), Email()])
#     email_admin = EmailField('Administrator email address', validators=[DataRequired(), Email()])
#     phone = IntegerField('Phone number', validators=[DataRequired()])
#     country = SelectField(choices=COUNTRIES)
#     city = StringField('City', validators=[DataRequired()])
#     vat_code = StringField('VAT code', validators=[DataRequired()])
#     web_site = URLField('Web site', validators=[DataRequired()])
#     address = StringField('Address', validators=[DataRequired()])
#     supplier = BooleanField('Are you a supplier?')
#     customer = BooleanField('Are you a buyer?')
#     submit = SubmitField('Update')
#
#     def validate_username(self, name_company):
#         if name_company.data != current_user.name_company:
#             name_company = CompanyCustomer.query.filter_by(name_company=self.name_company.data).first()
#             if name_company:
#                 raise ValidationError('"%s" already exist, please select new username' % name_company.data)
#
#     def validate_email(self, email):
#         if email.data != current_user.email:
#             email = CompanyCustomer.query.filter_by(email=self.email.data).first()
#             if email:
#                 raise ValidationError('This email is already associated to another account.')
#
#     def validate_email_admin(self, email_admin):
#         if email_admin.data != current_user.email_admin:
#             email_admin = CompanyCustomer.query.filter_by(email_admin=self.email_admin.data).first()
#             if email_admin:
#                 raise ValidationError('This email is already associated to another account.')
