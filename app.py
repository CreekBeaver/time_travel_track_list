from flask import Flask, render_template, json, request
import random
import os

# Define Helper Functions
def tracklist_generator(num_tracks, date):
	"""
	tracklist_generator will take a provided number of tracks and date and call on
	a microservice to generate a random track list. It will return a list of songs
	:param num_tracks:
	:param date:
	:return:
	"""

	#-- This will need internal checks to sanitize the data. --#

	# Once Sanitized, send the data to the Microservice

	# After Recieved from the microservice, Translate the data into something readable
	# raw_tracks = [Call to microservice]

	raw_tracks = []
	for i in range(1, 100):
		raw_tracks.append(i)

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
			#date = request.form.get('date')
			num_tracks = request.form.get('num_tracks')
			#list = tracklist_generator(num_tracks, date)
			track_list = tracklist_generator(int(num_tracks), 'placeholder')
		return render_template("main_track.j2", tracks=track_list)


# Listener
if __name__ == "__main__":
	port = int(os.environ.get("PORT", 9112))
	app.run(port=port, debug=True)