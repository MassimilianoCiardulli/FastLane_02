from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, validators, SubmitField, ValidationError, IntegerField, SelectField
from wtforms.fields.html5 import EmailField, URLField
from wtforms.validators import DataRequired, Length, Email, InputRequired
from app import PrivateCustomer, CompanyCustomer
from utilities import COUNTRIES


# @LoginManager.user_loader
# def load_private_customer(id):
#     return PrivateCustomer.query.get(int(id))


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

    def validate_email(self, email):
        email = PrivateCustomer.query.filter_by(email=self.email.data).first()
        if email:
            raise ValidationError('This email is already associated to another account.')


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
    submit = SubmitField('Register')

    def validate_username(self, name_company):
        name_company = CompanyCustomer.query.filter_by(name_company=self.name_company.data).first()
        if name_company:
            raise ValidationError('"%s" already exist, please select new username' % name_company.data)

    def validate_email(self, email):
        email = CompanyCustomer.query.filter_by(email=self.email.data).first()
        if email:
            raise ValidationError('This email is already associated to another account.')

    def validate_email_admin(self, email_admin):
        email_admin = CompanyCustomer.query.filter_by(email_admin=self.email_admin.data).first()
        if email_admin:
            raise ValidationError('This email is already associated to another account.')


class loginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=20)])
    submit = SubmitField('Login')


class RatingForm(FlaskForm):
    submit = SubmitField('Leave a review!')


class UpdateAccountFormPrivate(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=4, max=20)])
    email = EmailField('Email address', validators=[DataRequired(), Email()])
    phone = IntegerField('Phone number', validators=[DataRequired()])
    country = SelectField(choices=COUNTRIES)
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = PrivateCustomer.query.filter_by(username=self.username.data).first()
            if user:
                raise ValidationError('"%s" already exist, please select new username' % username.data)

    def validate_email(self, email):
        if email.data != current_user.email:
            email = PrivateCustomer.query.filter_by(email=self.email.data).first()
            if email != current_user.email:
                raise ValidationError('This email is already associated to another account.')


class UpdateAccountFormCompany(FlaskForm):
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
    submit = SubmitField('Update')

    def validate_username(self, name_company):
        if name_company.data != current_user.name_company:
            name_company = CompanyCustomer.query.filter_by(name_company=self.name_company.data).first()
            if name_company:
                raise ValidationError('"%s" already exist, please select new username' % name_company.data)

    def validate_email(self, email):
        if email.data != current_user.email:
            email = CompanyCustomer.query.filter_by(email=self.email.data).first()
            if email:
                raise ValidationError('This email is already associated to another account.')

    def validate_email_admin(self, email_admin):
        if email_admin.data != current_user.email_admin:
            email_admin = CompanyCustomer.query.filter_by(email_admin=self.email_admin.data).first()
            if email_admin:
                raise ValidationError('This email is already associated to another account.')
