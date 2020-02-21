from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, IntegerField, SelectField, \
    TextAreaField, BooleanField, FileField
from wtforms.fields.html5 import EmailField, URLField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Email, Optional, InputRequired, EqualTo
from app import CompanyCustomer
from models import PrivateCustomer
from utilities import COUNTRIES, TYPES

#
# def load_company_customer(id_company):
#     return CompanyCustomer.query.get(int(id_company))


class RegistrationFormPrivate(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', [InputRequired(), EqualTo('confirm_password', message='Passwords must match')])
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
    password = PasswordField('Password', [InputRequired(), EqualTo('confirm_password', message='Passwords must match')])
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


class OrderCreation(FlaskForm):
    product_name = StringField('Product name', validators=[DataRequired()])
    product_id = StringField('Product id', validators=[DataRequired()])
    order_description = TextAreaField('Insert a brief order description', validators=[DataRequired()])
    date_insert = DateField('This order has been added in the date', validators=[DataRequired()])
    date_request = DateField('This order has been required in the date', validators=[DataRequired()])
    date_delivery = DateField('Delivery day', validators=[DataRequired()])
    time_delivery = TimeField('Delivery time', validators=[DataRequired()])
    order_delivery_type = StringField('Delivery type')
    delivery_company = StringField('Delivery Company')
    submit = SubmitField('Create a new order')


class UploadForm(FlaskForm):
    file = FileField('Choose File', validators=[DataRequired()])
    upload = SubmitField('Upload')


class FormNextStep(FlaskForm):
    submit = SubmitField('Next Step')


class FormChat(FlaskForm):
    message = TextAreaField('Insert here your message...', validators=[DataRequired()])
    submit = SubmitField('Send')

