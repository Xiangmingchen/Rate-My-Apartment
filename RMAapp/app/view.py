from flask import Flask, render_template, flash, redirect
from app import app, db, data
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

@app.route('/database/update')
def update_database():
    # zpid = 3197980
    # data.centerRequest(zpid)
    data.update_database()
    return 'Database updated'

# 89045947
@app.route('/center_request/<zpid>')
def center_request(zpid):
    request_success = data.center_request(zpid)
    if not request_success:
        return 'Request failed'
    return 'Request succeeded'

@app.route('/database/<int:zpid>')
def database(zpid):

    # Dispay the apartments with pictures first
    apartment = db.session.query(Apartment) \
                        .filter(Apartment.zpid == zpid).one_or_none()
    if apartment:
        return 'Apartment address: %s' % (apartment.address[0].street + ' ' + apartment.address[0].city)
    else:
        return 'No apartment <%i> in database' % zpid

@app.route('/database/expand')
def expand_database():
    new_apart_count = data.expand_database()
    return 'Added %i apartments' % new_apart_count

@app.route('/database/count/<table_name>')
def count_database_rows(table_name):
    count = data.count_rows(table_name)
    if count >= 0:
        return 'There are %i in %s database' % (count, table_name)
    else:
        return 'Invalid table name'

@app.route('/database/show_data/<table_name>')
def show_data(table_name):
    return data.display_data(table_name)

@app.route('/get_address/<int:zpid>')
def getaddress(zpid):
    return data.get_address(zpid)

@app.route('/database/add_new_apartment/<address>/<int:zipcode>')
def add_new_apartment(address, zipcode):
    success = data.add_new_apartment(address, zipcode)
    if success:
        return 'Apartment added'
    else:
        return 'Apartment adding failed'
