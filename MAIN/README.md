# Music Playlist System

A comprehensive music playlist management system built with Python, featuring a circular linked list-based queue, playlist management, and persistent storage.

## Features

### Core Features
- **Music Library Management**
  - Add tracks with title, artist, album, and duration
  - Search tracks by title
  - Delete tracks
  - View all tracks with pagination
  - Automatic sorting by title, then artist, album, and duration

- **Playlist Management**
  - Create multiple playlists
  - Add tracks to playlists (no duplicates allowed)
  - Search for tracks and add them to playlists
  - View playlist details and duration
  - Delete playlists
  - Pagination support for 10+ playlists

- **Queue & Player**
  - Create queues from library or playlists
  - O(1) next/previous operations using circular linked list
  - Shuffle mode (maintains current track)
  - Repeat mode (all-repeat)
  - Play, skip, and previous controls
  - Pagination for large queues
  - Add tracks to queue dynamically

- **Data Persistence**
  - All data saved in JSON format
  - Automatic saves for tracks, playlists, and queues
  - Resume playback after application restart

### Data Structures
- **Circular Linked List**: Queue implementation for O(1) operations
- **Custom Classes**: Track, Playlist, Queue, Album
- **Sorted Tracks**: Default sorting by title, artist, album, duration

## Project Structure

```
MAIN/
├── main.py                  # Main application entry point
├── models.py                # Data structure classes (Track, Playlist, Queue, Album)
├── storage.py               # JSON persistence manager
├── ui.py                    # UI utilities and color formatting
├── library_interface.py     # Library management interface
├── playlist_interface.py    # Playlist management interface
├── queue_interface.py       # Queue and player interface
└── data/                    # Data storage directory
    ├── tracks.json          # All tracks
    ├── playlists.json       # All playlists
    ├── queue.json           # Current queue state
    └── albums.json          # Album information
```

## Getting Started

### Prerequisites
- Python 3.6+
- No external dependencies required

### Running the Application

```bash
cd MAIN
python main.py
```

## Usage Guide

### Music Library
1. **Add New Track**
   - Enter track details: title, artist, album, duration (mm:ss)
   - Optional: add additional artists
   - Track is automatically added to the correct album

2. **Search Tracks**
   - Search by track title
   - View all matching results
   - Add results to playlists

3. **View Library**
   - View all tracks with pagination
   - Tracks are automatically sorted

### Playlists
1. **Create Playlist**
   - Enter unique playlist name
   - Playlist created and ready for tracks

2. **Add Tracks to Playlist**
   - Browse library and select tracks
   - Or search for specific tracks
   - Each track can only be added once per playlist

3. **Manage Playlist**
   - View playlist details and duration
   - Remove tracks
   - Delete entire playlist

### Queue & Player
1. **Create Queue**
   - From entire library
   - From specific playlist

2. **Playback Controls**
   - Play: Start playing current track
   - Next: Skip to next track
   - Previous: Go to previous track
   - Shuffle: Randomize track order (keeps current track)
   - Repeat: Loop queue when reaching end

3. **Queue Management**
   - Add individual tracks
   - Add entire playlists
   - Clear queue
   - View paginated queue

## Data Format

### Track (JSON)
```json
{
  "title": "Gangnam Style",
  "artist": "PSY",
  "album": "Psy 6 (Six Rules), Part 1",
  "duration": "03:39",
  "additional_artists": "",
  "date_added": "2025-11-29T..."
}
```

### Playlist (JSON)
```json
{
  "name": "My Playlist",
  "tracks": [...],
  "date_created": "2025-11-29T..."
}
```

## Algorithm Details

### Queue Operations (O(1))
- **Next**: Move to next node in circular list
- **Previous**: Move to previous node in circular list
- **Current Track Tracking**: Pointer maintains current position

### Shuffle Algorithm
- Creates copy of track list
- Removes current track
- Randomizes remaining tracks
- Rebuilds queue with current track at front
- Maintains current track reference

### Unshuffle Algorithm
- Restores original track order
- Relocates current track to same position in original order

### Sorting
- Tracks sorted by: Title → Artist → Album → Duration
- Automatic when loading from storage

## Requirements Met

✅ Create tracks and add to library with permanent storage
✅ Create playlists with permanent storage
✅ Establish queues with shuffle and repeat modes
✅ Search tracks and add to playlists
✅ Music library with sorted tracks
✅ Playlists with distinct tracks (no duplicates)
✅ Queue with O(1) operations
✅ Shuffle mode (maintains current track)
✅ Repeat mode
✅ Pagination (both playlists and queue)
✅ Current track remains constant during shuffle/unshuffle
✅ Persistent data storage (JSON)
✅ No database usage (JSON only)

## Future Enhancements

- Album tracking and browsing
- Import tracks from CSV/JSON files
- Playlist sorting options
- Advanced shuffle algorithms
- Shuffle + Repeat combination
- GUI interface
- Music file playback integration

## License

This project is part of the Data Structure and Algorithms course (ITCC47) and Object-Oriented Programming course (ITCC45).

## Authors

Team Members:
- Ang, Chellzie
- Baquilid, Charmaine
- Ramiso, Modesthea
- Solon, Shekinah
- Tee, Kim Hie

BSIT 2C
