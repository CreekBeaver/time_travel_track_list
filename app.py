from flask import Flask, render_template, json, request
import os
import datetime
from urllib.parse import quote
import json
import requests
import random

# -- Define Helper Functions --


def data_verification(date, num_tracks):
	"""
	data_verification performs a check on the form information for
	Time Travel Track List to ensure that the users input is
	valid
	:param date: string representing date input from form
	:param num_tracks:  string representing number of tracks from form
	:return: List, containing boolean information if legit. and string for error to display
	"""

	# Initial data check values assume good information is passed via form.
	data_check = [True, 0]

	# -- Handle 0 Length date input
	if len(date) == 0 and len(num_tracks) == 0:
		error_string = "Please Provide a Date (Prior to Today) and Number of Desired Tracks"
		data_check[0] = False
		data_check[1] = error_string
		return data_check

	# Handles no Date Input
	if len(date) == 0:
		error_string = "Please enter a date"
		data_check[0] = False
		data_check[1] = error_string
		return data_check

	# Handles no track number input
	if len(num_tracks) == 0:
		error_string = "Please enter a number of tracks"
		data_check[0] = False
		data_check[1] = error_string
		return data_check

	# Check to ensure that the Track List input is a positive integer.
	if int(num_tracks) < 1 or int(num_tracks) > 100:
		error_string = "I'm Sorry, you have entered either too many or two few tracks\n"
		error_string += "Please enter a number of tracks greater than 0, or less than 100"
		data_check[0] = False
		data_check[1] = error_string
		return data_check

	# Check to Make Sure that the Date is not in the Future
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
	# Weekday of 6 means the day is already a Sunday
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
	a microservice to generate a random track list. It will return a dictionary of
	songs as the key and the corresponding artist as the value
	:param num_tracks: Number of Desired Tracks to be generated
	:param date: Date from which the information is pulled from the Billboard 100
	:return: Dictionary the length of num_tracks, containing song : artist
	key value pairing from the provided date.
	"""

	# Data is Sanitized when this function is called. Call microservice with the
	# sunday corresponding to the provided date.
	sunday = find_sunday(date)

	# Build an HTTP Request for the service
	url = 'http://flip1.engr.oregonstate.edu:4519'
	data = {'num_tracks': num_tracks, 'date': sunday}
	jsonData = json.dumps(data)

	# Call the microservice
	print("Calling the microservice @ ", url, 'with', jsonData)
	response = requests.post(url=url, json=jsonData)
	return_dict = response.json()
	print(return_dict)

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

# -- Start App Definition


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

			# Validate that the provided data is acceptable.
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


@app.route('/random', methods=['GET', 'POST'])
def random_list():
	if request.method == 'GET':
		return render_template('main.j2', error='')

	# How to handle a random response
	if request.method == 'POST':
		# Generate the Random Date
		start_date = datetime.date(1958, 11, 1)
		end_date = datetime.date.today()
		time_delta = end_date - start_date
		day_delta = time_delta.days
		random_num_days = random.randrange(day_delta)
		rand_date = str(start_date + datetime.timedelta(days=random_num_days))



		# Generate the Random Track
		num_tracks = random.randint(1, 100)


		# Create the Track List
		track_dictionary = tracklist_generator(int(num_tracks), rand_date)

		# Create the Hyperlink List
		hyper_link_dictionary = hyper_linker(track_dictionary)

		# Make a Dictionary of the lists
		return render_template("main_track.j2", context=hyper_link_dictionary)




# Listener - Will Need to Change when loaded onto the server.
if __name__ == "__main__":
	port = int(os.environ.get("PORT", 9112))
	# app.run()
	app.run(port=port, debug=True)