from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class GetTownForm(FlaskForm):
    town = StringField('Напишите город', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')