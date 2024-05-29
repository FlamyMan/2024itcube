from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class ExampleForm(FlaskForm):
    draft = TextAreaField("Черновик")
    answer = StringField("Ответ",   validators=[DataRequired()])
    submit = SubmitField('Готово')