from flask import Flask, render_template, json, request
import random
import os
import datetime
from scrape_test import non_api_scrape
# Define Helper Functions


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


def hyper_linker(track_list):
	"""
	Takes a track list then returns a mirrored List with associated
	Youtube Query_Strings
	:param track_list: List containing tracks
	:return: Hyperlinks for each track
	"""

	return_list = []

	for track in track_list:
		base_url = 'https://www.youtube.com/results?search_query='
		# Split the tracks into their components:
		split_track = track.split(" ")
		# -- To Do: Find a Way To Strip the special characters
		# handle one length tracks
		if len(split_track) == 1:
			base_url += split_track[0]
			return_list.append(base_url)
		else:
			pass

	return return_list


def tracklist_generator(num_tracks, date):
	"""
	tracklist_generator will take a provided number of tracks and date and call on
	a microservice to generate a random track list. It will return a list of songs
	:param num_tracks:
	:param date:
	:return:
	"""

	# -- To Do: Add Check to ensure that the Track List input is a positive integer.
	# -- To Do: Verify that the Number of Tracks Does Not Exceed 100.
	# -- To Do: Add Check to Make Sure that the Date is not in the Future
	# This will sanize to ensure that the date is the sunday for the query string.
	sunday = find_sunday(date)

	#Build an HTTP Request for the service


	# After Recieved from the microservice, Translate the data into something readable
	raw_tracks = non_api_scrape(sunday)

	# --- Randomly Select tracks from a list to return ---#
	return_list = []
	while len(return_list) < num_tracks:
		# Generate a Random value based on the remaining raw_track list size
		index = random.randint(0, len(raw_tracks)-1) # random.randint = N such that a <= N <= B

		# Append the Track to the return List
		return_list.append(raw_tracks[index])

		# Remove the track from the raw_tracks List
		raw_tracks.pop(index)

	# This is where I will Call to Hyperlink each of the tracks in the list

	return return_list


def hyperlinker(track_lsit):
	"""
	hperlinker will take an input track list and return the same list in the form of hyperlinks
	where the users can hear the songs within the playlist.
	:param track_lsit:
	:return:
	"""

	# This will also require some kind of data sanitization
	pass


# Configuration
app = Flask(__name__)


# Routes
@app.route('/', methods=['GET', 'POST'])
def root():
	# This will handle the initial requests to the Page
	if request.method == 'GET':
		return render_template('main.j2')

	# This will handle when the button is pressed and cause everything to happen.
	if request.method == 'POST':
		if request.form.get('generate') == 'submit':
			date = request.form.get('date')
			print('here is the date', date)
			num_tracks = request.form.get('num_tracks')
			#list = tracklist_generator(num_tracks, date)
			track_list = tracklist_generator(int(num_tracks), date)
		return render_template("main_track.j2", tracks=track_list)


# Listener
if __name__ == "__main__":
	port = int(os.environ.get("PORT", 9112))
	app.run(port=port, debug=True)