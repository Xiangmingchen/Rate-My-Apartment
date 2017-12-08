from flask import Flask
app = Flask(__name__)

@app.route('/user/<userid>')
def show_user_profile(userid):
    return 'User %s' % userid
