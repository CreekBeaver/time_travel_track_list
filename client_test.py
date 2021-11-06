import datetime
import json
import requests
from urllib.parse import quote

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


def tracklist_generator(num_tracks, date):
    """
    tracklist_generator will take a provided number of tracks and date and call on
    a microservice to generate a random track list. It will return a list of songs
    :param num_tracks:
    :param date:
    :return:
    """

    # This will sanize to ensure that the date is the sunday for the query string.

    sunday = find_sunday(date)

    # -- To Do: Build an HTTP Request for the service
    url = 'http://flip1.engr.oregonstate.edu:4519'
    data = {'num_tracks': num_tracks, 'date': sunday }
    jsonData = json.dumps(data)
    print(jsonData)
    response = requests.post(url=url, json=jsonData)
    return_dict = response.json()

    return return_dict

def hyper_linker(track_dictionary):
    """
    Takes a track list then returns a mirrored List with associated
    Youtube Query_Strings
    :param track_list: Dictionary Containing Songs and Song Titles
    :return: Dictionary with hyperlinked Music
    """

    return_dictionary = {}

    # Create the Return Dictionary to Pass to the Front End
    for key in track_dictionary:
        base_url = 'https://www.youtube.com/results?search_query=' + quote(key)
        return_dictionary[key] = [track_dictionary[key], base_url]

    return return_dictionary


dict = tracklist_generator(20, '2021-10-24')
hyper_linker(dict)
