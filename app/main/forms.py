from flask_wtf import FlaskForm
from wtforms import validators, StringField, SubmitField


class TermForm(FlaskForm):
    term = StringField('Term: ', validators=[validators.DataRequired()])
    submit = SubmitField('Predict...')
