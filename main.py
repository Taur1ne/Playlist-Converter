# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 10:23:26 2019

@author: cwong
"""
import praw
from config import Config
from musicplatform import YoutubePlaylist, SpotifyPlaylist
from html.parser import HTMLParser
from urllib.parse import urlparse


def main():
    c = Config()
    reddit = get_reddit(c)
    # for item in reddit.inbox.all(limit=None):
    #    print(repr(item))
    platforms = {
            'Youtube': YoutubePlaylist(
                    client_id=c.google_playlistconverter_client_id,
                    secret=c.google_playlistconverter_secret,
                    scopes=['https://www.googleapis.com/auth/youtube.force-ssl',
                            'https://www.googleapis.com/auth/youtube.readonly']
                    ),
            # 'Google': [],
            'Spotify': SpotifyPlaylist(username=c.spotify_username,
                                       client_id=c.spotify_client_id,
                                       secret=c.spotify_secret)
    }
    
    for mention in reddit.inbox.mentions(limit=10):
        for url in get_urls(mention.body_html):
            src_p = get_platform(url)
            dst_platforms = [key for key in platforms.keys() if key != src_p]
            try:
                src_platform = platforms[src_p]
            except KeyError:
                print('Platform is unsupported: {}'.format(url))
                continue
            
            # Obtain playlist information from source platform
            src_playlist = src_platform.get_playlist(url)
            src_playlist_name = src_playlist.name
            src_playlist_desc = src_playlist.description
            
            # Retrieve track information from the source playlist
            tracks = src_platform.get_playlist_tracks(url)
            
            # Loop through the destination platforms and create playlists
            for dst_p in dst_platforms:
                dst_platform = platforms[dst_p]
                # Create the playlist on the destination platform
                dst_playlist = dst_platform.create_playlist(src_playlist_name,\
                                                description=src_playlist_desc)
                dst_playlist_url = dst_playlist.uri
                
                # Set the track unique identifiers for that dest. platform
                for track in tracks:
                    track.uri = dst_platform.get_track_uri(track=track)
                
                dst_platform.add_songs_to_playlist(dst_playlist.id, tracks)
                print('{} playlist has been created here: {}'.format(
                        dst_platform.platform_name, dst_playlist_url))
        # Need to mark the mention as read
        mention.mark_read()


def get_reddit(config):
    return praw.Reddit(
            user_agent='Playlist Converter (by /u/PlaylistConverter)',
            client_id=config.reddit_client_id,
            client_secret=config.reddit_secret,
            username=config.reddit_username,
            password=config.reddit_password)


def get_platform(url: str) -> str:
    url = url.lower()
    try:
        parsed_uri = urlparse(url)
    except ValueError:
        return 'Unsupported'
    netloc = parsed_uri.netloc
    if 'spotify.com' in netloc:
        return 'Spotify'
    elif 'youtube.com' in netloc:
        return 'Youtube'
    elif 'google.com' in netloc:
        return 'Google'
    elif 'apple.com' in netloc:
        return 'Apple'
    else:
        return 'Unsupported'


def get_urls(html: str) -> list:
    parser = MyHTMLParser()
    parser.feed(html)
    return parser.URLS


class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.URLS = []
    
    def clean(self):
        self.URLS = []
        
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    self.URLS.append(attr[1])
    
    def handle_endtag(self, tag):
        pass
    
    def handle_data(self, data):
        pass

if __name__ == '__main__':
    main()