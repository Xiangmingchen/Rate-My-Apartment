from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, validators
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    search = StringField('search', validators=[DataRequired()])

class ReviewForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    rating = IntegerField('Rating', [validators.InputRequired()])
    comment = TextAreaField('Comment', [validators.Length(min=10, max=100000)])
