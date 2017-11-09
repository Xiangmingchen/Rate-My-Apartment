from flask import Flask, render_template, flash, redirect
from app import app
from app import requestZillowAPI
import math


@app.route('/')
@app.route('/filter')
def filter():

    requestZillowAPI.request()

    from app.models import Apartment, Address
    from app.query import session
    apartments = session.query(Apartment).all()

    localAp = []
    centerZipcode = 61801

    for apartment in apartments:
        if apartment.address[0].zipcode == centerZipcode:
            localAp.append(apartment)
    apartments = localAp

    return render_template('index.html', title='Home', \
                            apartments=apartments, \
                            rows=math.ceil(len(apartments) / 3),\
                            length=len(apartments))
