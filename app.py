import os
from hashlib import md5
from flask import Flask, render_template, redirect, session, flash, url_for, request
from flask_bootstrap import Bootstrap
from flask_login import current_user
from sqlalchemy_utils import database_exists
from flask_bcrypt import Bcrypt
from PIL import Image
from models import app, db, CompanyCustomer, PrivateCustomer, Rating

app.config['SECRET_KEY'] = 'ldjashfjahef;jhasef;jhase;jfhae;'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fastlane.db'

Bootstrap(app)
bcrypt = Bcrypt(app)


from form import RegistrationFormPrivate, loginForm, RegistrationFormCompany, UpdateAccountFormPrivate, \
    UpdateAccountFormCompany, RatingForm


@app.before_first_request
def create_all():
    if not database_exists('sqlite:///fastlane.db'):
        db.create_all()
        db.session.commit()


@app.route('/register_private', methods=['POST', 'GET'])
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    form_private = RegistrationFormPrivate()
    if form_private.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form_private.password.data)
        new_customer = PrivateCustomer(name=form_private.name.data, username=form_private.username.data,
                                       password=hashed_pwd, email=form_private.email.data,
                                       phone_num=form_private.phone.data,
                                       address=form_private.address.data,
                                       country=form_private.country.data,
                                       type='Private')
        db.session.add(new_customer)
        db.session.commit()
        return redirect('login')
    return render_template('reg_private.html', formReg=form_private)


@app.route('/register_company', methods=['POST', 'GET'])
def register_company():
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    form_company = RegistrationFormCompany()
    if form_company.is_submitted():
        hashed_pwd = bcrypt.generate_password_hash(form_company.password.data)
        new_customer = CompanyCustomer(name_company=form_company.name_company.data, password=hashed_pwd,
                                       email=form_company.email.data, phone_num=form_company.phone.data,
                                       city=form_company.city.data,
                                       address=form_company.address.data, vat_code=form_company.vat_code.data,
                                       country=form_company.country.data,
                                       web_site=form_company.web_site.data, email_amm=form_company.email_admin.data,
                                       type='Company')
        db.session.add(new_customer)
        db.session.commit()
        return redirect('login')
    return render_template('reg_company.html', formReg=form_company)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if session.get('email'):
        return redirect('profile_private')
    else:
        formRed = loginForm()
        if formRed.validate_on_submit():
            customer_selected = CompanyCustomer.query.filter_by(email=formRed.email.data).first()
            if bcrypt.check_password_hash(customer_selected.password, formRed.password.data):
                session['email'] = customer_selected.email
                return redirect('profile_private')
            else:
                error = 'ERROR: username or password should be incorrect. Please Try again'
                return redirect('login.html')
        return render_template('login.html', formReg=formRed)


@app.route('/feedback', methods=['POST', 'GET'])
def feedback():
    form_rating = RatingForm()
    if form_rating.is_submitted():
        new_review = Rating(id_reviewer=form_rating.id_reviewer.data, type=form_rating.type.data, review=form_rating.review.data)
        db.session.add(new_review)
        db.session.commit()
        return redirect('home')
    return render_template('feedback.html', form_rating=form_rating)


@app.route('/', )
@app.route('/home')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run()
