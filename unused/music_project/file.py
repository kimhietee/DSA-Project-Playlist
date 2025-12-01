import json
from pprint import pprint
import os

from default_data import DEFAULT_DATA

class File:
    '''Main code for file store.'''
    def __init__(self:object, filename:str):
        self.default_data = DEFAULT_DATA # default data
        self.filename = filename # supported file

    def read_data(self:object, return_to_default:bool=False) -> dict:
        '''READ - Reads current json file data if exists, if not, use default data.

        return_to_default - set to True to return to the default data provided.
        '''
        if os.path.exists(self.filename) and not return_to_default:
            with open(self.filename, 'r') as file:
                try:
                    current_data = json.load(file)
                except json.JSONDecodeError as err:
                    print('Error', err)
                    current_data = self.default_data
        else:
            current_data = self.default_data
        return current_data

    def write_data(self:object, new_data:dict=None):
        '''SAVE - Overwrite our current data.

        new_data - overwrite data using the new_data. 
        If not provided, uses the default data provided instead.
        '''
        if new_data is None:
            new_data = self.default_data
        with open(self.filename, 'w') as file:
            json.dump(new_data, file, indent=4)
        file.close()


class MusicLibrary:
    '''Music Library Management System'''
    def __init__(self:object, file_manager:File):
        self.file_manager = file_manager
        self.library = file_manager.read_data()
    
    def add_track(self:object, artist:str, track_name:str, album:str, duration:str, genre:str):
        '''Add a new track to the library'''
        if artist not in self.library:
            self.library[artist] = {}
        
        self.library[artist][track_name] = {
            'Album': album,
            'Duration': duration,
            'Genre': genre
        }
        self.file_manager.write_data(self.library)
        print(f"Added '{track_name}' by {artist}")
    
    def get_all_tracks(self:object) -> dict:
        '''Get all tracks from the library'''
        return self.library
    
    def search_tracks(self:object, keyword:str) -> dict:
        '''Search for tracks by artist, track name, or genre'''
        results = {}
        keyword_lower = keyword.lower()
        
        for artist, tracks in self.library.items():
            if keyword_lower in artist.lower():
                results[artist] = tracks
            else:
                matching_tracks = {}
                for track_name, details in tracks.items():
                    if (keyword_lower in track_name.lower() or 
                        keyword_lower in details.get('Genre', '').lower() or
                        keyword_lower in details.get('Album', '').lower()):
                        matching_tracks[track_name] = details
                if matching_tracks:
                    results[artist] = matching_tracks
        
        return results
    
    def display_library(self:object):
        '''Display all tracks in the library'''
        pprint(self.library)


class Playlist:
    '''Playlist Management'''
    def __init__(self:object, name:str):
        self.name = name
        self.tracks = []  # List of (artist, track_name) tuples
    
    def add_track(self:object, artist:str, track_name:str):
        '''Add track to playlist'''
        self.tracks.append({'artist': artist, 'track': track_name})
        print(f"Added '{track_name}' by {artist} to playlist '{self.name}'")
    
    def remove_track(self:object, index:int):
        '''Remove track from playlist by index'''
        if 0 <= index < len(self.tracks):
            removed = self.tracks.pop(index)
            print(f"Removed '{removed['track']}' from playlist '{self.name}'")
    
    def get_tracks(self:object) -> list:
        '''Get all tracks in the playlist'''
        return self.tracks
    
    def clear(self:object):
        '''Clear all tracks from playlist'''
        self.tracks = []
        print(f"Cleared playlist '{self.name}'")
    
    def to_dict(self:object) -> dict:
        '''Convert playlist to dictionary for saving'''
        return {'name': self.name, 'tracks': self.tracks}


class PlaylistManager:
    '''Manage multiple playlists'''
    def __init__(self:object, file_manager:File):
        self.file_manager = file_manager
        self.playlists_file = 'playlists.json'
        self.playlists = self._load_playlists()
    
    def _load_playlists(self:object) -> dict:
        '''Load playlists from file'''
        if os.path.exists(self.playlists_file):
            with open(self.playlists_file, 'r') as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return {}
        return {}
    
    def create_playlist(self:object, name:str) -> Playlist:
        '''Create a new playlist'''
        playlist = Playlist(name)
        self.playlists[name] = playlist.to_dict()
        self._save_playlists()
        print(f"Created playlist '{name}'")
        return playlist
    
    def add_to_playlist(self:object, playlist_name:str, artist:str, track_name:str):
        '''Add track to an existing playlist'''
        if playlist_name in self.playlists:
            if 'tracks' not in self.playlists[playlist_name]:
                self.playlists[playlist_name]['tracks'] = []
            self.playlists[playlist_name]['tracks'].append({'artist': artist, 'track': track_name})
            self._save_playlists()
            print(f"Added '{track_name}' by {artist} to playlist '{playlist_name}'")
    
    def get_playlist(self:object, name:str) -> list:
        '''Get tracks from a playlist'''
        if name in self.playlists:
            return self.playlists[name].get('tracks', [])
        return []
    
    def _save_playlists(self:object):
        '''Save all playlists to file'''
        with open(self.playlists_file, 'w') as file:
            json.dump(self.playlists, file, indent=4)


class MusicQueue:
    '''Music Queue Management'''
    def __init__(self:object, file_manager:File):
        self.file_manager = file_manager
        self.queue_file = 'queue.json'
        self.queue = self._load_queue()
    
    def _load_queue(self:object) -> list:
        '''Load queue from file'''
        if os.path.exists(self.queue_file):
            with open(self.queue_file, 'r') as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return []
        return []
    
    def add_from_library(self:object, library:MusicLibrary, artist:str, track_name:str):
        '''Add track from library to queue'''
        if artist in library.library and track_name in library.library[artist]:
            self.queue.append({'artist': artist, 'track': track_name})
            self._save_queue()
            print(f"Added '{track_name}' by {artist} to queue")
        else:
            print(f"Track not found: {track_name} by {artist}")
    
    def add_from_playlist(self:object, playlist_manager:PlaylistManager, playlist_name:str):
        '''Add all tracks from a playlist to queue'''
        tracks = playlist_manager.get_playlist(playlist_name)
        self.queue.extend(tracks)
        self._save_queue()
        print(f"Added all tracks from playlist '{playlist_name}' to queue")
    
    def get_queue(self:object) -> list:
        '''Get current queue'''
        return self.queue
    
    def skip(self:object) -> dict:
        '''Skip to next track'''
        if self.queue:
            current = self.queue.pop(0)
            self._save_queue()
            return current
        return None
    
    def clear(self:object):
        '''Clear the queue'''
        self.queue = []
        if os.path.exists(self.queue_file):
            os.remove(self.queue_file)
        print("Queue cleared")
    
    def _save_queue(self:object):
        '''Save queue to file'''
        if self.queue:
            with open(self.queue_file, 'w') as file:
                json.dump(self.queue, file, indent=4)
        else:
            if os.path.exists(self.queue_file):
                os.remove(self.queue_file)


# Example usage
file_manager = File('data.json')
library = MusicLibrary(file_manager)
playlist_manager = PlaylistManager(file_manager)
music_queue = MusicQueue(file_manager)
