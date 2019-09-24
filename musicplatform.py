# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 15:19:36 2019

@author: Taur1ne
"""
import os
import pprint

import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors


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


class Playlist(object):
    def __init__(self, name: str, description: str = '', uri: str = '',
                 id: str = '', platform: str = '', data: dict = {}):
        self.name = name
        self.description = description
        self.uri = uri
        self.id = id
        self.platform = platform
        self.data = data


class MusicPlatform(object):
    def __init__(self, client_id: str = '', secret: str = '',
                 username: str = '', password: str = '',
                 platform_name: str ='', scopes: list = []) -> None:
        self.client_id = client_id
        self.secret = secret
        self.username = username
        self.password = password
        self.platform_name = platform_name
        self.scopes = scopes
        self.conn = None
        

    def get_playlist_tracks(self, url: str) -> list:
        pass

    def create_playlist(self, playlist_name: str, description: str = ''
                        ) -> None:
        pass
    
    def get_playlist(self, url) -> dict:
        pass
    
    def get_track_uri(name: str = '', artist_name: str = '', album: str = '',
                      track: Track = None) -> str:
        pass


class SpotifyPlaylist(MusicPlatform):
    def __init__(self, client_id='', secret='', username='', password='',
                 platform_name='Spotify', scopes: list = []):
        super(SpotifyPlaylist, self).__init__(client_id=client_id,
             secret=secret, username=username, password=password,
             platform_name=platform_name, scopes=scopes)
        # ccm = SpotifyClientCredentials()
        # self.conn = spotipy.Spotify(client_credentials_manager=ccm)
        token = util.prompt_for_user_token(self.username,
                                           scope='playlist-modify-public',
                                           client_id=self.client_id,
                                           client_secret=self.secret,
                                           redirect_uri='http://localhost/callback')
        self.conn = spotipy.Spotify(auth=token)
        
    def get_playlist_tracks(self, url: str) -> list:
        playlist = self.get_playlist(url)
        tracks = []
        for track in playlist.data['tracks']['items']:
            t = track['track']
            tracks.append(Track(t['name'],
                          artist=t['artists'][0]['name'],
                          album=t['album']['name']))
        return tracks

    def create_playlist(self, playlist_name: str, description: str = ''
                        ) -> dict:
        playlist = self.conn.user_playlist_create(self.username, playlist_name,
                                                  public=True,
                                                  description=description)
        return self._fill_playlist(playlist)
    
    def get_playlist(self, url: str) -> Playlist:
        spotify_id = self._get_id(url)
        result = self.conn._get(url=('https://api.spotify.com/v1/playlists/{}')
        .format(spotify_id))
        return self._fill_playlist(result)
    
    def _fill_playlist(self, p: dict) -> Playlist:
        name = p['name']
        desc = p['description']
        ext_url = p['external_urls']['spotify']
        url_id = p['id']
        return Playlist(name, description=desc, uri=ext_url, id=url_id,
                        platform=self.platform_name, data=p)

    def _get_id(self, url: str):
        l_url = url.lower()
        if 'playlist' in l_url:
            return url.split('/')[-1]
        else:
            raise ValueError('URL is not a playlist')

    def add_songs_to_playlist(self, playlist_id: str, tracks: list):
        track_ids = [track.uri for track in tracks if track.uri != '']
        pprint.pprint(track_ids)
        if len(track_ids) > 0:
            return self.conn.user_playlist_add_tracks(self.username,
                                                      playlist_id,
                                                      track_ids)
        else:
            return None
    
    def get_track_uri(self, name: str = '', artist_name: str = '',
                      album: str = '', track: Track = None) -> str:
        if track is not None:
            name = track.name
            artist_name = track.artist
            album = track.album

        results = self.conn.search(q='track:{}'.format(name), type='track',
                                   limit=20)
        
        for t in results['tracks']['items']:
            track_album = t['album']
            uri = t['uri']
            for artist in t['artists']:
                if artist['name'] == artist_name and artist_name != '':
                    return uri
            if track_album['name'] == album and album != '':
                return uri
        return ''


class ApplePlaylist(MusicPlatform):
    pass


class GoogleMusicPlaylist(MusicPlatform):
    pass


class YoutubePlaylist(MusicPlatform):
    def __init__(self, client_id='', secret='', username='', password='',
                 platform_name='Youtube', scopes: list = []):
        super(YoutubePlaylist, self).__init__(client_id=client_id,
             secret=secret, username=username, password=password,
             platform_name=platform_name, scopes=scopes)
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        # scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
    
        api_service_name = 'youtube'
        api_version = 'v3'
        client_secrets_file = 'google_playlistconverter.json'
    
        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()
        self.conn = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)
        
    def get_playlist_tracks(self, url: str) -> list:        
        url_id = self._get_id(url)
        tracks = []
        request = self.conn.playlistItems().list(
                part='contentDetails, id, snippet, status', playlistId=url_id)
        response = request.execute()
        for track in response['items']:
            title = track['snippet']['title'].split('\n')[0]
            tracks.append(Track(title))
        pprint.pprint(tracks)
        return tracks

    def create_playlist(self, playlist_name, description: str = ''
                        ) -> Playlist:
        # scopes = []
        request = self.conn.playlists().insert(
                part='snippet, status',
                body={
                        'snippet': {
                                'title': playlist_name,
                                'description': description
                                },
                        'status': {
                                'privacyStatus': 'public'
                                }})
        response = request.execute()
        pprint.pprint(response)
        return self._fill_playlist(response)
    
    def get_playlist(self, url: str) -> Playlist:
        url_id = self._get_id(url)
        request = self.conn.playlists().list(
                part='snippet', id=url_id)
        response = request.execute()
        return self._fill_playlist(response['items'][0])

    def _fill_playlist(self, p: dict) -> Playlist:
        snip = p['snippet']
        name = snip['title']
        desc = snip['description']
        url_id = p['id']
        ext_uri = 'https://www.youtube.com/playlist?list={}'.format(url_id)
        
        return Playlist(name, description=desc, uri=ext_uri, id=url_id,
                        platform=self.platform_name, data=p)

    def _get_id(self, url: str) -> str:
        return url.split('list=')[-1]    

    def add_songs_to_playlist(self, playlist_id: str, tracks: list
                              ) -> None:
        for track in tracks:
            request = self.conn.playlistItems().insert(
                    part='snippet',
                    body={
                            'snippet': {
                                    'playlistId': playlist_id,
                                    'resourceId':{
                                            'videoId': track.uri,
                                            'kind': 'youtube#video'
                                            }}})
            request.execute()
    
    def get_track_uri(self, name: str = '', artist_name: str = '',
                      album: str = '', track: Track = None) -> str:
        if track is not None:
            name = track.name
            artist_name = track.artist
            album = track.album
        
        query = '{} {} {}'.format(name, artist_name, album)
        request = self.conn.search().list(
                part='snippet',
                maxResults=1,
                q=query)
        response = request.execute()
        pprint.pprint('query: {}'.format(query))
        pprint.pprint(response)
        return response['items'][0]['id']['videoId']
        
        
        