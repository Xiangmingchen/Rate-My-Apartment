from flask import Flask, render_template, flash, redirect
from app import app, db, requestZillowAPI
from app.models import Apartment, Address
import math


@app.route('/')
@app.route('/filter')
def filter():

    # Dispay the apartments with pictures first
    apartments = db.session.query(Apartment) \
                        .order_by(Apartment.image_count.desc()) \
                        .all()

    ## if you want to only display the apartments in a certain city, put the city
    ## zipcode at centerZipcode, and enable the following lines
    # localAp = []
    # centerZipcode = 61801
    #
    # for apartment in apartments:
    #     if apartment.address[0].zipcode == centerZipcode:
    #         localAp.append(apartment)
    # apartments = localAp

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

# 89045947
@app.route('/center_request/<zpid>')
def center_request(zpid):
    requestZillowAPI.centerRequest(zpid)
    return 'Request made'

@app.route('/debug/<int:zpid>')
def debug(zpid):

    # Dispay the apartments with pictures first
    apartment = db.session.query(Apartment) \
                        .filter(Apartment.zpid == zpid).one_or_none()
    if apartment:
        return 'Apartment address: %s' % (apartment.address[0].street + ' ' + apartment.address[0].city)
    else:
        return 'No apartment: %i' % zpid
