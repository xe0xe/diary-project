from flask import Flask, render_template, redirect, request
from data import db_session
from flask_login import LoginManager, login_user, login_required, logout_user, user_logged_out, current_user
from data.users import User
from data.charges import Charge
from login_form import LoginForm
from register_form import RegisterForm
from panel_form import PanelForm
from charge_form import ChargeForm
from flask_restful import reqparse, abort, Api, Resource
import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/blogs.db")
login_manager = LoginManager()
login_manager.init_app(app)

month = int(str(datetime.date.today()).split('-')[1])

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/')
def index():
    return render_template('index.html', title='Главная')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/success")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/success', methods=['GET', 'POST'])
def success():
    form = PanelForm()
    db_sess = db_session.create_session()
    charges = db_sess.query(Charge).filter((Charge.user == current_user), (Charge.created_date == month))
    return render_template('diary.html', title='Главная', form=form, charges=charges)

@app.route('/next')
def next():
    global month
    month += 1
    form = PanelForm()
    db_sess = db_session.create_session()
    charges = db_sess.query(Charge).filter((Charge.user == current_user), (Charge.created_date == month))
    return render_template('diary.html', form=form, charge=charges)

@app.route('/back')
def back():
    global month
    month -= 1
    form = PanelForm()
    db_sess = db_session.create_session()
    charges = db_sess.query(Charge).filter((Charge.user == current_user), (Charge.created_date == month))
    return render_template('diary.html', form=form, charge=charges)

@app.route('/charges',  methods=['GET', 'POST'])
@login_required
def add_charge():
    form = ChargeForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if charge := db_sess.query(Charge).filter((Charge.user == current_user), (Charge.created_date == month)).first():
            charge.content = float(charge.content) + float(form.content.data)
            db_sess.merge(current_user)
            db_sess.commit()
        else:
            charge = Charge()
            charge.content = form.content.data
            charge.created_date = month
            current_user.charges.append(charge)
            db_sess.merge(current_user)
            db_sess.commit()
        return redirect('/success')
    return render_template('charge.html', title='Добавление расхода',
                           form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


app.run(port=8080, host='127.0.0.1')

