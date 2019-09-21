# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 15:19:36 2019

@author: Taur1ne
"""
import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import pprint


class Track(object):
    def __init__(self, name, uri='', album='', artist=''):
        self.name = name
        self.uri = uri
        self.album = album
        self.artist = artist
    
    
    def __str__(self):
        return ('[name: {}, uri: {}, album: {}, artist: {}]\n'
                .format(self.name, self.uri, self.album, self.artist))

    def __repr__(self):
        return self.__str__()


class MusicPlatform(object):
    def __init__(self, client_id: str = '', secret: str = '',
                 username: str = '', password: str = '',
                 platform_name: str ='') -> None:
        self.client_id = client_id
        self.secret = secret
        self.username = username
        self.password = password
        self.platform_name = platform_name
        self.conn = None


    def get_playlist(self, url: str):
        pass

    def create_playlist(self, playlist_name: str, tracks: dict,
                        description: str = '') -> None:
        pass


class SpotifyPlaylist(MusicPlatform):
    def __init__(self, client_id='', secret='', username='', password='',
                 platform_name='Spotify'):
        super(SpotifyPlaylist, self).__init__(client_id=client_id,
             secret=secret, username=username, password=password,
             platform_name=platform_name)
        # ccm = SpotifyClientCredentials()
        # self.conn = spotipy.Spotify(client_credentials_manager=ccm)
        token = util.prompt_for_user_token(self.username,
                                           scope='playlist-modify-public',
                                           client_id=self.client_id,
                                           client_secret=self.secret,
                                           redirect_uri='http://localhost/callback')
        self.conn = spotipy.Spotify(auth=token)
        
    def get_playlist_tracks(self, url: str) -> list:
        spotify_id = self._get_id(url)
        result = self.conn._get(url=('https://api.spotify.com/v1/playlists/{}')
        .format(spotify_id))
        tracks = []
        for track in result['tracks']['items']:
            t = track['track']
            tracks.append(Track(t['name'],
                          artist=t['artists'][0]['name'],
                          album=t['album']['name']))
        return tracks

    def _get_id(self, url: str):
        l_url = url.lower()
        if 'playlist' in l_url:
            return url.split('/')[-1]
        else:
            raise ValueError('URL is not a playlist')
    
    def create_playlist(self, playlist_name: str, description: str = ''
                        ) -> dict:
        playlist = self.conn.user_playlist_create(self.username, playlist_name,
                                                  public=True,
                                                  description=description)
        return playlist

    def add_songs_to_playlist(self, playlist_id: str, tracks: list):
        track_ids = [track.uri for track in tracks if track.uri != '']
        self.conn.user_playlist_add_tracks(self.username, playlist_id,
                                           track_ids)
    
    def get_track_uri(self, name: str, artist_name: str = '', album: str = ''
                     ) -> str:
        results = self.conn.search(q='track:{}'.format(name), type='track',
                                   limit=20)
        if name == "Isn't It Time":
            pprint.pprint(results)
        for track in results['tracks']['items']:
            track_album = track['album']
            uri = track['uri']
            for artist in track['artists']:
                if artist['name'] == artist_name:
                    return uri
            if track_album['name'] == album:
                return uri
        return ''


class ApplePlaylist(MusicPlatform):
    pass


class GooglePlaylist(MusicPlatform):
    pass


class YoutubePlaylist(MusicPlatform):
    pass