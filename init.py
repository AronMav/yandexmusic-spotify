import spotipy as oauth2
import spotipy
import configparser
from yandex_music.client import Client


def connect_ya(auth_file):
    config = configparser.ConfigParser()
    config.read(auth_file)
    token = config.get('YANDEX', 'TOKEN')
    return Client(token)


def connect_sp(auth_file):
    config = configparser.ConfigParser()
    config.read(auth_file)
    username = config.get('SPOTIFY', 'USERNAME')
    scope = config.get('SPOTIFY', 'SCOPE')
    client_id = config.get('SPOTIFY', 'CLIENT_ID')
    client_secret = config.get('SPOTIFY', 'CLIENT_SECRET')
    redirect_uri = config.get('SPOTIFY', 'REDIRECT_URI')
    cache_path = config.get('SPOTIFY', 'CACHE')

    token = oauth2.prompt_for_user_token(
        username=username,
        scope=scope,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        cache_path=cache_path,
    )
    return spotipy.Spotify(auth=token)


client_ya = connect_ya('AuthToken.cfg')
client_sp = connect_sp('AuthToken.cfg')

list_search_track = []

tracks = client_ya.users_likes_tracks()
for track in tracks:
    artists = ''
    for artist in track.track.artists:
        if artists == '':
            artists = artist['name']
        else:
            artists = artists + ', ' + artist['name']
    results = client_sp.search(track.track.title + ' ' + artists)
    number = 0
    for result in results['tracks']['items']:
        client_sp.current_user_saved_tracks_add(tracks=[result['uri']])
        artists = ''
        for art in result['artists']:
            if artists == '':
                artists = art['name']
            else:
                artists = artists + ', ' + art['name']
        list_search_track.append(artists + ' - ' + result['name'])
        break
for track in list_search_track:
    print(track)
