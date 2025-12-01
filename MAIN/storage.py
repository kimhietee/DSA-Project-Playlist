"""
Music Playlist System - Data Storage Manager
Handles JSON persistence for tracks, playlists, and queues
"""
import json
import os
from typing import List, Dict, Optional
from models import Track, Playlist, Queue, Album


class StorageManager:
    """Manages persistent data storage in JSON format"""
    
    def __init__(self, data_dir: str = "./data"):
        self.data_dir = data_dir
        self.tracks_file = os.path.join(data_dir, "tracks.json")
        self.playlists_file = os.path.join(data_dir, "playlists.json")
        self.queue_file = os.path.join(data_dir, "queue.json")
        self.albums_file = os.path.join(data_dir, "albums.json")
        
        self._ensure_data_dir()
    
    def _ensure_data_dir(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def _read_json(self, filepath: str) -> dict:
        """Read JSON file safely"""
        if not os.path.exists(filepath):
            return {}
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    
    def _write_json(self, filepath: str, data: dict):
        """Write data to JSON file"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Error writing to {filepath}: {e}")
    
    # ============== TRACKS MANAGEMENT ==============
    
    def save_track(self, track: Track):
        """Save a single track"""
        data = self._read_json(self.tracks_file)
        
        if 'tracks' not in data:
            data['tracks'] = []
        
        # Check if track already exists
        track_dict = track.to_dict()
        for existing in data['tracks']:
            if (existing['title'] == track.title and 
                existing['artist'] == track.artist and 
                existing['album'] == track.album):
                return False  # Track already exists
        
        data['tracks'].append(track_dict)
        self._write_json(self.tracks_file, data)
        return True
    
    def load_all_tracks(self) -> List[Track]:
        """Load all tracks from storage"""
        data = self._read_json(self.tracks_file)
        
        if 'tracks' not in data:
            return []
        
        tracks = [Track.from_dict(t) for t in data['tracks']]
        # Sort by title, artist, album, duration, then date_added as final tie-breaker
        tracks.sort(key=lambda t: (
            (t.title or '').lower(),
            (t.artist or '').lower(),
            (t.album or '').lower(),
            t.duration_to_seconds(),
            getattr(t, 'date_added', '') or ''
        ))
        return tracks
    
    def delete_track(self, title: str, artist: str, album: str) -> bool:
        """Delete a track from storage"""
        data = self._read_json(self.tracks_file)
        
        if 'tracks' not in data:
            return False
        
        original_len = len(data['tracks'])
        data['tracks'] = [t for t in data['tracks'] 
                         if not (t['title'] == title and t['artist'] == artist and t['album'] == album)]
        
        if len(data['tracks']) < original_len:
            self._write_json(self.tracks_file, data)
            return True
        return False
    
    def search_tracks(self, query: str) -> List[Track]:
        """Search tracks by title"""
        all_tracks = self.load_all_tracks()
        query_lower = query.lower()
        return [t for t in all_tracks if query_lower in t.title.lower()]
    
    # ============== PLAYLISTS MANAGEMENT ==============
    
    def save_playlist(self, playlist: Playlist) -> bool:
        """Save a playlist"""
        data = self._read_json(self.playlists_file)
        
        if 'playlists' not in data:
            data['playlists'] = []
        
        # Check if playlist name already exists
        for existing in data['playlists']:
            if existing['name'] == playlist.name:
                return False  # Playlist already exists
        
        data['playlists'].append(playlist.to_dict())
        self._write_json(self.playlists_file, data)
        return True
    
    def load_all_playlists(self) -> List[Playlist]:
        """Load all playlists from storage"""
        data = self._read_json(self.playlists_file)
        
        if 'playlists' not in data:
            return []
        
        playlists = [Playlist.from_dict(p) for p in data['playlists']]
        return playlists
    
    def update_playlist(self, playlist: Playlist) -> bool:
        """Update an existing playlist"""
        data = self._read_json(self.playlists_file)
        
        if 'playlists' not in data:
            return False
        
        for i, p in enumerate(data['playlists']):
            if p['name'] == playlist.name:
                data['playlists'][i] = playlist.to_dict()
                self._write_json(self.playlists_file, data)
                return True
        
        return False
    
    def delete_playlist(self, playlist_name: str) -> bool:
        """Delete a playlist"""
        data = self._read_json(self.playlists_file)
        
        if 'playlists' not in data:
            return False
        
        original_len = len(data['playlists'])
        data['playlists'] = [p for p in data['playlists'] if p['name'] != playlist_name]
        
        if len(data['playlists']) < original_len:
            self._write_json(self.playlists_file, data)
            return True
        return False
    
    def get_playlist_by_name(self, name: str) -> Optional[Playlist]:
        """Get a specific playlist by name"""
        playlists = self.load_all_playlists()
        for p in playlists:
            if p.name == name:
                return p
        return None
    
    # ============== QUEUE MANAGEMENT ==============
    
    def save_queue(self, queue: Queue):
        """Save queue to storage"""
        data = {'queue': queue.to_dict()}
        self._write_json(self.queue_file, data)
    
    def load_queue(self) -> Optional[Queue]:
        """Load queue from storage"""
        data = self._read_json(self.queue_file)
        
        if 'queue' not in data or not data['queue'].get('tracks'):
            return None
        
        return Queue.from_dict(data['queue'])
    
    def clear_queue(self):
        """Clear saved queue"""
        self._write_json(self.queue_file, {})
    
    # ============== ALBUMS MANAGEMENT ==============
    
    def save_album(self, album: Album) -> bool:
        """Save or update an album"""
        data = self._read_json(self.albums_file)
        
        if 'albums' not in data:
            data['albums'] = []
        
        # Check if album exists
        for i, existing in enumerate(data['albums']):
            if existing['album_name'] == album.album_name:
                data['albums'][i] = album.to_dict()
                self._write_json(self.albums_file, data)
                return True
        
        data['albums'].append(album.to_dict())
        self._write_json(self.albums_file, data)
        return False  # New album
    
    def load_all_albums(self) -> List[Album]:
        """Load all albums"""
        data = self._read_json(self.albums_file)
        
        if 'albums' not in data:
            return []
        
        return [Album.from_dict(a) for a in data['albums']]
    
    def get_album_by_name(self, name: str) -> Optional[Album]:
        """Get album by name"""
        albums = self.load_all_albums()
        for album in albums:
            if album.album_name == name:
                return album
        return None
    
    def get_or_create_album(self, album_name: str) -> Album:
        """Get existing album or create new one"""
        album = self.get_album_by_name(album_name)
        if album:
            return album
        return Album(album_name)
