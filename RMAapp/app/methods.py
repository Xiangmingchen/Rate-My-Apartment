# These are routes used to manipulate database
# I know there are better ways but I went along with urls

@app.route('/database/update')
def update_database():
    # zpid = 3197980
    # data.centerRequest(zpid)
    data.update_database()
    return 'Database updated'

# 89045947
@app.route('/center_request/<int:zpid>')
def center_request(zpid):
    new_apart_count = data.center_request(zpid)
    return 'Request created %i new apartments' % new_apart_count

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

@app.route('/database/store_comps/<int:zpid>')
def store_comps(zpid):
    return data.store_comps_file(zpid)
