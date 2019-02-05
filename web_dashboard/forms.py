from flask_wtf import FlaskForm
from wtforms.fields import *
from wtforms.validators import DataRequired


class AnalyzeForm(FlaskForm):
    zipcode = StringField(u'Zipcode', validators=[DataRequired()])
    submit = SubmitField(u'Analyze')
