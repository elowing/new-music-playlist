import os

import gmusicapi
from lxml import html
import requests

USER = os.environ.get('GOOGLE_USER')
PASS = os.environ.get('GOOGLE_PASS')


def main():
    best_new_releases = pitchfork()
    google_music(best_new_releases)


def pitchfork():
    page = requests.get('http://pitchfork.com/best/high-scoring-albums')
    tree = html.fromstring(page.content)

    artists = tree.xpath('//*[@id="main"]/ul/li/ul/li/a/div[2]/h1/text()')
    albums = tree.xpath('//*[@id="main"]/ul/li/ul/li/a/div[2]/h2/text()')
    return zip(artists, albums)


def google_music(pairs):
    api = gmusicapi.Mobileclient()
    api.login(USER, PASS, gmusicapi.Mobileclient.FROM_MAC_ADDRESS)
    playlists = api.get_all_playlists()
    playlist_id = [playlist['id'] for playlist in playlists
        if playlist['id'] == '86be30ae-2648-4ba6-8f83-f914ccdd8434'][0]

    for pair in pairs:
        query = ' '.join(pair)
        results = api.search_all_access(query)
        track_ids = [song['track']['storeId'] for song in results['song_hits']]
        if track_ids:
            api.add_songs_to_playlist(playlist_id, track_ids)

if __name__ == '__main__':
    main()
