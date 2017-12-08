from flask import Flask, render_template, flash, redirect, request, url_for
from app import app, db, data
from app.models import Apartment, Address
from app.forms import SearchForm
import math


@app.route('/', methods=['GET', 'POST'])
def homepage():
    form = SearchForm()
    if form.validate_on_submit():
        search = form.search.data
        return redirect(url_for('filter', search=search))
    return render_template('home.html', form=form)


@app.route('/filter/<search>')
def filter(search=None):

    # Dispay the apartments with pictures first
    apartments = db.session.query(Apartment) \
                        .order_by(Apartment.image_count.desc()) \
                        .all()

    # if you want to only display the apartments in a certain city, put the city
    # zipcode at centerZipcode, and enable the following lines
    search = search.capitalize()
    local_apart = []
    if search is not None:
        for apartment in apartments:
            if apartment.address[0].city == search:
                local_apart.append(apartment)
        apartments = local_apart

    def length(a):
        return len(a)

    return render_template('index.html', title='Home', \
                            apartments=apartments, \
                            rows=math.ceil(len(apartments) / 3),\
                            length=len(apartments), \
                            len=length)

@app.route('/reviewpage/<int:zpid>')
def reviewpage(zpid):
    this_apart = db.session.query(Apartment).filter(Apartment.zpid == zpid).one_or_none()
    def length(a):
        return len(a)
    return render_template('reviewpage.html', apartment=this_apart, \
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

@app.route('/database/query_address/<int:zpid>')
def database(zpid):
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

@app.route('/database/delete_extra_address')
def delete_extra_address():
    count = data.delete_extra_address()
    return 'Deleted %i address' % count

@app.route('/database/delete_address/<int:id>')
def delete_address(id):
    success = data.delete_address_by_id(id)
    return 'Address <id = %i> deletion %s' % (id, 'succeeded' if success else 'failed')

@app.route('/database/store_response/<int:zpid>')
def store_response(zpid):
    return data.store_response_file(zpid)

app.secret_key = 'CS196'
