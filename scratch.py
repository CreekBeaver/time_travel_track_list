import random

def tracklist_generator(num_tracks, date):
    """
    tracklist_generator will take a provided number of tracks and date and call on
    a microservice to generate a random track list. It will return a list of songs
    :param num_tracks:
    :param date:
    :return:
    """

    # This will need internal checks to sanitize the data.

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
        index = random.randint(0, len(raw_tracks) - 1)  # random.randint = N such that a <= N <= B

        # Append the Track to the return List
        return_list.append(raw_tracks[index])

        # Remove the track from the raw_tracks List
        raw_tracks.pop(index)

    # This is where I will Call to Hyperlink each of the tracks in the list

    return return_list

l = tracklist_generator(10, 'test')
print(l)