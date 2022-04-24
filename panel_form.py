from flask_wtf import FlaskForm
from wtforms import SubmitField


class PanelForm(FlaskForm):
    back = SubmitField('Назад')
    forward = SubmitField('Вперед')
    add = SubmitField('Добавить')
