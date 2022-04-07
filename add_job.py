from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, \
    SubmitField, EmailField, IntegerField, DateField
from wtforms.validators import DataRequired


class AddJob(FlaskForm):
    collaborators = StringField('Сотрудники', validators=[DataRequired()])
    job = StringField('Название работы', validators=[DataRequired()])
    work_size = IntegerField('Объем работы', validators=[DataRequired()])
    start_date = DateField('Начало работ', validators=[DataRequired()])
    end_date = DateField("Окончание работ", validators=[DataRequired()])
    team_leader = StringField('Бригадир', validators=[DataRequired()])
    submit = SubmitField('Добавить')