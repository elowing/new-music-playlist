import os

import gmusicapi
from lxml import html
import requests

USER = os.environ.get('GOOGLE_USER')
PASS = os.environ.get('GOOGLE_PASS')


def main():
    pitchfork()
    google_music()


def pitchfork():
    page = requests.get('http://pitchfork.com/best/high-scoring-albums')
    tree = html.fromstring(page.content)

    artists = tree.xpath('//*[@id="main"]/ul/li/ul/li/a/div[2]/h1/text()')
    albums = tree.xpath('//*[@id="main"]/ul/li/ul/li/a/div[2]/h2/text()')
    return zip(artists, albums)


def google_music():
    api = gmusicapi.Mobileclient()
    api.login(USER, PASS, gmusicapi.Mobileclient.FROM_MAC_ADDRESS)

    library = api.get_all_songs()
    sweet_track_ids = [track['id'] for track in library
                       if track['artist'] == 'The Cat Empire']

    # results = api.search_all_access('query')

    playlist_id = api.create_playlist('Rad muzak')
    api.add_songs_to_playlist(playlist_id, sweet_track_ids)

if __name__ == '__main__':
    main()
