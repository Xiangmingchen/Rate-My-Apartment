# from flask_wtf.csrf import CSRFProtect

# Flask-WTF provides your Flask application integration with WTForms. For example:
from flask import render_template
from wtforms import StringField, TextAreaField, SubmitField
from flask_wtf import FlaskForm


class ContactForm(FlaskForm):
    name = StringField('Username')
    subject = TextAreaField("Subject")
    review = TextAreaField('Review')
    submit = SubmitField("Send!")

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