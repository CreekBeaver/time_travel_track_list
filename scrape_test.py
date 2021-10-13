# ----------------------------- #
# Title: Scrape Test
# Desc: This is me attempting to learn how to scrape the internet
# Change Log: K.Creek | 10/12/2021 | Initial Revision
# ----------------------------- #

import requests
from bs4 import BeautifulSoup
import datetime


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

#test = non_api_scrape(3, '2021-10-09')
#for row in test:
#    print(test)

def find_sunday(date):
    """
    Function will take a given date and return the Sunday of that week
    :param date: string. Format YYYY-MM-DD
    :return: Date. String containing the sunday of that week in 'YYYY-MM-DD' format

    """
    # Split the string into three separate values
    date_list = date.split('-')

    # d places this into the date-time format.
    d = datetime.datetime(int(date_list[0]), int(date_list[1]), int(date_list[2]))
    if d.weekday() == 6:
        return date
    else:
        start = d - datetime.timedelta(days=d.weekday())
        sunday = start - datetime.timedelta(days=1)
        r_string = sunday.strftime('%Y-%m-%d')
        return r_string


d = find_sunday('2014-02-07')