import requests
from xml.etree.ElementTree import fromstring, ElementTree
import xml.dom.minidom
from app import ZillowAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import Apartment, Address
from app.query import session

def request():
    # The following lines request a property info by address and zipcode
    '''
    parameters = {'zws-id': ZillowAPI.zwsid, 'address': '1109 W Stoughton St', \
      'citystatezip': '61801', 'rentzestimate': True}
    response = requests.get("http://www.zillow.com/webservice/GetSearchResults.htm", params=parameters)
    '''

    # The following lines request 10 more property info with one known zpid
    parameters = {'zws-id': ZillowAPI.zwsid, 'zpid': 3225056, 'count': 25, 'rentzestimate': True}
    response = requests.get("http://www.zillow.com/webservice/GetComps.htm", params=parameters)


    # root of the entire document
    root = fromstring(response.content)

    # create a pretty version of the response and print it
    '''
    xmlOfRoot = xml.dom.minidom.parseString(response.content)
    prettyXml = xmlOfRoot.toprettyxml()
    print(prettyXml)
    '''

    # Create lists of each info type and retreive info from the root
    zpidList = root.findall('.//response//zpid')
    addressList = root.findall('.//response//address')
    rentList = root.findall('.//response//rentzestimate/amount')

    # Store the apartments info into database
    for i in range(len(zpidList)):
        thisA = session.query(Apartment).filter(Apartment.zpid == int(zpidList[i].text)).all()
        if len(thisA) == 0:
            new_address = Address(street=addressList[i].find('street').text, \
                                  zipcode=int(addressList[i].find('zipcode').text), \
                                  city=addressList[i].find('city').text, \
                                  state=addressList[i].find('state').text)

            new_apartment = Apartment(zpid=int(zpidList[i].text), \
                                      rentPerMonth=float(rentList[i].text), \
                                      address=[new_address])

            session.add(new_address)
            session.add(new_apartment)

            session.commit()
        else:
            thisA[0].rentPerMonth = float(rentList[i].text)
            session.commit()
