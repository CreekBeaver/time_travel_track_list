from flask import Flask, render_template, json, request
import os
import datetime
from urllib.parse import quote
import json
import requests

# -- Define Helper Functions --


def data_verification(date, num_tracks):

	data_check = [True, 0]

	# -- Handle 0 Length date input
	if len(date) == 0 and len(num_tracks) == 0:
		error_string = "We're Sorry, it appears you need to enter a date and time"
		data_check[0] = False
		data_check[1] = error_string
		return data_check

	if len(date) == 0:
		error_string = "Please enter a date"
		data_check[0] = False
		data_check[1] = error_string
		return data_check

	if len(num_tracks) == 0:
		error_string = "Please enter a number of tracks"
		data_check[0] = False
		data_check[1] = error_string
		return data_check

	# -- To Do: Add Check to ensure that the Track List input is a positive integer.
	if int(num_tracks) < 1 or int(num_tracks) > 100:
		error_string = "I'm Sorry, you have entered either too many or two few tracks\n"
		error_string += "Please enter a number of tracks greater than 0, or less than 100"
		data_check[0] = False
		data_check[1] = error_string
		return data_check
	# -- To Do: Add Check to Make Sure that the Date is not in the Future

	# Split the date
	date_list = date.split('-')
	date_compare = datetime.datetime(int(date_list[0]), int(date_list[1]), int(date_list[2]))
	date_now = datetime.datetime.now()

	if date_compare > date_now:
		error_string = "I'm Sorry, your date is in the future, please try again with a different date"
		data_check[0] = False
		data_check[1] = error_string
		return data_check
	else:
		return data_check


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
	data = {'num_tracks': num_tracks, 'date': sunday}
	jsonData = json.dumps(data)
	print(jsonData)
	response = requests.post(url=url, json=jsonData)
	return_dict = response.json()

	return return_dict


def hyper_linker(track_dictionary):
	"""
	Takes a track list then returns a mirrored List with associated
	Youtube Query_Strings
	:param track_dictionary: Dictionary Containing Songs and Song Titles
	:return: Dictionary with hyperlinked Music
	"""

	return_dictionary = {}

	# Create the Return Dictionary to Pass to the Front End
	for key in track_dictionary:
		base_url = 'https://www.youtube.com/results?search_query=' + quote(key)
		return_dictionary[key] = [track_dictionary[key], base_url]

	return return_dictionary





# Configuration
app = Flask(__name__)


# Routes
@app.route('/', methods=['GET', 'POST'])
def root():
	# This will handle the initial requests to the Page
	if request.method == 'GET':
		return render_template('main.j2', error='')

	# This will handle when the button is pressed and cause everything to happen.
	if request.method == 'POST':
		if request.form.get('generate') == 'submit':
			date = request.form.get('date')
			num_tracks = request.form.get('num_tracks')
			print('here is date', type(date))

			data_check = data_verification(date, num_tracks)

			# Verify the Data
			if data_check[0] == False:
				return render_template('main.j2', error=data_check[1])
			else:
				# Create the Track List
				track_dictionary = tracklist_generator(int(num_tracks), date)

				# Create the Hyperlink List
				hyper_link_dictionary = hyper_linker(track_dictionary)

				# Make a Dictionary of the lists
				return render_template("main_track.j2", context=hyper_link_dictionary)


# Listener - Will Need to Change when loaded onto the server.
if __name__ == "__main__":
	port = int(os.environ.get("PORT", 9112))
	app.run(port=port, debug=True)