# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 22:03:10 2019

@author: cwong
"""
from config import Config
from musicplatform import YoutubePlaylist
import pprint

def main():
    c = Config()
    yt = YoutubePlaylist(client_id=c.google_playlistconverter_client_id,
                        secret=c.google_playlistconverter_secret,
                        scopes=['https://www.googleapis.com/auth/youtube.force-ssl',
                                'https://www.googleapis.com/auth/youtube.readonly'])
    # pprint.pprint(yt.create_playlist('testing!!!', description='gains'))
    pprint.pprint(yt.get_playlist_tracks('https://www.youtube.com/playlist?list=PL9FE0DC696121F551'))
    

if __name__ == '__main__':
    main()    