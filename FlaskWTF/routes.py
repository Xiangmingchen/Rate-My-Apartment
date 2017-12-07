from flask import Flask, render_template, request, redirect
from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
app = Flask(__name__)
app.secret_key = 'CS196'  # do we need this?


class ContactForm(Form):
    name = StringField('username', validators=[DataRequired()])
    subject = TextAreaField("subject", validators=[DataRequired()])
    reviews = TextAreaField('reviews', validators=[DataRequired()])
    submit = SubmitField("submit", validators=[DataRequired()])


@app.route('/', methods=('GET', 'POST'))
def submit():
    form = ContactForm()
    if form.validate_on_submit():  # meaning if form is submitted successfully.
        return "Thank you for posting the review!"  # or redirect('/success')
    return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)


# @app.route('/send', methods=['GET', 'POST'])
# def send():
#
#     if request.method == 'POST':
#         name = request.form['name']
#         subject = request.form['subject']
#         reviews = request.form['reviews']
#
#         return "Review Posted." and render_template('form.html', name=name, subject=subject, reviews=reviews)
#
#     elif request.method == 'GET':
#         form = ContactForm()
#         return render_template('form.html', form=form)
#
#
# @app.route('/success')
# def thanks():
#     return "Your Review is Submitted!"
