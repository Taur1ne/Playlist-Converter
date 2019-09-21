# -*- coding: utf-8 -*-
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import Config

def main():
    c = Config()
    scope = 'playlist-read-collaborative'
    
    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    url = 'https://open.spotify.com/playlist/25ZSrTYT8Z8pDCJH7BjOs5'
    spotify_id = get_id(url)
    # results = sp.search(q='playlist:{}'.format(spotify_id), type='playlist')
    result = sp._get(url='https://api.spotify.com/v1/playlists/{}'.format(spotify_id))
    for track in result['tracks']['items']:
        print(track['track']['name'])
    
        
    


def get_id(url):
    l_url = url.lower()
    
    if 'playlist' in l_url:
        return url.split('/')[-1]
    else:
        raise ValueError('URL is not a playlist')


if __name__ == '__main__':
    main()