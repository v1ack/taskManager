from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    user_type = SelectField('Права доступа', choices=[(0, 'Рабочий'), (1, 'Администратор')])
    submit = SubmitField('Зарегистрировать')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Введите другое имя')


class SendResult(FlaskForm):
    task_result = StringField('Введите результат', validators=[DataRequired()])
    number = StringField(default=0)
    submit = SubmitField('Отправить')


class VerifyTask(FlaskForm):
    number = StringField(default=0)
    submit = SubmitField('Подтвердить')


class AddTask(FlaskForm):
    task = StringField('Задача', validators=[DataRequired()])
    user_id = SelectField('Пользователь', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Назначить')
