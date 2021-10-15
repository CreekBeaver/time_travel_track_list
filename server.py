from flask import Flask, request
import os
import json
import requests

# Configuration
app = Flask(__name__)

# Routes
import requests
from bs4 import BeautifulSoup
import datetime
import re

def medicine_scrape(medicine_name):
    # Wikipedia URL: https://en.wikipedia.org/wiki/[name]
    wiki_url = 'https://en.wikipedia.org/wiki/' + str(medicine_name)

    # Call the Wikipedia
    wiki_response = requests.get(wiki_url)
    soup = BeautifulSoup(wiki_response.content, 'html.parser')

    # Need to extract the Medline Plus URL
    # medline_url = soup.find_all('a', {'class' : 'external text'}, href=True)
    medline_url = soup.find('a', attrs={'href': re.compile("^https://medlineplus.gov")}).get('href')

    # Now call the medline Plus URL
    medline_response = requests.get(medline_url)

    # Clean up the medline HTML
    soup2 = BeautifulSoup(medline_response.content, 'html.parser')
    how_section = soup2.find('div', attrs={'id': 'how', })
    how_section2 = how_section.find_all('div', class_='section-body')
    description = how_section2[0].text.strip()

    return {'url': medline_url, 'howToTake': description}


def non_api_scrape(date):
    """
    This is an attempt to scrape the billboard 100 without an API
    :param date: Date in
    :return: List of songs
    """

    # Need to Find a way to determine the week start of the date.

    # querystring = https://www.billboard.com/charts/hot-100/YYYY-MM-DD
    query_string = 'https://www.billboard.com/charts/hot-100/' + date

    response = requests.get(query_string)
    soup = BeautifulSoup(response.content, 'html.parser')
    # This will get us the HTML for all the Spans that have the songs. Now I need to Put them in a list
    track_html_list = soup.find_all("span", class_="chart-element__information__song text--truncate color--primary")


    # Clean up the HTML From the List
    clean_list = []
    for track in track_html_list:
        clean_list.append(track.text.strip())

    return clean_list

@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'GET':
        print('Get Request Recieved')

        return "Response to a Get Request"
    if request.method == 'POST':
        # This gets the String Data in String form from the request
        request_json = request.get_json()

        # This will parse the string into a dicitonary
        in_dict = json.loads(request_json)

        # Call the Function that will form the response
        server_response = medicine_scrape(in_dict['name'])

        return json.dumps(server_response)

# Listener


if __name__ == '__main__':
    app.run(port=9115, debug=True)