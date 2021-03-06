import requests
from xml.etree.ElementTree import fromstring, ElementTree
import xml.dom.minidom
from lxml import html, etree
from RMAapp.app import db, ZillowAPI
from sqlalchemy import create_engine, func
from RMAapp.app.models import Apartment, Address, Image, Review, Details, Rooms, Amentities, City

## --------------- Interface functions --------------------
# Update the entire database
# return: nothing
# used helper functions: update_apartment_info()
# possible erros: none
def update_database():
    current_list = db.session.query(Apartment).all()
    for apartment in current_list:
        new_rent = get_rent(apartment.zpid)
        update_apartment_info(apartment, new_rent)

# Request GetComps from Zillow based on zpid, add new apartments to the database
# This fuction will not request if the zpid has been center_requested before
# input: zpid: the center zpid of the request
# return: on success: number of new apartments added
#         on failure: False
# used helper functions:
#       create_new_apartment()
#       rent_handler()
# possible errors:
#   1. Comp error: when GetComps returns error
#       handling: print error message to console, return False
def center_request(zpid):
    if isinstance(zpid, tuple):
        zpid = zpid[0]
    # check whether this apartment has been a center of request
    thisApart = db.session.query(Apartment).filter(Apartment.zpid == zpid).one_or_none()
    if thisApart is not None and not thisApart.comps:
        return 0
    # The following lines request 25 more property info with one known zpid
    parameters = {'zws-id': ZillowAPI.zwsid, 'zpid': zpid, 'count': 25, 'rentzestimate': True}
    response = requests.get("http://www.zillow.com/webservice/GetComps.htm", params=parameters)
    root = fromstring(response.content)
    # if there is an error, print an error message and return false
    error_code = int(root.find('.//code').text)
    if error_code != 0:
        print('Comp error: %i, %s' % (error_code, root.find('./message/text').text))
        thisApart.comps = False
        db.session.commit()
        return False
    # create a list of comparable apartments
    compList = root.findall('.//properties/comparables/comp')
    new_apart_count = 0
    # Store the apartments info into database
    for apart in compList:
        zp_id = int(apart.find('.//zpid').text)
        this_Apart = db.session.query(Apartment).filter(Apartment.zpid == zp_id).one_or_none()
        if this_Apart is None:  # if this apartment is not in our database, add it to database
            if create_new_apartment(zp_id, rent_handler(apart)):
                new_apart_count += 1
        # else: # otherwise update the info for this apartment
        #     update_apartment_info(thisApart, float(apart.find('./rentzestimate/amount').text))
        # compzpidlist.append(zpid)
    if thisApart == None:
        if create_new_apartment(zpid, rent_handler(root.find('.//principal'))):
            new_apart_count += 1
    thisApart = db.session.query(Apartment).filter(Apartment.zpid == zpid).one_or_none()
    thisApart.comps = False
    db.session.commit()
    return new_apart_count

# Expand database by center requesting every zpid in database
# return: total number of new added apartments
# used helper functions: center_request()
def expand_database():
    zpid_list = db.session.query(Apartment.zpid).all()
    new_apart_count = 0
    for zpid in zpid_list:
        new_apart_count += center_request(zpid)
    return new_apart_count

# Count how many rows are in the target table, same as number of entries in the database
# input: table_name: lowercased table name
# return: on success: number of rows in the table
#         on failure: -1
def count_rows(table_name):
    count = 0
    if table_name == 'apartment':
        count = db.session.query(func.count(Apartment.id)).scalar()
    elif table_name == 'address':
        count = db.session.query(func.count(Address.id)).scalar()
    elif table_name == 'image':
        count = db.session.query(func.count(Image.id)).scalar()
    elif table_name == 'review':
        count = db.session.query(func.count(Review.id)).scalar()
    elif table_name == 'details':
        count = db.session.query(func.count(Details.id)).scalar()
    elif table_name == 'rooms':
        count = db.session.query(func.count(Rooms.id)).scalar()
    elif table_name == 'amentities':
        count = db.session.query(func.count(Amentities.id)).scalar()
    elif table_name == 'city':
        count = db.session.query(func.count(City.id)).scalar()
    else:
        count = -1
    return count

# Display all the rows of a table, both printed to console and return as a string
# input: table_name: 'city', 'details', 'apartment' or 'address' are valid
# return: on success: a string representation of all the data in the specified data
#         on failure: 'Invalid table name'
def display_data(table_name):
    if table_name == 'apartment':
        apartments = db.session.query(Apartment).all()
        display = '{:3} | {:10} | {:10} | {:10} | {:6} | {:10} | {:10}'.format \
                 ('id', 'zpid', 'addressID', 'addressNum', 'rent', 'imgcount', 'imgNum')
        for apart in apartments:
            display = '\n'.join([display, '{:3} | {:10} | {:10} | {:10} | {:6} | {:10} | {:10}'.format \
                     (apart.id, apart.zpid, apart.address[0].id, len(apart.address), apart.rentPerMonth if apart.rentPerMonth is not None else 'None', apart.image_count, len(apart.image))])
    elif table_name == 'address':
        addresses = db.session.query(Address).all()
        display = '{:3} | {:30} | {:7} | {:10} | {:5} | {:3}'.format \
                 ('id', 'street', 'zipcode', 'city', 'state', 'aID')
        for address in addresses:
            display = '\n'.join([display, '{:3} | {:30} | {:6} | {:10} | {:5} | {}'.format \
                     (address.id, address.street, address.zipcode, address.city, address.state, address.apartment_id)])
    elif table_name == 'details':
        details = db.session.query(Details).all()
        display = '{:3} | {:3} | {:4} | {:8} | {:6} | {:20}'.format \
                 ('id', 'bed', 'bath', 'year_up', 'num_fl', 'parking type')
        for detail in details:
            display = '\n'.join([display, '{:3} | {:3} | {:4} | {:8} | {:6} | {}'.format \
                     (detail.id, detail.bedrooms if detail.bedrooms else 'None', detail.bathrooms if detail.bathrooms else 'None', detail.year_update if detail.year_update else 'None', \
                     detail.num_floor if detail.num_floor else 'None', detail.parking_type if detail.parking_type else 'None')])
    elif table_name == 'city':
        cities = db.session.query(City).all()
        display = '{:3} | {:10} | {:6}'.format('id', 'city', 'num_ap')
        for city in cities:
            display = '\n'.join([display, '{:3} | {:10} | {:6}'.format(city.id, city.name, len(city.apartments))])
    else:
        display = 'Invalid table name'
    print('%s data' % table_name)
    print(display)
    return display

# Request GetZestimate from zillow to for the address of a zpid
# input: zpid: the zpid of the apartment
# return: on success: a string representation of the address
#         on failure: a string of error code
def get_address(zpid):
    # request through GetZestimate API
    parameters = {'zws-id': ZillowAPI.zwsid, 'zpid': zpid, 'rentzestimate': True}
    response = requests.get("https://www.zillow.com/webservice/GetZestimate.htm", params=parameters)
    apart = fromstring(response.content)
    if apart.find('.//code').text != '0':
        return ('error code: ' + ' '
              + apart.find('.//code').text)
    else:
        return (apart.find('.//address/street').text + ' '
              + apart.find('.//address/city').text + ' '
              + apart.find('.//address/state').text)

# Add a new apartment to the database with address and zipcode
# input:
#   address: the address of the new apartment to add
#   zipcode: the zipcode of the new apartment to add
# used helper function:
#       handle_error()
#       rent_handler()
# return: on success: True
#         on failure: False
# possible errors:
#   1. apartment already exist:
#       handling: print 'Apartment already exists, adding failed' to console, return False
#   2. response is error:
#       handling: passes apartment into handle_error(), which prints error message and more
#                 return False
def add_new_apartment(address, zipcode):
    exist = db.session.query(Address).filter(Address.street == address).one_or_none()
    if exist:
        print('Apartment already exists, adding failed')
        return False
    # The following lines request a property info by address and zipcode
    parameters = {'zws-id': ZillowAPI.zwsid, 'address': address, \
                  'citystatezip': zipcode, 'rentzestimate': True}
    response = requests.get("http://www.zillow.com/webservice/GetSearchResults.htm", params=parameters)
    apart = fromstring(response.content)
    if apart.find('.//code').text != '0':
        handle_error(apart)
        return False
    else:
        if create_new_apartment(int(apart.find('.//zpid').text), rent_handler(apart)):
            return True

# Delete address from the database if its apartment_id is None
# print the deleted address id to the console
# return: the number of addresses deleted
def delete_extra_address():
    count = 0
    floating_addresses = db.session.query(Address).filter(Address.apartment_id == None).all()
    for address in floating_addresses:
        print('deleted address with id {}'.format(address.id))
        count += 1
        db.session.delete(address)
    db.session.commit()
    return count

# Delete unwanted address by its id
# input: id: the id of the address
# return: if the address exists: True
#         otherwise: False
def delete_address_by_id(id):
    this_address = db.session.query(Address).filter(Address.id == id).one_or_none()
    if this_address is None:
        return False
    db.session.delete(this_address)
    db.session.commit()
    return True

# Request GetUpdatedPropertyDetails and store the response
# input: zpid: the zpid to request
# return: a string specifying the name of new file created
def store_response_file(zpid):
    # request from GetUpdatedPropertyDetails API
    parameters = {'zws-id': ZillowAPI.zwsid, 'zpid': zpid}
    response = requests.get("https://www.zillow.com/webservice/GetUpdatedPropertyDetails.htm", params=parameters)
    xmlOfRoot = xml.dom.minidom.parseString(response.content)
    prettyXml = xmlOfRoot.toprettyxml()

    filename = str(zpid) + '.xml'
    file = open(filename, 'w+')
    file.write(prettyXml)
    file.close()
    return 'File written as %s' % filename

# Request GetComps and store the response
# inpust: zpid: the zpid to request
# return: a string specifying the name of new file created
def store_comps_file(zpid):
    parameters = {'zws-id': ZillowAPI.zwsid, 'zpid': zpid, 'count': 25, 'rentzestimate': True}
    response = requests.get("http://www.zillow.com/webservice/GetComps.htm", params=parameters)
    xmlOfRoot = xml.dom.minidom.parseString(response.content)
    prettyXml = xmlOfRoot.toprettyxml()
    filename = str(zpid) + '.xml'
    file = open(filename, 'w+')
    file.write(prettyXml)
    file.close()
    return 'File written as %s' % filename

## --------------- Internal Helper functions --------------------
# Handle erros of GetUpdatedPropertyDetails response
# print error messages to the console
# or delete the apartment if the data is protected
# input: apart: an ElementTree element object of the apartment
# used helper function: delete_if_exist()
def handle_error(apart):
    error_code = int(apart.find('.//code').text)
    if error_code < 10:
        print('Error code: %i. %s' % (error_code, apart.find('./message/text').text))
    elif error_code == 500:
        print('Error code: 500. The zpid parameter <%s> you have provided is not valid.' % apart.find('.//zpid').text)
    elif error_code == 501 or error_code == 502:
        print('Error code: %i. Apartment <%s>, %s' % (error_code, apart.find('.//zpid').text,
                                                      apart.find('./message/text').text))
        # if the data of this apartment is protected, delete this apartment from database
        delete_if_exist(int(apart.find('.//zpid').text))
    else:
        print('Unexpected error: %i.' % error_code)

# Request GetUpdatedPropertyDetails with zpid,
# Create a new apartment from the response
# Print zpid of the new apartment to console
# inputs:
#   Zpid: the zpid of the new apartment
#   rent: the rentzestimate of the new apartment
#         (info about rent is not available in GetUpdatedPropertyDetails)
# used helper function: handle_error()
# return: on success: True
#         on failure: False
def create_new_apartment(Zpid, rent):
    # request from GetUpdatedPropertyDetails API
    parameters = {'zws-id': ZillowAPI.zwsid, 'zpid': Zpid}
    response = requests.get("https://www.zillow.com/webservice/GetUpdatedPropertyDetails.htm", params=parameters)
    # root of this apartment
    apart = fromstring(response.content)
    # if the request returns an error
    if int(apart.find('.//code').text) != 0:
        handle_error(apart)
        return False
    # create a new address for this apartment
    new_address = Address(street=apart.find('.//address/street').text, \
                          zipcode=int(apart.find('.//address/zipcode').text), \
                          city=apart.find('.//address/city').text.capitalize(), \
                          state=apart.find('.//address/state').text, \
                          longitude=float(apart.find('.//address/longitude').text), \
                          latitude=float(apart.find('.//address/latitude').text))
    # a list of root of all image urls
    images = apart.findall('.//images/image/url')
    images_list = []
    for image_url in images:
        new_image = Image(url=image_url.text)
        images_list.append(new_image)

    image_count = len(images_list)

    # adding details to the apartment
    facts_root      = apart.find('.//editedFacts')
    bedrooms        = int(facts_root.find('./bedrooms').text) if facts_root.find('./bedrooms') != None else None
    bathrooms       = float(facts_root.find('./bathrooms').text) if facts_root.find('./bathrooms') != None else None
    area            = int(facts_root.find('./finishedSqFt').text) if facts_root.find('./finishedSqFt') != None else None
    lot_area        = int(facts_root.find('./lotSizeSqFt').text) if facts_root.find('./lotSizeSqFt') != None else None
    year_built      = int(facts_root.find('./yearBuilt').text) if facts_root.find('./yearBuilt') != None else None
    year_update     = int(facts_root.find('./yearUpdated').text) if facts_root.find('./yearUpdated') != None else None
    num_floor       = int(facts_root.find('./numFloors').text) if facts_root.find('./numFloors') != None else None
    basement        = facts_root.find('./basement').text if facts_root.find('./basement') != None else None
    view            = facts_root.find('./view').text if facts_root.find('./view') != None else None
    parking_type    = facts_root.find('./parkingType').text if facts_root.find('./parkingType') != None else None
    heating_source  = facts_root.find('./heatingSources').text if facts_root.find('./heatingSources') != None else None
    heating_system  = facts_root.find('./heatingSystem').text if facts_root.find('./heatingSystem') != None else None
    cooling         = facts_root.find('.//coolingSystem').text if facts_root.find('.//coolingSystem') != None else None

    details = Details(bedrooms=bedrooms, bathrooms=bathrooms, area=area, lot_area=lot_area, cooling_system=cooling,\
                      year_built=year_built, year_update=year_update, num_floor=num_floor, heating_system=heating_system,\
                      basement=basement, view=view, parking_type=parking_type, heating_source=heating_source)
    # add rooms
    rooms = []
    room_list = facts_root.find('./rooms').text.split(', ') if facts_root.find('./rooms') != None else []
    for name in room_list:
        rooms.append(Rooms(name=name))
    # add amentities
    amentities = []
    amentity_list = facts_root.find('./appliances').text.split(', ') if facts_root.find('./appliances') != None else []
    for name in amentity_list:
        amentities.append(Amentities(name=name))
    # add description
    description = apart.find('.//homeDescription').text if apart.find('.//homeDescription') != None else None
    # create a new apartment for this apartment
    new_apartment = Apartment(zpid=Zpid, \
                              rentPerMonth=rent, \
                              address=[new_address], \
                              image=images_list, \
                              image_count=image_count,\
                              comps=True,\
                              details=[details],\
                              rooms=rooms,\
                              amentities=amentities,\
                              review_number=0,\
                              average_rating=0,\
                              descripion=description)
    # adding cities
    cities = db.session.query(City).all()
    city_exist = False
    for city in cities:
        if new_address.city == city.name:
            city_exist = True
            city.apartments.append(new_apartment)
            break
    if not city_exist:
        new_city = City(name=new_address.city,\
                    apartments=[new_apartment])
        db.session.add(new_city)

    # Add this new apartment to our database
    if city_exist:
        db.session.add(new_apartment)
    db.session.commit()
    print('Created new apartment <%s>' % (Zpid))
    return True

# Request GetUpdatedPropertyDetails
# Update the apartment info of a existing apartment
# Print the updated apartment zpid to console
# inputs:
#   old_apart: a database object of the apartment to be updated
#   rent: the rentzestimate of this apartment
# used helper function: handle_error()
def update_apartment_info(old_apart, rent):
    is_updated = False
    # update the apartment rate if it changed
    if old_apart.rentPerMonth != rent:
        old_apart.rentPerMonth = rent
        is_updated = True
    # request from GetUpdatedPropertyDetails API
    parameters = {'zws-id': ZillowAPI.zwsid, 'zpid': old_apart.zpid}
    response = requests.get("https://www.zillow.com/webservice/GetUpdatedPropertyDetails.htm", params=parameters)
    # root of this apartment
    new_apart = fromstring(response.content)
    # if the request returns an error
    if int(new_apart.find('.//code').text) != 0:
        handle_error(new_apart)
        return
    # a list of root of all image urls
    images = new_apart.findall('.//images/image/url')
    image_list = old_apart.image
    # look through the old url list, if the new url is not there, add it
    for new_image_url in images:
        has_this_image = False
        for old_url in old_apart.image:
            if new_image_url.text == old_url.url:
                has_this_image = True
                break
        if not has_this_image:
            image_list.append(Image(url=new_image_url.text))
            is_updated = True
    image_count = len(image_list)
    old_apart.image_count = image_count
    old_apart.image = image_list
    db.session.commit()
    if is_updated:
        print('Updated apartment info <%i>' % old_apart.zpid)

# Delete an apartment by zpid from database if it exists
# Print the zpid of the deleted apartment to console
# input: zpid: the zpid of the apartment to be deleted
def delete_if_exist(zpid):
    exist_apart = db.session.query(Apartment).filter(Apartment.zpid == zpid).one_or_none()
    if exist_apart:
        print('Deleted apartment <%s> from database' % zpid)
        db.session.delete(exist_apart)
        db.session.commit()

# Handle the fact that some apartments have rentzestimate while others don't
# input: apart: the apartment element root
# return: if has rentzestimate: a float of the rent
#         otherwise: None
def rent_handler(apart):
    amount = apart.find('.//rentzestimate/amount')
    if amount != None:
        return float(amount.text)
    else:
        return None


def get_rent(zpid):
    parameters = {'zws-id': ZillowAPI.zwsid, 'zpid': zpid, 'rentzestimate': True}
    response = requests.get("http://www.zillow.com/webservice/GetZestimate.htm", params=parameters)
    root = fromstring(response.content)
    return rent_handler(root)
