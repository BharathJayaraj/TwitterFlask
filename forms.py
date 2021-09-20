from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms import (
    validators,
    SubmitField,
    StringField,
    BooleanField
)


class FilterForm(FlaskForm):
    try:
        startdate = DateField('Start Date', format='%Y-%m-%d', validators=(validators.DataRequired(),))
        enddate = DateField('End Date', format='%Y-%m-%d', validators=(validators.DataRequired(),))
        chronological = BooleanField('Chronological')
        submit = SubmitField('Submit')
    except Exception as err:
        print("Exception occurred in filter form function.", err)


class SearchForm(FlaskForm):
    try:
        search = StringField('Search')
        submit = SubmitField('Search')
    except Exception as err:
        print("Exception occurred in search form function.", err)
