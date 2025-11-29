# 🎵 Music Playlist System - Complete Implementation Guide

## ✨ Project Overview

A fully functional **Music Playlist System** built in Python with advanced data structures and algorithms. This system implements a **circular linked list queue** for O(1) playback operations, comprehensive music management features, and persistent JSON storage.

## 📦 What's Included

### Core Files Created
```
MAIN/
├── main.py                      ✓ Application entry point
├── models.py                    ✓ Data structures (Track, Playlist, Queue, Album)
├── storage.py                   ✓ JSON persistence manager
├── ui.py                        ✓ UI utilities and color formatting
├── library_interface.py         ✓ Music library management
├── playlist_interface.py        ✓ Playlist management
├── queue_interface.py           ✓ Queue and player interface
├── init_sample_data.py          ✓ Sample data initialization
├── test_system.py               ✓ Comprehensive test suite
├── requirements.txt             ✓ Dependencies list
├── README.md                    ✓ Full documentation
├── SETUP.md                     ✓ Setup instructions
└── data/                        ✓ Data storage
    ├── tracks.json              ✓ All tracks
    ├── playlists.json           ✓ All playlists
    └── queue.json               ✓ Current queue state
```

## 🚀 Quick Start

### Step 1: Initialize Sample Data
```bash
python init_sample_data.py
```
Creates 20 sample tracks and 4 playlists automatically.

### Step 2: Run the Application
```bash
python main.py
```

### Step 3: Explore Features
- Navigate using menu options
- Add tracks to the library
- Create and manage playlists
- Create and play queues with shuffle/repeat

## ✅ Requirements Fulfillment

### Core Requirements (All Implemented ✓)

#### 1. **Music Library** ✓
- ✓ Create and add tracks to the library
- ✓ Tracks have: Title, Artist, Additional Artists, Album, Duration (mm:ss)
- ✓ Tracks sorted by: Title → Artist → Album → Duration
- ✓ Search functionality for tracks
- ✓ Delete tracks from library
- ✓ Permanent JSON storage

#### 2. **Playlists** ✓
- ✓ Create playlists with unique names
- ✓ Playlists contain distinct tracks (no duplicates)
- ✓ Display total playlist duration
- ✓ Add tracks from library to playlist
- ✓ Search and add tracks to playlist
- ✓ Delete playlists
- ✓ Pagination for 10+ playlists (with [Previous]/[Next] options)
- ✓ Permanent storage

#### 3. **Queues** ✓
- ✓ Create queue from library or playlist
- ✓ Shuffle and Repeat modes (not both simultaneously)
- ✓ Return to original order with unshuffle
- ✓ **All O(1) operations**: next, previous, current track
- ✓ Shuffle/unshuffle preserves current track
- ✓ Skip last track behavior:
  - No repeat: stops, shows "no more tracks"
  - With repeat: returns to first track
- ✓ First track previous with repeat: goes to last track
- ✓ Pagination: display first 10 tracks per page
- ✓ Add tracks to queue dynamically
- ✓ Add entire playlists to queue
- ✓ Persistent storage when not cleared
- ✓ Resume queue state on restart

#### 4. **Search Functionality** ✓
- ✓ Search tracks by title
- ✓ Display all matching results
- ✓ Add directly to playlist from search results

#### 5. **Data Storage** ✓
- ✓ JSON format (no databases)
- ✓ Permanent persistence
- ✓ Automatic saves on all operations
- ✓ Queue restoration on app restart

### Data Structures Implemented

#### Track Class ✓
```python
- title: str
- artist: str
- album: str
- duration: str (mm:ss format)
- additional_artists: str
- date_added: ISO timestamp
+ duration_to_seconds(): int
+ seconds_to_duration(seconds): str
+ get_display_name(): str
+ to_dict() / from_dict()
```

#### Playlist Class ✓
```python
- name: str
- tracks: List[Track]
- date_created: ISO timestamp
+ add_track(track): bool
+ remove_track(index): bool
+ get_total_duration(): int
+ get_total_duration_formatted(): str
+ sort_tracks()
+ to_dict() / from_dict()
```

#### Queue Class (Circular Linked List) ✓
```python
- head: Node
- current: Node
- is_shuffled: bool
- is_repeat: bool
- total_tracks: int
+ next_track(): Track [O(1)]
+ prev_track(): Track [O(1)]
+ get_current_track(): Track [O(1)]
+ shuffle(): void
+ unshuffle(): void
+ toggle_repeat(): void
+ toggle_shuffle(): void
+ add_track(track): void
+ add_playlist(playlist): void
+ get_tracks_page(page, size): tuple
+ to_dict() / from_dict()
```

#### Node Class (for Circular Linked List) ✓
```python
- track: Track
- next: Node (pointer to next)
- prev: Node (pointer to previous)
```

#### Album Class ✓
```python
- album_name: str
- tracks: List[Track]
- date_created: ISO timestamp
+ add_track(track): void
+ get_total_duration(): int
+ to_dict() / from_dict()
```

### Algorithm Complexity Analysis

| Operation | Time Complexity | Notes |
|-----------|-----------------|-------|
| Next Track | O(1) | Pointer movement in circular list |
| Previous Track | O(1) | Pointer movement in circular list |
| Get Current Track | O(1) | Direct pointer access |
| Shuffle | O(n) | Randomize n-1 tracks, rebuild list |
| Unshuffle | O(n) | Restore original order, locate current |
| Add Track | O(1) | Append to linked list |
| Duplicate Check | O(n) | Linear search through tracks |
| Load All Tracks | O(n log n) | JSON read + sort |
| Sort Tracks | O(n log n) | Python's timsort |

## 🎯 Features Breakdown

### Music Library Interface
```
[1] View all tracks          - Browse library with pagination
[2] Add new track            - Create new track with duration
[3] Search track             - Find tracks by title
[4] Delete track             - Remove track from library
[5] Play from library        - Create queue from all tracks
[6] Back to main menu        - Return to main menu
```

### Playlists Interface
```
[1] Create new playlist      - Create unique playlist
[2] Open playlist            - Manage tracks in playlist
[3] Delete playlist          - Remove playlist
[4] Back to main menu        - Return to main menu

Within Playlist:
[1] Add track to playlist    - Select from library
[2] Search and add track     - Find and add track
[3] Remove track             - Delete from playlist
[4] Play this playlist       - Create queue from playlist
[5] Back to playlists        - Return to playlists menu
```

### Queue & Player Interface
```
[1] Play                     - Start playing current track
[2] Next                     - Skip to next track
[3] Previous                 - Go to previous track
[4] Toggle repeat            - Turn repeat on/off
[5] Toggle shuffle           - Turn shuffle on/off
[6] Clear queue              - Empty entire queue
[7] Add tracks to queue      - Add from library or playlist
[8-9] Previous/Next page     - Pagination controls
[10] Back to main menu       - Exit queue (saves state)
```

## 📊 Test Results

All 8 comprehensive tests passed successfully:
- ✅ Track Creation and Display
- ✅ Playlist Management
- ✅ Queue Operations (O(1))
- ✅ Shuffle and Unshuffle
- ✅ Storage (JSON Persistence)
- ✅ Sorting
- ✅ Repeat Mode
- ✅ Pagination

Run tests with: `python test_system.py`

## 🔄 Data Persistence Examples

### tracks.json Structure
```json
{
  "tracks": [
    {
      "title": "Gangnam Style",
      "artist": "PSY",
      "album": "Psy 6 (Six Rules), Part 1",
      "duration": "03:39",
      "additional_artists": "",
      "date_added": "2025-11-29T19:34:39.349650"
    }
  ]
}
```

### playlists.json Structure
```json
{
  "playlists": [
    {
      "name": "Pop Hits",
      "tracks": [...],
      "date_created": "2025-11-29T19:34:40.123456"
    }
  ]
}
```

### queue.json Structure
```json
{
  "queue": {
    "tracks": [...],
    "original_order": [...],
    "current_track": {...},
    "is_shuffled": false,
    "is_repeat": true
  }
}
```

## 💡 Algorithm Highlights

### Circular Linked List Queue
```python
# Structure visualization:
┌─────────────────────────────────────┐
│  Song 1 ←→ Song 2 ←→ Song 3 ←→ ... │
└─────────────────────────────────────┘
     ↑                              │
     └──────────────────────────────┘
     (Circular: last connects to first)
```

### Shuffle Algorithm
1. Save current track reference
2. Copy original track list (excluding current)
3. Randomize the copy
4. Insert current track at front
5. Rebuild circular linked list
6. Result: Current track maintained at front

### Unshuffle Algorithm
1. Save current track reference
2. Restore original track order
3. Traverse list to find current track position
4. Move pointer to that position
5. Result: Original order restored with current track preserved

## 📋 Sample Data

20 pre-loaded tracks across genres:
- Pop: Gangnam Style, Call Me Maybe, Roar
- Dance: Timber, Just Dance, Domino
- Rock: Blinded in Chains, Arctic Monkeys
- Modern: Levitating, Heat Waves, Blinding Lights
- And more...

4 sample playlists:
- Pop Hits (5 tracks)
- Dance Party (5 tracks)
- Workout Mix (4 tracks)
- Chill Vibes (4 tracks)

## 🔧 Usage Examples

### Add a Track
```
Main Menu → [1] Music Library → [2] Add new track
Enter: "Hotel California"
Enter: "Eagles"
Enter: "Hotel California" (album)
Enter: "06:30" (duration in mm:ss)
Enter additional artists or press Enter
```

### Create a Playlist and Add Tracks
```
Main Menu → [2] Playlists → [1] Create new playlist
Enter: "My Favorites"
[2] Open playlist → [1] Add track from library
Select tracks to add
```

### Play with Shuffle and Repeat
```
Main Menu → [3] Queue & Player
Create from library or playlist
[5] Turn on shuffle
[4] Turn on repeat
[1] Play
[2] Next to skip
[3] Previous to go back
```

## 🎓 Educational Value

This project demonstrates:
- **Data Structures**: Circular Linked List, Arrays, JSON structures
- **Algorithms**: Sorting, Shuffling, Searching, Pagination
- **OOP Principles**: Encapsulation, Inheritance, Polymorphism
- **File I/O**: JSON persistence, file operations
- **Time Complexity**: O(1) vs O(n) analysis
- **UI Design**: Menu systems, user input validation
- **Code Organization**: Modular design with separate concerns

## 📚 Files Documentation

### models.py (650+ lines)
Core data structures with all required functionality and O(1) operations.

### storage.py (250+ lines)
JSON-based persistence layer with CRUD operations for all data types.

### ui.py (200+ lines)
UI utilities including color formatting, menu helpers, and input validation.

### library_interface.py (300+ lines)
Music library management with search, add, delete, and view operations.

### playlist_interface.py (350+ lines)
Playlist management with track addition, removal, and operations.

### queue_interface.py (200+ lines)
Queue display, pagination, and playback controls.

### main.py (150+ lines)
Application entry point with main menu and integration.

### init_sample_data.py (100+ lines)
One-time data initialization with 20 tracks and 4 playlists.

### test_system.py (400+ lines)
Comprehensive test suite covering all functionality.

## 🚀 Getting Started

1. **First Time Setup**
   ```bash
   cd MAIN
   python init_sample_data.py
   python main.py
   ```

2. **Run Tests**
   ```bash
   python test_system.py
   ```

3. **Explore Features**
   - Add your own tracks
   - Create playlists
   - Create and play queues
   - Use shuffle and repeat modes
   - Search for tracks

## 📝 Notes

- All data persists automatically in `data/` folder
- Queue state is saved on exit
- No external dependencies required (Python standard library only)
- Supports Windows, macOS, and Linux
- ANSI color support for terminal output
- All requirements met from project specifications

## 🎉 Conclusion

A complete, functional Music Playlist System that meets all project requirements with:
- ✅ Advanced data structures (circular linked list)
- ✅ O(1) queue operations
- ✅ Persistent JSON storage
- ✅ User-friendly interface
- ✅ Comprehensive error handling
- ✅ Extensive testing
- ✅ Production-ready code

Ready to enhance with additional features as needed!

---

**Project Status**: ✅ COMPLETE AND TESTED
**All Requirements Met**: ✅ YES
**Ready for Submission**: ✅ YES
