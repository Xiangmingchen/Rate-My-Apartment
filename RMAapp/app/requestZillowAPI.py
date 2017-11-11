import requests
from xml.etree.ElementTree import fromstring, ElementTree
import xml.dom.minidom
from lxml import html, etree
from app import ZillowAPI, db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Apartment, Address, Image



def update_database():
    current_list = db.session.query(Apartment).all()
    for apartment in current_list:
        update_apartment_info(apartment, apartment.rentPerMonth)

def delete_if_exist(zpid):
    # delete the photos of this apartment
    exist_apart = db.session.query(Apartment).filter(Apartment.zpid == zpid).one_or_none()
    if exist_apart:
        print('Deleted apartment: %s from database' % zpid)
        db.session.delete(exist_apart)
        db.session.commit()

def handle_error(apart):
    error_code = int(apart.find('.//code').text)
    if error_code == 1:
        print('Error code 1. There was a server-side error while processing the request\nCheck to see if your url is properly formed.')
    elif error_code == 2:
        print('Error code 2. The specified ZWSID parameter was invalid or not specified in the request')
    elif error_code == 3:
        print('Error code 3. The specified ZWSID parameter was invalid or not specified in the request\nPlease come back later and try again.')
    elif error_code == 4:
        print('Error code 4. The API call is currently unavailable')
    elif error_code == 500:
        print('Error code 500. The zpid parameter <%s> you have provided is not valid.' % (apart.find('.//zpid').text))
    elif error_code == 501:
        print('Error code 501. The Protected data (zpid: %s) is unavailable through API' % (apart.find('.//zpid').text))
        # if the data of this apartment is protected, delete this apartment from database
        delete_if_exist(int(apart.find('.//zpid').text))
    elif error_code == 502:
        print('Error code 502. No updated data is available for this property (zpid: %s)' % (apart.find('.//zpid').text))
        delete_if_exist(int(apart.find('.//zpid').text))

def create_new_apartment(Zpid, rent):
    # request from GetUpdatedPropertyDetails API
    parameters = {'zws-id': ZillowAPI.zwsid, 'zpid': Zpid}
    response = requests.get("https://www.zillow.com/webservice/GetUpdatedPropertyDetails.htm", params=parameters)
    # root of this apartment
    apart = fromstring(response.content)
    # if the request returns an error
    if int(apart.find('.//code').text) != 0:
        handle_error(apart)
        return
    # create a new address for this apartment
    new_address = Address(street=apart.find('.//address/street').text, \
                          zipcode=int(apart.find('.//address/zipcode').text), \
                          city=apart.find('.//address/city').text, \
                          state=apart.find('.//address/state').text)
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
                              image_count=image_count)
    # Add this new apartment and new address to our database
    db.session.add(new_address)
    db.session.add(new_apartment)
    db.session.commit()

def update_apartment_info(old_apart, rent):
    old_apart.rentPerMonth = rent
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
    for new_image_url in images:
        has_this_image = False
        for old_url in old_apart.image:
            if new_image_url.text == old_url.url:
                has_this_image = True
                break
        if not has_this_image:
            image_list.append(Image(url=new_image_url.text))
    image_count = len(image_list)
    old_apart.image_count = image_count
    old_apart.image = image_list
    db.session.commit()

def centerRequest(zpid):
    # The following lines request a property info by address and zipcode
    '''
    parameters = {'zws-id': ZillowAPI.zwsid, 'address': '1109 W Stoughton St', \
      'citystatezip': '61801', 'rentzestimate': True}
    response = requests.get("http://www.zillow.com/webservice/GetSearchResults.htm", params=parameters)
    '''

    # The following lines request 25 more property info with one known zpid
    parameters = {'zws-id': ZillowAPI.zwsid, 'zpid': zpid, 'count': 25, 'rentzestimate': True}
    response = requests.get("http://www.zillow.com/webservice/GetComps.htm", params=parameters)


    # root of the entire document
    root = fromstring(response.content)

    # Create lists of each info type and retreive info from the root
    compList = root.findall('.//properties/comparables/comp')

    # Store the apartments info into database
    for apart in compList:
        thisA = db.session.query(Apartment).filter(Apartment.zpid == int(apart.find('./zpid').text)).all()
        if len(thisA) == 0:
            # if this apartment is not in our database, add it to database
            # the if is for debug
            create_new_apartment(int(apart.find('./zpid').text), \
                                 float(apart.find('./rentzestimate/amount').text))
        else:
            update_apartment_info(thisA[0], float(apart.find('./rentzestimate/amount').text))
        # to see whether each zpid's comp are the same list of zpids
        print(apart.find('./zpid').text)
