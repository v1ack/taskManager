from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    type = db.Column(db.Integer, default=0)
    password_hash = db.Column(db.String(128))
    tasks = db.relationship('Task', backref='user_task', lazy='dynamic', foreign_keys='Task.user_id')
    author_tasks = db.relationship('Task', backref='author', lazy='dynamic', foreign_keys='Task.author_id')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def tasks_list(self):
        return self.tasks.all()

    def given_tasks_list(self):
        return self.author_tasks.all()

    def tasks_quantity(self):
        to = self.tasks_list()
        by = self.given_tasks_list()
        return {'to': {'all': len(to),
                       'not_done': len([i for i in to if i.status == 0]),
                       'done': len([i for i in to if i.status == 1]),
                       'verified': len([i for i in to if i.status == 2])},
                'by': {'all': len(by),
                       'not_done': len([i for i in by if i.status == 0]),
                       'done': len([i for i in by if i.status == 1]),
                       'verified': len([i for i in by if i.status == 2])}}


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    result = db.Column(db.String(300), default='')
    status = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Task {self.task}>'

    def get_author_name(self):
        return User.query.get(self.author_id).username

    def get_user_name(self):
        return User.query.get(self.user_id).username
