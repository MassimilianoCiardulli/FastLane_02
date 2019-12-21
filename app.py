import os, datetime
from flask import render_template, redirect, session, flash, request, url_for
from flask_bootstrap import Bootstrap
from sqlalchemy.exc import IntegrityError
from sqlalchemy_utils import database_exists
from flask_bcrypt import Bcrypt
from models import app, db, CompanyCustomer, PrivateCustomer, Rating, Product, Order, CompanyUser, Department, \
    MessageWithCustomer, MessageWithDepartment
from form import RegistrationFormPrivate, loginForm, RegistrationFormCompany, RatingForm, RegistrationProduct, \
    OrderCreation, subRegistrationForm, loginEmployeeForm, UploadForm, FormNextStep, FormChat
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from sqlalchemy import or_
from werkzeug.utils import secure_filename

app.config['SECRET_KEY'] = 'ldjashfjahef;jhasef;jhase;jfhae;'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fastlane.db'
UPLOAD_FOLDER = os.getcwd()+'/static/uploaded_file'

Bootstrap(app)
bcrypt = Bcrypt(app)

app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd()+"/static"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

photos = UploadSet('photos', IMAGES)
#media = UploadSet('media', default_dest=lambda app: app.instance_path)
configure_uploads(app, photos)
patch_request_class(app)


CUSTOMERS = 0

@app.before_first_request
def create_all():
    if not database_exists('sqlite:///fastlane.db'):
        db.create_all()
        db.session.add(Department(department_name='Design'))
        db.session.add(Department(department_name='Production'))
        db.session.add(Department(department_name='Prototype'))
        db.session.commit()


@app.route('/register_private', methods=['POST', 'GET'])
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    form_private = RegistrationFormPrivate()
    if form_private.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form_private.password.data)
        new_customer = PrivateCustomer(name=form_private.name.data.upper(), username=form_private.username.data.upper(),
                                       password=hashed_pwd, email=form_private.email.data.upper(),
                                       phone_num=form_private.phone.data,
                                       address=form_private.address.data.upper(),
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
        new_customer = CompanyCustomer(name_company=form_company.name_company.data.upper(), password=hashed_pwd,
                                       email=form_company.email.data.upper(), phone_num=form_company.phone.data,
                                       city=form_company.city.data,
                                       address=form_company.address.data.upper(), vat_code=form_company.vat_code.data,
                                       country=form_company.country.data,
                                       web_site=form_company.web_site.data, email_amm=form_company.email_admin.data.upper(),
                                       type='Company', supplier=form_company.supplier.data, customer=form_company.customer.data)
        db.session.add(new_customer)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('Data inserted is already registered in another account, please modified your data.', "Warning")
            return render_template('reg_company.html', formReg=form_company)

        return redirect('login')
    else:
        return render_template('reg_company.html', formReg=form_company)


@app.route('/register_company_employee', methods=['POST', 'GET'])
def register_employee():
    form_employee = subRegistrationForm()
    if form_employee.is_submitted():
        hashed_pwd = bcrypt.generate_password_hash(form_employee.password.data)
        new_employee = CompanyUser(username=form_employee.username.data.upper(), password=hashed_pwd,
                                       company_id=session['id_user'],
                                       name=form_employee.name.data.upper(), surname=form_employee.surname.data.upper(),
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
        user_selected = CompanyUser.query.filter_by(username=form_login_employee.username.data.upper()).first()
        if CompanyUser.query.filter_by(username=form_login_employee.username.data.upper()).first() and bcrypt.check_password_hash(
                user_selected.password, form_login_employee.password.data):
            session['username_user'] = user_selected.username.upper()
            session['name_employee'] = user_selected.name.upper()
            session['role_employee'] = user_selected.role
            session['department_employee'] = user_selected.department
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
            customer_selected = CompanyCustomer.query.filter_by(email=formLog.email.data.upper()).first()
            if CompanyCustomer.query.filter_by(email=formLog.email.data.upper()).first():
                if bcrypt.check_password_hash(customer_selected.password, formLog.password.data):
                    session['email'] = customer_selected.email.upper()
                    session['id_user'] = customer_selected.name_company.upper()
                    session['type'] = 'COMPANY'
                    return redirect('login_company_employee')
                else:
                    error = 'ERROR: username or password should be incorrect. Please Try again'
                    return redirect('login')
            elif PrivateCustomer.query.filter_by(email=formLog.email.data.upper()).first():
                customer_selected = PrivateCustomer.query.filter_by(email=formLog.email.data.upper()).first()
                if bcrypt.check_password_hash(customer_selected.password, formLog.password.data):
                    session['email'] = customer_selected.email.upper()
                    session['id_user'] = customer_selected.name.upper()
                    session['username'] = customer_selected.username.upper()
                    session['type'] = 'PRIVATE'
                    return redirect('order')
                else:
                    error = 'ERROR: username or password should be incorrect. Please Try again'
                    return redirect('login')
        return render_template('login.html', formLog=formLog)


@app.route('/logout')
def logout():
    session_exists = True
    session_employee_exists = True
    session.pop('email')
    session.pop('id_user')
    session.pop('type')

    try:
        session['email']
    except KeyError:
        session_exists = False

    try:
        session['username_user']
        session.pop('username_user')
        session.pop('name_employee')
    except KeyError:
        session_employee_exists = False

    if session_employee_exists:
        return redirect('company_member_logout')

    if not session_exists:
        return redirect('home')
    return render_template('logout.html')


@app.route('/company_member_logout')
def company_member_logout():
    session_exists = True
    try:
        session.pop('username_user')
        session.pop('name_employee')
        session.pop('role_employee')
        session.pop('department_employee')
        session['username_user']
    except KeyError:
        session_exists = False

    if not session_exists:
        return redirect('home')
    return render_template('logout.html')


@app.route('/feedback', methods=['POST', 'GET'])
def feedback():
    form_rating = RatingForm()
    if form_rating.is_submitted():
        new_review = Rating(id_reviewer=form_rating.id_reviewer.data.upper(), type=form_rating.type.data,
                            review=form_rating.review.data)
        db.session.add(new_review)
        db.session.commit()
        return redirect('home')
    return render_template('feedback.html', form_rating=form_rating)


@app.route('/order', methods=['POST', 'GET'])
def order():
    formNextStep = FormNextStep()
    if session['type'] == 'COMPANY':
        orders = Order.query.filter(or_(Order.user == session['id_user'],
                                        Order.user == session['username_user'],
                                        Order.order_company_customer == session['id_user'],
                                        Order.company == session['id_user'])).all()
        if formNextStep.is_submitted():
            return redirect('order')
    elif session['type'] == 'PRIVATE':
        orders = Order.query.filter_by(order_private_customer=session['username']).all()
    if session.get('name_employee') is not None:
        if not os.path.exists('static/' + str(session.get('name_employee'))):
            os.makedirs('static/' + str(session.get('name_employee')))
        file_url = os.listdir('static/' + str(session.get('name_employee')))
        file_url = [str(session.get('name_employee')) + "/" + file for file in file_url]
    else:
        if not os.path.exists('static/' + str(session.get('id_user'))):
            os.makedirs('static/' + str(session.get('id_user')))
        file_url = os.listdir('static/' + str(session.get('id_user')))
        file_url = [str(session.get('id_user')) + "/" + file for file in file_url]
    formUpload = UploadForm()
    if formUpload.validate_on_submit():
        if session.get('name_employee') is not None:
            filename = photos.save(formUpload.file.data, name=str(session.get('name_employee')) + '.jpg',
                                   folder=str(session.get('name_employee')))
        else:
            filename = photos.save(formUpload.file.data, name=str(session.get('id_user')) + '.jpg',
                                   folder=str(session.get('id_user')))
        file_url.append(filename)
    return render_template('order.html', orders=orders, formNextStep=formNextStep, formupload=formUpload, filelist=file_url)


@app.route('/order/<int:order_no>', methods=['POST', 'GET'])
def update_status(order_no):
    order = Order.query.filter_by(order_id=order_no).first()
    departments = Department.query.all()
    order_status = order.order_state
    if order.order_state == 'TO BE STARTED':
        order_status = departments[0].department_name
    else:
        i = 0
        for department in departments:
            if order.order_state == department.department_name:
                try:
                    if departments[i+1]:
                        order_status = departments[i+1].department_name
                        break
                except IndexError:
                    order_status = 'FINISHED'
                    break
            else:
                i = i+1
    order.order_state = order_status
    db.session.commit()

    #ToDo: come rimuovere codice duplicato? se scrivo return order() mi da errore
    formNextStep = FormNextStep()
    if session['type'] == 'COMPANY':
        orders = Order.query.filter(or_(Order.user == session['id_user'],
                                        Order.user == session['username_user'],
                                        Order.order_company_customer == session['id_user'],
                                        Order.company == session['id_user'])).all()
        if formNextStep.is_submitted():
            return redirect('order')
    elif session['type'] == 'PRIVATE':
        orders = Order.query.filter_by(order_private_customer=session['username']).all()
    try:
        if not os.path.exists('static/' + str(session.get('name_employee'))):
            os.makedirs('static/' + str(session.get('name_employee')))
        file_url = os.listdir('static/' + str(session.get('name_employee')))
        file_url = [str(session.get('name_employee')) + "/" + file for file in file_url]
    except KeyError:
        if not os.path.exists('static/' + str(session.get('id_user'))):
            os.makedirs('static/' + str(session.get('id_user')))
        file_url = os.listdir('static/' + str(session.get('id_user')))
        file_url = [str(session.get('id_user')) + "/" + file for file in file_url]
    formUpload = UploadForm()
    if formUpload.validate_on_submit():
        try:
            filename = photos.save(formUpload.file.data, name=str(session.get('name_employee')) + '.jpg',
                                   folder=str(session.get('name_employee')))
        except KeyError:
            filename = photos.save(formUpload.file.data, name=str(session.get('id_user')) + '.jpg',
                                   folder=str(session.get('id_user')))
        file_url.append(filename)
    return render_template('order.html', orders=orders, formNextStep=formNextStep, formupload=formUpload, filelist=file_url)


@app.route('/order_creation', methods=['POST', 'GET'])
def order_creation():
    form_order_creation = OrderCreation()
    CUSTOMERS = PrivateCustomer.query.all()
    if form_order_creation.is_submitted():
        customer_selected = request.form.get('customerId')
        if PrivateCustomer.query.filter_by(username=customer_selected).first() is not None:
            new_order = Order(order_description=form_order_creation.order_description.data, order_delivery_type=form_order_creation.order_delivery_type.data.upper(),
                          order_delivery_date=form_order_creation.date_delivery.data, order_delivery_time=form_order_creation.time_delivery.data,
                          order_delivery_company=form_order_creation.delivery_company.data.upper(), order_state='TO BE STARTED',
                          order_private_customer=customer_selected, company=session['id_user'],
                          user=session['username_user'], date_insert=form_order_creation.date_insert.data, date_request=form_order_creation.date_request.data)

        elif CompanyCustomer.query.filter_by(name_company=customer_selected).first() is not None:
            new_order = Order(order_description=form_order_creation.order_description.data, order_delivery_type=form_order_creation.order_delivery_type.data.upper(),
                          order_delivery_date=form_order_creation.date_delivery.data, order_delivery_time=form_order_creation.time_delivery.data,
                          order_delivery_company=form_order_creation.delivery_company.data.upper(), order_state='TO BE STARTED',
                          order_company_customer=customer_selected, company=session['id_user'],
                          user=session['username_user'], date_insert=form_order_creation.date_insert.data, date_request=form_order_creation.date_request.data)

        db.session.add(new_order)
        db.session.commit()
        return redirect('order')
    return render_template('order_creation.html', form_order_creation=form_order_creation, customers=CUSTOMERS)


@app.route('/order_management_menu/<int:order_no>')
def order_management_menu(order_no):
    session['order_no'] = order_no
    return render_template('order_management_menu.html', order_no=order_no)


@app.route('/talk_with_the_customer', methods=['POST', 'GET'])

def talk_with_the_customer():
    order = Order.query.filter_by(order_id=session['order_no']).first()
    steps = Department.query.all()
    messages = MessageWithCustomer.query.filter_by(order_product_id=session['order_no']).all()
    if order.order_private_customer:
        customer = order.order_private_customer
    elif order.order_company_customer:
        customer = order.order_company_customer
    formChat = FormChat()
    if formChat.is_submitted():
        if session['type'] == 'COMPANY':
            new_message = MessageWithCustomer(order_product_id=session['order_no'], company_user=session['username_user'],
                                              message=formChat.message.data, customer=customer, sender=session['name_employee']+' - '+session['id_user'],
                                              datetime=datetime.datetime.now())
        if session['type'] == 'PRIVATE':
            new_message = MessageWithCustomer(order_product_id=session['order_no'],
                                              message=formChat.message.data, customer=customer, sender=session['id_user'],
                                              datetime=datetime.datetime.now())
        db.session.add(new_message)
        db.session.commit()
        return redirect('talk_with_the_customer')
    return render_template('talk_with_the_customer.html', order=order, steps=steps, formChat=formChat, messages=messages)


@app.route('/upload_file_customer', methods=['POST', 'GET'])
def upload_file_customer():
    if request.method =='POST':
        file = request.files['file[]']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            flash("File Uploaded", "Success")
        return render_template('upload_file_customer.html')
    return render_template('upload_file_customer.html')


@app.route('/talk_with_departments', methods=['POST', 'GET'])
def talk_with_departments():
    order = Order.query.filter_by(order_id=session['order_no']).first()
    steps = Department.query.all()
    messages = MessageWithDepartment.query.filter_by(order_product_id=session['order_no']).all()
    formChat = FormChat()
    employee_department = CompanyUser.query.filter_by(username=session['username_user']).first().department
    if formChat.is_submitted():
        if session['type'] == 'COMPANY':
            new_message = MessageWithDepartment(order_product_id=session['order_no'], company_user=session['username_user']+' - '+employee_department,
                                              department=employee_department, message=formChat.message.data,
                                              datetime=datetime.datetime.now())
        db.session.add(new_message)
        db.session.commit()
        return redirect('talk_with_departments')
    return render_template('talk_with_departments.html', order=order, steps=steps, formChat=formChat, messages=messages)

#todo: non funziona perche bisogna passare alla pagina talk_with department l'order_no
@app.route('/upload_file_departments/<int:order_no>', methods=['POST', 'GET'])
def upload_file_departments(order_no):
    if request.method =='POST':
        file = request.files['file[]']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash("File Uploaded", "Success")
        return render_template('talk_with_departments.html', order_no=order_no, file=file)
    return render_template('upload_file_departments.html')


@app.route('/register_product', methods=['POST', 'GET'])
def register_product():
    form_product = RegistrationProduct()
    if form_product.validate_on_submit():
        new_product = Product(name=form_product.name.data.upper(), quantity=form_product.quantity.data,
                              price=form_product.price.data,
                              availability=form_product.availability.data,
                              type=form_product.type.data.upper())
        db.session.add(new_product)
        db.session.commit()
        return redirect('order.html')
    return render_template('reg_product.html', formReg=form_product)


@app.route("/upload", methods=["POST", "GET"])
def upload():
    if session.get('name_employee') is not None:
        if not os.path.exists('static/' + str(session.get('name_employee'))):
            os.makedirs('static/' + str(session.get('name_employee')))
        file_url = os.listdir('static/' + str(session.get('name_employee')))
        file_url = [str(session.get('name_employee')) + "/" + file for file in file_url]
    else:
        if not os.path.exists('static/' + str(session.get('id_user'))):
            os.makedirs('static/' + str(session.get('id_user')))
        file_url = os.listdir('static/' + str(session.get('id_user')))
        file_url = [str(session.get('id_user')) + "/" + file for file in file_url]
    formUpload = UploadForm()
    filename=''
    if formUpload.validate_on_submit():
        if session.get('name_employee') is not None:
            filename = photos.save(formUpload.file.data, name=str(session.get('name_employee')) + '.jpg', folder=str(session.get('name_employee')))
        else:
            filename = photos.save(formUpload.file.data, name=str(session.get('id_user')) + '.jpg', folder=str(session.get('id_user')))
        file_url.append(filename)
    flash('warning', filename)
    return render_template("upload_image.html", formupload=formUpload, filelist=file_url)


@app.route('/company_communications')
def communications():
    return render_template("company_communications.html")


@app.route('/upload_report/<string:type>')
def upload_report(type):
    return render_template("upload_report.html")


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run()
