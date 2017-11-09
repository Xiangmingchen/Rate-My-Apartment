import requests
from xml.etree.ElementTree import fromstring, ElementTree
import xml.dom.minidom
from lxml import html, etree
from app import ZillowAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import Apartment, Address, Image
from app.query import session



def findimage(url):
    return

def create_new_apartment(Zpid, rent):
    # request from GetUpdatedPropertyDetails API
    parameters = {'zws-id': ZillowAPI.zwsid, 'zpid': Zpid}
    response = requests.get("https://www.zillow.com/webservice/GetUpdatedPropertyDetails.htm", params=parameters)
    # root of this apartment
    apart = fromstring(response.content)
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


    # create a new apartment for this apartment
    new_apartment = Apartment(zpid=Zpid, \
                              rentPerMonth=rent, \
                              address=[new_address], \
                              image=images_list)
    # Add this new apartment and new address to our database
    session.add(new_address)
    session.add(new_apartment)
    session.commit()

def update_apartment_info(old_apart, rent):
    old_apart.rentPerMonth = rent
    # request from GetUpdatedPropertyDetails API
    parameters = {'zws-id': ZillowAPI.zwsid, 'zpid': old_apart.zpid}
    response = requests.get("https://www.zillow.com/webservice/GetUpdatedPropertyDetails.htm", params=parameters)
    # root of this apartment
    new_apart = fromstring(response.content)
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
    old_apart.image = image_list
    session.commit()

def centerRequest(zpid):
    # The following lines request a property info by address and zipcode
    '''
    parameters = {'zws-id': ZillowAPI.zwsid, 'address': '1109 W Stoughton St', \
      'citystatezip': '61801', 'rentzestimate': True}
    response = requests.get("http://www.zillow.com/webservice/GetSearchResults.htm", params=parameters)
    '''

    # The following lines request 10 more property info with one known zpid
    parameters = {'zws-id': ZillowAPI.zwsid, 'zpid': zpid, 'count': 25, 'rentzestimate': True}
    response = requests.get("http://www.zillow.com/webservice/GetComps.htm", params=parameters)


    # root of the entire document
    root = fromstring(response.content)

    # Create lists of each info type and retreive info from the root
    compList = root.findall('.//properties/comparables/comp')

    # Store the apartments info into database
    for apart in compList:
        thisA = session.query(Apartment).filter(Apartment.zpid == int(apart.find('./zpid').text)).all()
        if len(thisA) == 0:
            # if this apartment is not in our database, add it to database
            create_new_apartment(int(apart.find('./zpid').text), float(apart.find('./rentzestimate/amount').text))

        else:
            update_apartment_info(thisA[0], float(apart.find('./rentzestimate/amount').text))
