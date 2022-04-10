from flask_wtf import FlaskForm
from wtforms import SubmitField


class PanelForm(FlaskForm):
    back = SubmitField('Назад')
    forward = SubmitField('Вперед')
    month = SubmitField('За месяц')
    year = SubmitField('За год')
