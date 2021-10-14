from flask import Flask, render_template, json, request
import random
import os
import datetime
from scrape_test import non_api_scrape
from urllib.parse import quote
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
		base_url = 'https://www.youtube.com/results?search_query='+ quote(track)
		return_list.append(base_url)

	return return_list


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

	return return_list

def zipper(l1, l2):
	i = 0
	d = {}
	while i < len(l1):
		d[l1[i]] = l2[i]
		i += 1
	return d

def data_verification(date, num_tracks):

	data_check = [True,0]

	# -- Handle 0 Length date input
	if len(date) == 0 and len(num_tracks) == 0:
		error_string = "We're Sorry, it appaers you need to enter a date and time"
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
				track_list = tracklist_generator(int(num_tracks), date)

				# Create the Hyperlink List
				hyper_link_list = hyper_linker(track_list)

				# Make a Dictionary of the lists
				track_dictionary = zipper(track_list, hyper_link_list)
				return render_template("main_track.j2", context=track_dictionary, tracks=track_list, hyperlink=hyper_link_list)


# Listener
if __name__ == "__main__":
	port = int(os.environ.get("PORT", 9112))
	app.run(port=port, debug=True)