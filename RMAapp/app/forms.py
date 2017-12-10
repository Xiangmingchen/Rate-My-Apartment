from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, validators, RadioField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    search = StringField('search', validators=[DataRequired()])

class ReviewForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    rating = RadioField('Rating', [validators.InputRequired()], choices=[("1", 'one'), ("2", 'two'), ("3", 'three'),("4",'four'),("5", 'five')])
    content = TextAreaField('Content', [validators.Length(min=10, max=100000)])


class TestForm(FlaskForm):
    choice_switcher = RadioField(
        'Choice?',
        [validators.Required()],
        choices=[('choice1', 'Choice One'), ('choice2', 'Choice Two')], default='choice1'
    )
