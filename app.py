from flask import render_template, redirect, session
from flask_bootstrap import Bootstrap
from sqlalchemy_utils import database_exists
from flask_bcrypt import Bcrypt
from models import app, db, CompanyCustomer, PrivateCustomer, Rating, Product, Order, CompanyUser
from form import RegistrationFormPrivate, loginForm, RegistrationFormCompany, RatingForm, RegistrationProduct, \
    OrderCreation, subRegistrationForm, loginEmployeeForm

app.config['SECRET_KEY'] = 'ldjashfjahef;jhasef;jhase;jfhae;'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fastlane.db'

Bootstrap(app)
bcrypt = Bcrypt(app)

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
    if form_company.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form_company.password.data)
        new_customer = CompanyCustomer(name_company=form_company.name_company.data, password=hashed_pwd,
                                       email=form_company.email.data, phone_num=form_company.phone.data,
                                       city=form_company.city.data,
                                       address=form_company.address.data, vat_code=form_company.vat_code.data,
                                       country=form_company.country.data,
                                       web_site=form_company.web_site.data, email_amm=form_company.email_admin.data,
                                       type='Company', supplier=form_company.supplier.data, customer=form_company.customer.data)
        db.session.add(new_customer)
        db.session.commit()
        return redirect('login')
    return render_template('reg_company.html', formReg=form_company)


@app.route('/register_company_employee', methods=['POST', 'GET'])
def register_employee():
    form_employee = subRegistrationForm()
    if form_employee.is_submitted():
        hashed_pwd = bcrypt.generate_password_hash(form_employee.password.data)
        new_employee = CompanyUser(username=form_employee.username.data, password=hashed_pwd,
                                       name=form_employee.name.data, surname=form_employee.surname.data,
                                       role=form_employee.role.data,
                                       department=form_employee.department.data)
        db.session.add(new_employee)
        db.session.commit()
        return redirect('login_company_employee')
    return render_template('subregistration_company.html', form_employee=form_employee)


@app.route('/login_company_employee', methods=['POST', 'GET'])
def login_employee():
    form_login_employee = loginEmployeeForm()
    if form_login_employee.is_submitted():
        user_selected = CompanyUser.query.filter_by(username=form_login_employee.username.data).first()
        if CompanyUser.query.filter_by(username=form_login_employee.username.data).first() and bcrypt.check_password_hash(
                user_selected.password, form_login_employee.password.data):
            session['email_user'] = user_selected.username
            session['name_employee'] = user_selected.name
            session['role_employee'] = user_selected.role
            return redirect('order')
        else:
            error = 'ERROR: username or password should be incorrect. Please Try again'
    return render_template('sublogin_company.html', form_login_employee=form_login_employee)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if session.get('email'):
        return redirect('order')
    else:
        formLog = loginForm()
        if formLog.validate_on_submit():
            customer_selected = CompanyCustomer.query.filter_by(email=formLog.email.data).first()
            if CompanyCustomer.query.filter_by(email=formLog.email.data).first():
                if bcrypt.check_password_hash(customer_selected.password, formLog.password.data):
                    session['email'] = customer_selected.email
                    session['id_user'] = customer_selected.name_company
                    session['type'] = 'COMPANY'
                    return redirect('register_company_employee')
                else:
                    error = 'ERROR: username or password should be incorrect. Please Try again'
                    return redirect('login')
            elif PrivateCustomer.query.filter_by(email=formLog.email.data).first():
                customer_selected = PrivateCustomer.query.filter_by(email=formLog.email.data).first()
                if bcrypt.check_password_hash(customer_selected.password, formLog.password.data):
                    session['email'] = customer_selected.email
                    session['id_user'] = customer_selected.name
                    session['type'] = 'PRIVATE'
                    return redirect('order')
                else:
                    error = 'ERROR: username or password should be incorrect. Please Try again'
                    return redirect('login')
        return render_template('login.html', formLog=formLog)


@app.route('/logout')
def logout():
    session_exists = True
    session.pop('email')
    session.pop('id_user')
    session.pop('type')

    try:
        session['email']
    except KeyError:
        session_exists = False

    if not session_exists:
        return redirect('home')
    return render_template('logout.html')


@app.route('/company_member_logout')
def company_member_logout():
    session_exists = True
    session.pop('email_user')
    session.pop('name_employee')
    session.pop('role_employee')

    try:
        session['email_user']
    except KeyError:
        session_exists = False

    if not session_exists:
        return redirect('home')
    return render_template('logout.html')


@app.route('/feedback', methods=['POST', 'GET'])
def feedback():
    form_rating = RatingForm()
    if form_rating.is_submitted():
        new_review = Rating(id_reviewer=form_rating.id_reviewer.data, type=form_rating.type.data,
                            review=form_rating.review.data)
        db.session.add(new_review)
        db.session.commit()
        return redirect('home')
    return render_template('feedback.html', form_rating=form_rating)


@app.route('/order')
def order():
    if session['type'] == 'COMPANY':
        orders = Order.query.filter_by(user=session['id_user']).all()
    elif session['type'] == 'PRIVATE':
        orders = Order.query.filter_by(order_private_customer=session['id_user']).all()
    return render_template('order.html', orders=orders)


@app.route('/order_creation', methods=['POST', 'GET'])
def order_creation():
    form_order_creation = OrderCreation()
    if form_order_creation.is_submitted():
        new_order = Order(order_description=form_order_creation.order_description.data, order_delivery_type=form_order_creation.order_delivery_type.data,
                          order_delivery_date=form_order_creation.date_delivery.data, order_delivery_time=form_order_creation.time_delivery.data,
                          order_delivery_company=form_order_creation.delivery_company.data, order_state='TO BE STARTED',
                          order_private_customer=form_order_creation.customer_id.data, departments=form_order_creation.departments.data,
                          user=session['id_user'], date_insert=form_order_creation.date_insert.data, date_request=form_order_creation.date_request.data)
        db.session.add(new_order)
        db.session.commit()
        return redirect('home')
    return render_template('order_creation.html', form_order_creation=form_order_creation)


@app.route('/register_product', methods=['POST', 'GET'])
def register_product():
    form_product = RegistrationProduct()
    if form_product.validate_on_submit():
        new_product = Product(name=form_product.name.data, quantity=form_product.quantity.data,
                              price=form_product.price.data,
                              availability=form_product.availability.data,
                              type=form_product.type.data)
        db.session.add(new_product)
        db.session.commit()
        return redirect('order.html')
    return render_template('reg_product.html', formReg=form_product)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run()
