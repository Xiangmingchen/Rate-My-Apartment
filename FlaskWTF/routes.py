from flask import Flask, render_template
from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = 'CS196'


class ContactForm(Form):
    name = StringField('Username', validators=[InputRequired()])
    subject = TextAreaField("Subject", validators=[InputRequired()])
    reviews = TextAreaField('Review', validators=[InputRequired()])


@app.route('/', methods=['GET', 'POST'])
def submit():
    form = ContactForm()
    if form.validate_on_submit():
        return 'Thank you for posting the review!'
    return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)


# unused codes below:
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
