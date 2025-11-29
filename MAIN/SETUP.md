# Setup and Installation Guide

## System Requirements

- Python 3.6 or higher
- Windows, macOS, or Linux
- Terminal/Command Prompt access

## Installation Steps

### 1. Navigate to the MAIN folder

```bash
cd "DSA-Project-Playlist\MAIN"
```

### 2. Initialize Sample Data (First Time Only)

To populate the application with sample tracks and playlists:

```bash
python init_sample_data.py
```

This will create:
- 20 sample tracks
- 4 sample playlists
- `data/` directory with JSON files

### 3. Run the Application

```bash
python main.py
```

## Quick Start

### First Run
1. Run `init_sample_data.py` to populate sample data
2. Run `main.py` to start the application
3. Explore the Music Library, Playlists, and Queue features

### Main Menu Options

**[1] Music Library**
- View all tracks in the library
- Add new tracks
- Search for tracks
- Delete tracks
- Play from library

**[2] Playlists**
- Create new playlists
- Open and manage playlists
- Add tracks to playlists
- Delete playlists

**[3] Queue & Player**
- Create queue from library
- Create queue from playlist
- Control playback (play, next, previous)
- Shuffle and repeat modes
- Add tracks to queue

**[4] About**
- View application information

**[5] Exit**
- Save and close application

## File Structure

```
MAIN/
├── main.py                      # Main application
├── models.py                    # Data structures
├── storage.py                   # JSON persistence
├── ui.py                        # UI utilities
├── library_interface.py         # Library management
├── playlist_interface.py        # Playlist management
├── queue_interface.py           # Queue and player
├── init_sample_data.py          # Sample data script
├── requirements.txt             # Dependencies (none!)
├── README.md                    # Documentation
├── SETUP.md                     # This file
└── data/                        # Data storage
    ├── tracks.json              # All tracks
    ├── playlists.json           # All playlists
    └── queue.json               # Current queue
```

## Data Storage

All data is saved in `data/` folder in JSON format:

### tracks.json
Contains all tracks in the music library with:
- Title, Artist, Album, Duration
- Additional artists (if any)
- Date added timestamp

### playlists.json
Contains all playlists with:
- Playlist name
- List of tracks
- Creation timestamp

### queue.json
Contains the current queue state:
- Track list
- Current playing track
- Shuffle and repeat status

## Adding Custom Tracks

### Through the Application
1. Run `main.py`
2. Select [1] Music Library
3. Select [2] Add new track
4. Enter track details
5. Track is automatically sorted

### Format for Duration
Use `mm:ss` format (e.g., `03:45` for 3 minutes 45 seconds)

## Creating Playlists

1. From main menu, select [2] Playlists
2. Select [1] Create new playlist
3. Enter unique playlist name
4. Add tracks from library or search

## Using the Player

1. From main menu, select [3] Queue & Player
2. Choose to create queue from:
   - Entire library
   - Specific playlist
3. Use playback controls:
   - [1] Play current track
   - [2] Next track
   - [3] Previous track
   - [4] Toggle repeat
   - [5] Toggle shuffle
   - [6] Clear queue
   - [7] Add more tracks

## Troubleshooting

### Application won't start
- Ensure Python 3.6+ is installed
- Check you're in the MAIN directory
- Try running: `python --version`

### Data not saving
- Check if `data/` folder exists
- Ensure write permissions in MAIN folder
- Close application properly (use Exit menu)

### Sample data already exists
- Sample data won't be duplicated
- Run `init_sample_data.py` again, it skips existing tracks

### Queue is empty
- Ensure tracks exist in library
- Create new queue from [3] Queue & Player menu

## Features Explained

### Circular Linked List Queue
- Used for O(1) next/previous operations
- Maintains current track during shuffle
- Enables shuffle and repeat functionality

### Track Sorting
Tracks are sorted by:
1. Title
2. Artist name
3. Album
4. Duration

### Shuffle Algorithm
- Preserves current playing track
- Returns to original order with unshuffle
- Randomizes other tracks around current

### Pagination
- Library: 15 tracks per page
- Playlists: 10 playlists per page
- Queue: 10 tracks per page

## Data Backup

To backup your data:
1. Copy the `data/` folder
2. Keep it in a safe location
3. To restore: replace `data/` folder with backup

## Notes

- All data is saved to JSON (no database)
- Application resumes queue state on restart
- Each track in playlist can only appear once
- Playlists must have unique names
- No external dependencies required

## Running in Development

### Check Python Syntax
```bash
python -m py_compile models.py
python -m py_compile storage.py
```

### Run with Debug Output
```bash
python -u main.py
```

## Performance

- **Track Operations**: O(1) for adding, searching
- **Queue Operations**: O(1) for next/previous
- **Playlist Operations**: O(1) for adding tracks
- **Sorting**: O(n log n) when loading tracks

## License & Credits

This project is part of ITCC47 (Data Structures & Algorithms) and ITCC45 (OOP) courses.

Team: BSIT 2C
- Ang, Chellzie
- Baquilid, Charmaine
- Ramiso, Modesthea
- Solon, Shekinah
- Tee, Kim Hie

For more information, see README.md
