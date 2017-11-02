from flask import Flask, render_template, flash, redirect
from app import app
import math

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():

    from app.models import Apartment, Address
    from app.query import session
    apartments = session.query(Apartment).all()
    UrbanaAp = []
    for apartment in apartments:
        if apartment.address[0].zipcode == 61801:
            UrbanaAp.append(apartment)

    return render_template('index.html', title='Home', apartments=UrbanaAp, \
                            rows=math.ceil(len(UrbanaAp) / 3),\
                            length=len(UrbanaAp))
