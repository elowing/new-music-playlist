from gmusicapi import Mobileclient
import os

USER = os.environ.get('GOOGLE_PERSONAL_USER')
PASS = os.environ.get('GOOGLE_PERSONAL_PASS')

api = Mobileclient()
api.login(USER, PASS, Mobileclient.FROM_MAC_ADDRESS)

# from pdb import set_trace; set_trace()
library = api.get_all_songs()
sweet_track_ids = [track['id'] for track in library
                   if track['artist'] == 'The Cat Empire']

results = api.search_all_access('query')

playlist_id = api.create_playlist('Rad muzak')
api.add_songs_to_playlist(playlist_id, sweet_track_ids)
