from flask_wtf import FlaskForm
from wtforms import SubmitField


class PanelForm(FlaskForm):
    back = SubmitField('Назад')
    now = SubmitField('Текущий')
    forward = SubmitField('Вперед')
    add = SubmitField('Добавить')
