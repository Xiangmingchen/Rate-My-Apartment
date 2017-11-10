from flask import Flask, render_template, flash, redirect
from app import app
from app import requestZillowAPI
import math


@app.route('/')
@app.route('/filter')
def filter():

    from app.models import Apartment, Address
    from app.query import session
    apartments = session.query(Apartment).all()

    ## if you want to only display the apartments in a certain city, put the city
    ## zipcode at centerZipcode, and enable the following lines
    localAp = []
    centerZipcode = 61801

    for apartment in apartments:
        if apartment.address[0].zipcode == centerZipcode:
            localAp.append(apartment)
    apartments = localAp

    def length(a):
        return len(a)

    return render_template('index.html', title='Home', \
                            apartments=apartments, \
                            rows=math.ceil(len(apartments) / 3),\
                            length=len(apartments), \
                            len=length)

@app.route('/update_database')
def update_database():
    # zpid = 3197980
    # requestZillowAPI.centerRequest(zpid)
    requestZillowAPI.update_database()
    return 'Database updated'
