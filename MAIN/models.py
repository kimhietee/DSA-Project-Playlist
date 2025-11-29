"""
Music Playlist System - Data Structure Models
"""
from datetime import datetime
from typing import List, Optional


class Track:
    """Represents a single music track"""
    
    def __init__(self, title: str, artist: str, album: str, duration: str, additional_artists: str = ""):
        self.title = title
        self.artist = artist
        self.album = album
        self.duration = duration  # Format: "mm:ss"
        self.additional_artists = additional_artists
        self.date_added = datetime.now().isoformat()
    
    def duration_to_seconds(self) -> int:
        """Convert duration string (mm:ss) to seconds"""
        parts = self.duration.split(':')
        return int(parts[0]) * 60 + int(parts[1])
    
    @staticmethod
    def seconds_to_duration(seconds: int) -> str:
        """Convert seconds to duration string (mm:ss)"""
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"
    
    def get_display_name(self) -> str:
        """Get formatted display name with artists"""
        if self.additional_artists:
            return f"{self.title} – {self.artist}, {self.additional_artists} ({self.duration})"
        return f"{self.title} – {self.artist} ({self.duration})"
    
    def to_dict(self) -> dict:
        """Convert track to dictionary for JSON storage"""
        return {
            'title': self.title,
            'artist': self.artist,
            'album': self.album,
            'duration': self.duration,
            'additional_artists': self.additional_artists,
            'date_added': self.date_added
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Track':
        """Create Track from dictionary"""
        track = Track(
            data['title'],
            data['artist'],
            data['album'],
            data['duration'],
            data.get('additional_artists', '')
        )
        if 'date_added' in data:
            track.date_added = data['date_added']
        return track
    
    def __repr__(self):
        return f"Track({self.title}, {self.artist}, {self.duration})"


class Album:
    """Represents an album containing tracks"""
    
    def __init__(self, album_name: str):
        self.album_name = album_name
        self.tracks = []
        self.date_created = datetime.now().isoformat()
    
    def add_track(self, track: Track):
        """Add track to album"""
        if not self._track_exists(track):
            self.tracks.append(track)
    
    def _track_exists(self, track: Track) -> bool:
        """Check if track already exists in album"""
        for t in self.tracks:
            if t.title == track.title and t.artist == track.artist:
                return True
        return False
    
    def get_total_duration(self) -> int:
        """Get total duration in seconds"""
        return sum(track.duration_to_seconds() for track in self.tracks)
    
    def to_dict(self) -> dict:
        return {
            'album_name': self.album_name,
            'tracks': [t.to_dict() for t in self.tracks],
            'date_created': self.date_created
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Album':
        album = Album(data['album_name'])
        album.date_created = data['date_created']
        album.tracks = [Track.from_dict(t) for t in data['tracks']]
        return album


class Playlist:
    """Represents a playlist containing tracks"""
    
    def __init__(self, name: str):
        self.name = name
        self.tracks = []
        self.date_created = datetime.now().isoformat()
    
    def add_track(self, track: Track) -> bool:
        """Add track to playlist. Returns True if added, False if already exists"""
        if not self._track_exists(track):
            self.tracks.append(track)
            return True
        return False
    
    def remove_track(self, track_index: int) -> bool:
        """Remove track from playlist by index"""
        if 0 <= track_index < len(self.tracks):
            del self.tracks[track_index]
            return True
        return False
    
    def _track_exists(self, track: Track) -> bool:
        """Check if track already exists in playlist"""
        for t in self.tracks:
            if (t.title == track.title and 
                t.artist == track.artist and 
                t.album == track.album):
                return True
        return False
    
    def get_total_duration(self) -> int:
        """Get total duration in seconds"""
        return sum(track.duration_to_seconds() for track in self.tracks)
    
    def get_total_duration_formatted(self) -> str:
        """Get formatted total duration"""
        total_seconds = self.get_total_duration()
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        if hours > 0:
            return f"{hours} hr {minutes} min {seconds} sec"
        elif minutes > 0:
            return f"{minutes} min {seconds} sec"
        return f"{seconds} sec"
    
    def sort_tracks(self):
        """Sort tracks by title, then artist, album, duration"""
        self.tracks.sort(key=lambda t: (t.title, t.artist, t.album, t.duration_to_seconds()))
    
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'tracks': [t.to_dict() for t in self.tracks],
            'date_created': self.date_created
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Playlist':
        playlist = Playlist(data['name'])
        playlist.date_created = data['date_created']
        playlist.tracks = [Track.from_dict(t) for t in data['tracks']]
        return playlist
    
    def __repr__(self):
        return f"Playlist({self.name}, {len(self.tracks)} tracks)"


class Node:
    """Node for circular linked list queue"""
    
    def __init__(self, track: Track):
        self.track = track
        self.next = None
        self.prev = None


class Queue:
    """Represents a music queue with circular linked list structure"""
    
    def __init__(self, tracks: List[Track] = None):
        self.original_order = []
        self.head = None
        self.current = None
        self.is_shuffled = False
        self.is_repeat = False
        self.total_tracks = 0
        
        if tracks:
            self.original_order = [t for t in tracks]
            self._build_queue(tracks)
    
    def _build_queue(self, tracks: List[Track]):
        """Build circular linked list from tracks"""
        if not tracks:
            return
        
        self.total_tracks = len(tracks)
        self.head = Node(tracks[0])
        current_node = self.head
        
        for track in tracks[1:]:
            new_node = Node(track)
            current_node.next = new_node
            new_node.prev = current_node
            current_node = new_node
        
        # Create circular structure
        current_node.next = self.head
        self.head.prev = current_node
        self.current = self.head
    
    def add_track(self, track: Track):
        """Add track to end of queue"""
        if self.total_tracks == 0:
            self.head = Node(track)
            self.head.next = self.head
            self.head.prev = self.head
            self.current = self.head
        else:
            new_node = Node(track)
            last_node = self.head.prev
            last_node.next = new_node
            new_node.prev = last_node
            new_node.next = self.head
            self.head.prev = new_node
        
        self.total_tracks += 1
        self.original_order.append(track)
    
    def add_playlist(self, playlist: Playlist):
        """Add all tracks from playlist to queue"""
        for track in playlist.tracks:
            self.add_track(track)
    
    def next_track(self) -> Optional[Track]:
        """Move to next track (O(1))"""
        if self.total_tracks == 0:
            return None
        
        if self.current:
            self.current = self.current.next
            return self.current.track
        return None
    
    def prev_track(self) -> Optional[Track]:
        """Move to previous track (O(1))"""
        if self.total_tracks == 0:
            return None
        
        if self.current:
            self.current = self.current.prev
            return self.current.track
        return None
    
    def get_current_track(self) -> Optional[Track]:
        """Get current track (O(1))"""
        if self.current:
            return self.current.track
        return None
    
    def shuffle(self):
        """Shuffle queue while maintaining current track"""
        if self.total_tracks <= 1 or self.is_shuffled:
            return
        
        current_track = self.get_current_track()
        
        # Create shuffled list without current track
        shuffled = self.original_order.copy()
        shuffled.remove(current_track)
        
        import random
        random.shuffle(shuffled)
        
        # Rebuild queue with current track at front
        shuffled.insert(0, current_track)
        self._build_queue(shuffled)
        self.is_shuffled = True
    
    def unshuffle(self):
        """Return to original order while maintaining current track"""
        if not self.is_shuffled or self.total_tracks <= 1:
            return
        
        current_track = self.get_current_track()
        self._build_queue(self.original_order)
        
        # Move to current track
        temp = self.current
        for _ in range(self.total_tracks):
            if self.current.track == current_track:
                break
            self.current = self.current.next
        
        self.is_shuffled = False
    
    def toggle_repeat(self):
        """Toggle repeat mode"""
        self.is_repeat = not self.is_repeat
    
    def toggle_shuffle(self):
        """Toggle shuffle mode"""
        if self.is_shuffled:
            self.unshuffle()
        else:
            self.shuffle()
    
    def clear(self):
        """Clear the queue"""
        self.head = None
        self.current = None
        self.is_shuffled = False
        self.is_repeat = False
        self.total_tracks = 0
        self.original_order = []
    
    def get_total_duration(self) -> int:
        """Get total duration in seconds"""
        total = 0
        if self.total_tracks == 0:
            return 0
        
        node = self.head
        for _ in range(self.total_tracks):
            total += node.track.duration_to_seconds()
            node = node.next
        return total
    
    def get_total_duration_formatted(self) -> str:
        """Get formatted total duration"""
        total_seconds = self.get_total_duration()
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        if hours > 0:
            return f"{hours} hr {minutes} min"
        elif minutes > 0:
            return f"{minutes} min"
        return f"{seconds} sec"
    
    def get_tracks_page(self, page: int = 1, page_size: int = 10) -> tuple:
        """
        Get tracks for a specific page
        Returns: (tracks_list, current_page, total_pages)
        """
        if self.total_tracks == 0:
            return [], 1, 0
        
        total_pages = (self.total_tracks + page_size - 1) // page_size
        page = max(1, min(page, total_pages))
        
        start_idx = (page - 1) * page_size
        tracks = []
        
        node = self.head
        for i in range(self.total_tracks):
            if i >= start_idx and i < start_idx + page_size:
                tracks.append(node.track)
            node = node.next
        
        return tracks, page, total_pages
    
    def to_dict(self) -> dict:
        """Convert queue to dictionary for storage"""
        tracks = []
        if self.head:
            node = self.head
            for _ in range(self.total_tracks):
                tracks.append(node.track.to_dict())
                node = node.next
        
        current_track = self.get_current_track()
        return {
            'tracks': tracks,
            'original_order': [t.to_dict() for t in self.original_order],
            'current_track': current_track.to_dict() if current_track else None,
            'is_shuffled': self.is_shuffled,
            'is_repeat': self.is_repeat
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Queue':
        """Create Queue from dictionary"""
        queue = Queue()
        
        if data.get('tracks'):
            tracks = [Track.from_dict(t) for t in data['tracks']]
            queue._build_queue(tracks)
        
        queue.original_order = [Track.from_dict(t) for t in data.get('original_order', [])]
        queue.is_shuffled = data.get('is_shuffled', False)
        queue.is_repeat = data.get('is_repeat', False)
        
        # Restore current track
        if data.get('current_track') and queue.head:
            current_data = data['current_track']
            node = queue.head
            for _ in range(queue.total_tracks):
                if (node.track.title == current_data['title'] and 
                    node.track.artist == current_data['artist']):
                    queue.current = node
                    break
                node = node.next
        
        return queue
