from flask import Flask, render_template, redirect
from data import db_session, jobs_api
from flask_login import LoginManager, login_user, login_required, logout_user, user_logged_out
from data.users import User
from data.jobs import Jobs
from data.news import News
from login_form import LoginForm
from register_form import RegisterForm
from add_job import AddJob
from flask_restful import reqparse, abort, Api, Resource
import news_resources, users_resource


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/blogs.db")
login_manager = LoginManager()
login_manager.init_app(app)

# user = User()
# user.name = "Пользователь 1"
# user.about = "биография пользователя 1"
# user.email = "email@email.ru"
# db_sess = db_session.create_session()
# db_sess.add(user)
# db_sess.commit()
#
# user = db_sess.query(User).filter(User.id == 2).first()
# news = News(title="Личная запись", content="Эта запись личная",
#             is_private=False)
# user.news.append(news)
# db_sess.commit()

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/')
def index():
    return render_template('index.html', title='Главная')


# @app.route("/")
# def index():
#     db_sess = db_session.create_session()
#     news = db_sess.query(News).filter(News.is_private != True)
#     return render_template("blog.html", news=news)


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

@app.route('/success')
def success():
    return render_template('blog.html', title='Главная')

@app.route('/atblog')
def atblog():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private != True)
    return render_template('blog.html', news=news)

@app.route('/addcost', methods=['GET', 'POST'])
def addcost():
    form = AddJob()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs(
            collaborators=form.collaborators.data,
            job=form.job.data,
            work_size=form.work_size.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            team_leader=form.team_leader.data
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect("/")
    return render_template('adding_job.html', title='Добавление работы', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


app.register_blueprint(jobs_api.blueprint)
api = Api(app)
api.add_resource(news_resources.NewsListResource, '/api/v2/news')
api.add_resource(news_resources.NewsResource, '/api/v2/news/<int:news_id>')
api.add_resource(users_resource.UsersListResource, '/api/v2/users')
api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:user_id>')
app.run(port=8080, host='127.0.0.1')
