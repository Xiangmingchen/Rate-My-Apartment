from flask import Flask, render_template
from forms import ContactForm

# In order to generate the csrf token, you must have a secret key, this is usually the same as your Flask app secret
#  key. If you want to use another secret key, config it:

app = Flask(__name__)
app.secret_key = 'CS196'


@app.route('/reviewpage', methods=['GET', 'POST'])
def review():
    form = ContactForm()

    if request.method == 'POST':
        return "Review Posted."
    elif request.method == 'GET':
        return render_template('reviewpage.html', form=form )

if __name__ == '__main__':
    app.run(debug=True)