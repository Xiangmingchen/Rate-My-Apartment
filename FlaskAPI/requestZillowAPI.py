import requests
from xml.etree.ElementTree import fromstring, ElementTree
import xml.dom.minidom
from ZillowAPI import zwsid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Address, Base, Apartment
from centerID import zpid

# The following lines request a property info by address and zipcode
'''
parameters = {'zws-id': zwsid, 'address': '1109 W Stoughton St', \
  'citystatezip': '61801', 'rentzestimate': True}
response = requests.get("http://www.zillow.com/webservice/GetSearchResults.htm", params=parameters)
'''

# The following lines request 10 more property info with one known zpid
parameters = {'zws-id': zwsid, 'zpid': zpid, 'count': 10, 'rentzestimate': True}
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


engine = create_engine('sqlite:///apartments.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()



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









# new_person = Person(name='new person')
# session.add(new_person)
# session.commit()
#
