# -*- coding: utf-8 -*-
import pprint

from musicplatform import MusicPlatform, SpotifyPlaylist, Track
from config import Config


def main():
    c = Config()
    sp = SpotifyPlaylist(username=c.spotify_username,
                         client_id=c.spotify_client_id,
                         secret=c.spotify_secret)
    # sp.get_playlist('https://open.spotify.com/playlist/4Yg2e0n6ZSJlABfBJLWVyA?si=SneZhsQ_R5-djkmrkdlWXg')
    # playlist = sp.create_playlist('Jeffar is a pirate', 'We should all live a pirate\'s life')
    
    auto = [Track('Playlist', artist='Kid Quill'),
            Track('Created', artist='Portugal. The Man'),
            Track('Automatically', artist='Hit-Boy'),
            Track('Jeff', artist='McCafferty'),
            Track("Isn't It Time", artist='The Babys', album='Broken Heart'),
            Track('You Shook Me All Night Long', artist='AC/DC')]
    wp = [Track('War Paint',
                album='Follow Your Bliss: The Best of Senses Fail'),
          Track('I Am the Arsonist - Live', artist='Silverstein')]
    
    
    #tracks = sp.get_playlist_tracks('https://open.spotify.com/playlist/1fUiRhbMvGf0AR9m68gEan?si=rtwTq76cQgqU0YrrFHT1aA')
    #playlist = sp.create_playlist('Panda II', description='suhhh')
    #for track in tracks:
    #    track.uri = sp.get_track_uri(track.name, artist_name=track.artist,
    #                                 album=track.album)
    #sp.add_songs_to_playlist(playlist['uri'], tracks)
    pprint.pprint(sp.get_playlist('https://open.spotify.com/playlist/1fUiRhbMvGf0AR9m68gEan?si=rtwTq76cQgqU0YrrFHT1aA').data)

if __name__ == '__main__':
    main()