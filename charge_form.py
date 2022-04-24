from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, SubmitField


class ChargeForm(FlaskForm):
    content = FloatField("Содержание")
    created_date = IntegerField('Номер месяца')
    submit = SubmitField('Применить')
