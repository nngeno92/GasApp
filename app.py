from flask import Flask, render_template, request, redirect, url_for
import os
from flask_sqlalchemy import SQLAlchemy
from bson.objectid import ObjectId
from datetime import datetime, date, time
from sqlalchemy import *
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:512104013N@localhost/jujaappdb'
app.config['SECRET_KEY'] = '512104013N'
CORS(app)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Define models


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    phone_no = db.Column(db.String(11))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(80))


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    phone_no = db.Column(db.String(11))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(80))


class Orderdetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    phone_no = db.Column(db.String(11))
    order_type = db.Column(db.String(10))
    brand = db.Column(db.String(10))
    size = db.Column(db.String(10))
    gate_region = db.Column(db.String(20))
    apartment = db.Column(db.String(20))
    time_placed = db.Column(db.Time())
    date_placed = db.Column(db.Date())
    complete = db.Column(db.String(10))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/faq')
def faq():
    return render_template('faq.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':

        user = User.query.filter_by(phone_no=request.form['phone_no']).first()

        if user:
            if request.form['password'] == user.password:
                login_user(user)

                return redirect(url_for('orders'))  # orders()
        return 'Invalid username/password combination'

    return render_template('login.html')


@app.route('/admin_login', methods=['POST', 'GET'])
def login_admin():
    if request.method == 'POST':

        admin = Admin.query.filter_by(
            phone_no=request.form['phone_no']).first()

        if admin:
            if request.form['password'] == admin.password:

                return redirect(url_for('admin'))
        return 'Invalid username/password combination'
    return render_template('admin_login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':

        name = request.form.get('name')
        email = request.form.get('email')
        phone_no = request.form.get('phone_no')
        password = request.form.get('password')

        new_user = User(name=name, phone_no=phone_no,
                        email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    else:

        return render_template('signup.html')


@app.route('/orders', methods=['POST', 'GET'])
@login_required
def orders():
    if request.method == 'POST':

        name = current_user.name  # login_user['name']
        phone_no = current_user.phone_no  # login_user['phone_no']
        order_type = request.form['order_type']
        brand = request.form['brand']
        size = request.form['size']
        gate_region = request.form['gate_region']
        apartment = request.form['apartment']
        date_placed = date.today()
        time_placed = func.current_timestamp()
        complete = "Pending"

        new_order = Orderdetails(name=name, phone_no=phone_no, order_type=order_type, brand=brand, size=size,
                                 gate_region=gate_region, apartment=apartment, date_placed=date_placed, time_placed=time_placed, complete=complete)

        db.session.add(new_order)
        db.session.commit()
        return render_template('order_confirmation.html')

    return render_template('orders.html', name=current_user.name)


@app.route('/complete_order_in_admin/<theid>', methods=['PUT', 'GET', 'POST'])
def complete_order_in_admin(theid):
    idd = theid

    Orderdetails.query.filter_by(id=idd).update(
        {Orderdetails.complete: "Completed"})
    db.session.commit()

    return redirect(url_for('admin'))


@app.route('/complete_order_in_latest/<theid>', methods=['PUT', 'GET', 'POST'])
def complete_order_in_latest(theid):
    idd = theid
    Orderdetails.query.filter_by(id=idd).update(
        {Orderdetails.complete: "Completed"})
    db.session.commit()

    return redirect(url_for('latest_orders'))


@app.route('/complete_order_in_pending/<theid>', methods=['PUT', 'GET', 'POST'])
def complete_order_in_pending(theid):
    idd = theid

    Orderdetails.query.filter_by(id=idd).update(
        {Orderdetails.complete: "Completed"})
    db.session.commit()
    return redirect(url_for('pending_orders'))


@app.route('/confirm_order')
@login_required
def confirm():
    return render_template('order_confirmation.html', name=current_user.name)


@app.route('/about')
def about_us():
    return render_template('about.html')


@app.route('/admin,,,')
def admin():

    all_orders = Orderdetails.query.order_by(desc(Orderdetails.id))

    return render_template('admin.html', orders=all_orders)


@app.route('/latest_orders')
def latest_orders():
    latest_orders = Orderdetails.query.order_by(desc(Orderdetails.id)).limit(5)
    return render_template('latest_orders.html', orders=latest_orders)


@app.route('/pending_orders')
def pending_orders():

    pending_orders = Orderdetails.query.filter_by(
        complete='Pending').order_by(desc(Orderdetails.id))
    return render_template('pending_orders.html', orders=pending_orders)


@app.route('/filter')
def filter():

    return render_template('filter.html')


@app.route('/filterby/<something>', methods=['POST'])
def filter_by(something):
    criteria = something

    if criteria == "order_type":
        value = request.form['order_type']
        by_order_type = Orderdetails.query.filter_by(
            order_type=value).order_by(desc(Orderdetails.id))
        return render_template('filter.html', orders=by_order_type)
    elif criteria == "gate":
        value = request.form['gate']
        by_gate = Orderdetails.query.filter_by(
            gate_region=value).order_by(desc(Orderdetails.id))
        return render_template('filter.html', orders=by_gate)
    elif criteria == "phone_no":
        value = request.form['phone_no']
        by_phone_no = Orderdetails.query.filter_by(
            phone_no=value).order_by(desc(Orderdetails.id))

        return render_template('filter.html', orders=by_phone_no)

    elif criteria == "date":
        value = request.form['date']
        by_date = Orderdetails.query.filter_by(
            date_placed=value).order_by(desc(Orderdetails.id))
        return render_template('filter.html', orders=by_date)
    else:
        pass


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(port=5001, debug=True)
