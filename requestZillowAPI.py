import requests
from xml.etree.ElementTree import fromstring, ElementTree
import xml.dom.minidom
from classApartment import Apartment
from ZillowAPI import zwsid

# The following lines request a property info by address and zipcode
'''
parameters = {'zws-id': zwsid, 'address': '1109 W Stoughton St', \
  'citystatezip': '61801', 'rentzestimate': True}
response = requests.get("http://www.zillow.com/webservice/GetSearchResults.htm", params=parameters)
'''

# The following lines request 10 more property info with one known zpid
parameters = {'zws-id': zwsid, 'zpid': 89056297, 'count': 25, 'rentzestimate': True}
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

# Create a list of apartments and store info into it
apartmentList = []
for i in range(len(zpidList)):
    zpid = int(zpidList[i].text)
    rent = int(rentList[i].text)
    address = addressList[i].find('street').text + ', ' \
        + addressList[i].find('zipcode').text + ', ' + addressList[i].find('city').text \
        + ', ' + addressList[i].find('state').text
    apartmentList.append(Apartment(zpid))
    apartmentList[i].set_rate(rent)
    apartmentList[i].set_address(address)


# Testing: print the length of apartmentList
print('The length of apartmentList is ',len(apartmentList))
print(Apartment.apartCount)

# Print each apartment info
for i in range(len(apartmentList)):
    apartmentList[i].display_info()
