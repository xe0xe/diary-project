from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, SubmitField


class ChargeForm(FlaskForm):
    content = FloatField("Содержание")
    submit = SubmitField('Применить')
