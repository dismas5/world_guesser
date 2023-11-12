from ctypes import sizeof
from logging import debug
from flask import Flask, render_template, request, session, flash
from consts import *
import requests
import xml.etree.ElementTree as ET

application = Flask(__name__, static_folder='static')

def update_countries_list(selected_continent):
    countries_map = {}
    response = requests.post(soap_url, headers=soap_headers, data=countries_names_request)

    if response.status_code != 200:
        return countries_map
    
    xml_response = response.content
    root = ET.fromstring(xml_response)

    tcc_grouped_by_continent_elements = root.findall('.//{http://www.oorsprong.org/websamples.countryinfo}tCountryCodeAndNameGroupedByContinent')

    for tcc_group in tcc_grouped_by_continent_elements:
        continent_name = tcc_group.find('.//{http://www.oorsprong.org/websamples.countryinfo}sName').text
        country_elements = tcc_group.findall('.//{http://www.oorsprong.org/websamples.countryinfo}tCountryCodeAndName')

        for country_element in country_elements:
            country_name = country_element.find('.//{http://www.oorsprong.org/websamples.countryinfo}sName').text
            if continent_name.strip() == selected_continent:
                countries_map[country_name] = False
    
    return countries_map


@application.route('/')
def index():
    response = requests.post(soap_url, headers=soap_headers, data=continents_request)

    continent_names = []

    if response.status_code != 200:
        return
       
    xml_response = response.content
    root = ET.fromstring(xml_response)
    
    namespaces = {'ns': 'http://www.oorsprong.org/websamples.countryinfo'}
    continents = root.findall('.//ns:tContinent/ns:sName', namespaces)

    for continent in continents:
        continent_names.append(continent.text)

    return render_template('index.html', continent_names=continent_names)

@application.route('/guesser', methods=['GET', 'POST'])
def guesser():
    if request.referrer == request.url_root:
       session.pop('counter', None)
       session.pop('countries_info', None)
       session.pop('continent', None)

    continent = request.form.get('selectedContinent')
    if continent is not None:
        session['continent'] = continent

    countries_info = session.get('countries_info', update_countries_list(continent))
    print(countries_info)
    session['countries_info'] = countries_info

    if request.method == 'POST':
        guess = request.form.get('guessInput')
        if guess in countries_info.keys() and countries_info[guess] == False:
            session['counter'] = session.get('counter', 0) + 1
            countries_info[guess] = True

    count = session.get('counter', 0)

    if count == len(countries_info):
        flash('Congratulations! You won!', 'success')

    return render_template('guesser.html', guess=guess, country_count=len(countries_info), count=count, countries_list=list(countries_info.keys()))

if __name__ == '__main__':
    application.secret_key = 'your_secret_key'
    application.run(debug=True)
