from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, Field
from wtforms.validators import DataRequired


class ProblemForm(FlaskForm):
    draft = TextAreaField("Черновик")
    answer = StringField("Ответ",   validators=[DataRequired()])