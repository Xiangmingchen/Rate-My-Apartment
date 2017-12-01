import requests
from xml.etree.ElementTree import fromstring, ElementTree
import xml.dom.minidom
from lxml import html, etree
from app import ZillowAPI, db
from sqlalchemy import create_engine, func
from app.models import Apartment, Address, Image, Review

## --------------- Interface functions --------------------
# Update the entire database
# return: nothing
# used helper functions: update_apartment_info()
# possible erros: none
def update_database():
    current_list = db.session.query(Apartment).all()
    for apartment in current_list:
        update_apartment_info(apartment, apartment.rentPerMonth)

# Request GetComps from Zillow based on zpid, add new apartments to the database
# This fuction will not request if the zpid has been center_requested before
# input: zpid: the center zpid of the request
# return: on success: number of new apartments added
#         on failture: False
# used helpe functions: create_new_apartment
# possible errors:
#   1. Comp error: when GetComps returns error
#       handling: print error message to console, return False
def center_request(zpid):
    # check whether this apartment has been a center of request
    thisApart = db.session.query(Apartment).filter(Apartment.zpid == zpid[0]).one_or_none()
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
        thisApart = db.session.query(Apartment).filter(Apartment.zpid == zpid[0]).one_or_none()
        if thisApart is None:  # if this apartment is not in our database, add it to database
            if create_new_apartment(zpid, rent_handler(apart)):
                new_apart_count += 1
        # else: # otherwise update the info for this apartment
        #     update_apartment_info(thisApart, float(apart.find('./rentzestimate/amount').text))
        # compzpidlist.append(zpid)
    thisApart.comps = False
    db.session.commit()
    return new_apart_count

# Expand database by center requesting every zpid in database
# return: total number of new added apartments
# used helpter functions: center_request()
# possible errors: none
def expand_database():
    zpid_list = db.session.query(Apartment.zpid).all()
    new_apart_count = 0
    for zpid in zpid_list:
        new_apart_count += center_request(zpid)
    return new_apart_count

# Count how many rows are in the target table, same as number of entries in the database
# input: table_name: lowercased table name
# return: on success: number of rows in the table
#         on failture: -1
# possible errors:
#   1. table doesn't exist:
#       handling: return -1
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
    else:
        count = -1
    return count

# 
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
                          city=apart.find('.//address/city').text.title(), \
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

    # create a new apartment for this apartment
    new_apartment = Apartment(zpid=Zpid, \
                              rentPerMonth=rent, \
                              address=[new_address], \
                              image=images_list, \
                              image_count=image_count,\
                              comps=True)
    # Add this new apartment to our database
    db.session.add(new_apartment)
    db.session.commit()
    print('Created new apartment <%i>' % Zpid)
    return True


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
    if old_apart.address[0].longitude is None:
        # add longitude and latitude to the old apartments
        old_apart.address[0].longitude = float(new_apart.find('.//address/longitude').text)
        old_apart.address[0].latitude = float(new_apart.find('.//address/latitude').text)
        print('Updated longitude <%s> latitude <%s> for apartment <%i>' % (new_apart.find('.//address/longitude').text, new_apart.find('.//address/latitude').text, old_apart.zpid))
    db.session.commit()
    if is_updated:
        print('Updated apartment info <%i>' % old_apart.zpid)





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
    else:
        display = 'Invalid table name'
    print('%s data' % table_name)
    print(display)
    return display


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
    else:
        if create_new_apartment(int(apart.find('.//zpid').text), rent_handler(apart)):
            return True
    return False

def delete_if_exist(zpid):
    # delete the photos of this apartment
    exist_apart = db.session.query(Apartment).filter(Apartment.zpid == zpid).one_or_none()
    if exist_apart:
        print('Deleted apartment <%s> from database' % zpid)
        db.session.delete(exist_apart)
        db.session.commit()

def rent_handler(apart):
    amount = apart.find('.//rentzestimate/amount')
    if amount:
        return float(amount.text)
    else:
        return None

def delete_extra_address():
    count = 0
    floating_addresses = db.session.query(Address).filter(Address.apartment_id == None).all()
    for address in floating_addresses:
        print('deleted address with id {}'.format(address.id))
        count += 1
        db.session.delete(address)
    db.session.commit()
    return count

def delete_address_by_id(id):
    this_address = db.session.query(Address).filter(Address.id == id).one_or_none()
    if this_address is None:
        return False
    db.session.delete(this_address)
    db.session.commit()
    return True

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
