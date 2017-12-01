# from flask_wtf.csrf import CSRFProtect

# Flask-WTF provides your Flask application integration with WTForms. For example:
from flask import render_template, redirect, app
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class ContactForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired()])
    subject = TextAreaField("Subject", validators=[DataRequired()])
    review = TextAreaField('Review', validators=[DataRequired()])
    submit = SubmitField("Send!", validators=[DataRequired()])

# Validating the request in your view handlers:


@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = ContactForm()
    if form.validate_on_submit(): # meaning if form is submitted successfully.
        return redirect('/success')
    return render_template('submit.html', form=form)


# In addition, a CSRF token hidden field is created automatically. You can render this in your template:

# <form method = "POST" action = "/">
#    {{form.csrf_token}}
#    {{form.name.label}} {{form.name(size=20)}}
#    <input type = "submit" value = "Go">
# </form>

# csrf = CSRFProtect(app)
