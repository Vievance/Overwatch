from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField, DateField
from wtforms.validators import DataRequired, Length
from datetime import date

class HeroForm(FlaskForm):
    roles = [('Tank', 'Tank'), ('DPS', 'DPS'), ('Support', 'Support')]

    name = StringField('Name', validators=[DataRequired(),Length(min=2, max=30)])
    role = RadioField('Role', choices=roles, validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired(),Length(min=2, max=30)])
    release_date = DateField('Relase Date', default=date(2016, 5, 4))
    submit = SubmitField('Submit')