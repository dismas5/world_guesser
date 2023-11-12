universal_soap_request = '''
<soap12:Envelope xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <{0} xmlns="http://www.oorsprong.org/websamples.countryinfo">
    </{0}>
  </soap12:Body>
</soap12:Envelope>
'''

countries_names_request = universal_soap_request.format('ListOfCountryNamesGroupedByContinent')
continents_request = universal_soap_request.format('ListOfContinentsByCode')

soap_url = 'http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso'
soap_headers = {
    'Content-Type': 'application/soap+xml; charset=utf-8'
}
