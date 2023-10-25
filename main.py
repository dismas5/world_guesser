import requests
import xml.etree.ElementTree as ET

# Define the URL and the SOAP XML payload
url = 'http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso'
headers = {
    'Content-Type': 'application/soap+xml; charset=utf-8'
}
soap_payload = '''
<soap12:Envelope xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <ListOfContinentsByCode xmlns="http://www.oorsprong.org/websamples.countryinfo">
    </ListOfContinentsByCode>
  </soap12:Body>
</soap12:Envelope>
'''

# Make the HTTP POST request
response = requests.post(url, headers=headers, data=soap_payload)

# Check if the request was successful
if response.status_code == 200:
    # Parse the XML response
    xml_response = response.content
    root = ET.fromstring(xml_response)

    # Find the elements with continent names
    namespaces = {'ns': 'http://www.oorsprong.org/websamples.countryinfo'}
    continents = root.findall('.//ns:tContinent/ns:sName', namespaces)

    # Extract and print the continent names
    for continent in continents:
        print(continent.text)
else:
    print(f"Request failed with status code: {response.status_code}")
