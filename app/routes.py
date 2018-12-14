from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, SendResult, AddTask, VerifyTask
from app.models import User, Task


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    stat = current_user.tasks_quantity()
    return render_template('index.html', title='Главная', stat=stat)


@app.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    tasks_list = current_user.tasks.all()
    form = SendResult()
    if form.validate_on_submit():
        task = Task.query.filter_by(id=int(form.number.data)).first()
        task.status = 1
        task.result = form.task_result.data
        db.session.commit()
        return redirect(url_for('tasks'))
    return render_template('tasks_for_user.html', title='Задачи', tasks=tasks_list, form=form)


@app.route('/users_tasks', methods=['GET', 'POST'])
@login_required
def users_tasks():
    tasks_list = current_user.author_tasks.all()
    form = VerifyTask()
    if form.validate_on_submit():
        task = Task.query.filter_by(id=int(form.number.data)).first()
        task.status = 2
        db.session.commit()
        return redirect(url_for('users_tasks'))
    return render_template('tasks_for_admins.html', title='Задачи', tasks=tasks_list, form=form,
                           current_user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неверные учетные данные', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Вход', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if current_user.type == 0:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, type=form.user_type.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Новый пользователь добавлен', 'primary')
        return redirect(url_for('login'))
    return render_template('register.html', title='Новый пользователь', form=form)


@app.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    if current_user.type == 0:
        return redirect(url_for('index'))
    form = AddTask()
    form.user_id.choices = [(user.id, user.username) for user in User.query.all()]
    if form.validate_on_submit():
        task = Task(task=form.task.data, author_id=current_user.id, user_id=form.user_id.data,
                    timestamp=datetime.utcnow())
        db.session.add(task)
        db.session.commit()
        flash('Задача назначенна', 'primary')
        return redirect(url_for('add_task'))
    return render_template('add_task.html', title='Назначить задачу', form=form)
