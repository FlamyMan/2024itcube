from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, BooleanField
from wtforms.fields import EmailField
from wtforms import validators
import string

class RegisterForm(FlaskForm):
    name = StringField('Имя пользователя', 
                       validators=[
                           validators.DataRequired(),
                           validators.Length(min=6, message="Минимальная длинна имени 6 символов"),])
    email = EmailField('Электронная почта', validators=[validators.DataRequired()])
    password = PasswordField('Пароль', validators=[validators.DataRequired(), validators.EqualTo('password_again', message='Пароли не совпадают')])
    password_again = PasswordField('Повторите пароль')
    submit = SubmitField('Зарегестрироваться')


class LoginForm(FlaskForm):
    enter = StringField('Электронная почта или имя пользователя', validators=[validators.DataRequired()])
    password = PasswordField('Пароль', validators=[validators.DataRequired()])
    remember_me = BooleanField('Запомнить меня?')
    submit = SubmitField('Войти')