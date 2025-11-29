# 🎵 Quick Reference Card

## Starting the App

```bash
# Initialize sample data (first time only)
python init_sample_data.py

# Run the application
python main.py

# Run tests
python test_system.py
```

## Main Menu Options

```
[1] Music Library       - Manage tracks
[2] Playlists          - Manage playlists
[3] Queue & Player     - Play music
[4] About              - View info
[5] Exit               - Close app
```

## Music Library Commands

```
[1] View all tracks    - Browse with pagination
[2] Add new track      - Create track (mm:ss format)
[3] Search track       - Find by title
[4] Delete track       - Remove from library
[5] Play from library  - Create queue with all tracks
[6] Back               - Return to main menu
```

## Playlist Commands

```
[1] Create new         - New playlist (unique name)
[2] Open playlist      - Manage tracks
[3] Delete playlist    - Remove playlist
[4] Back               - Return to main menu
```

## Queue/Player Commands

```
[1] Play               - Start playing
[2] Next               - Skip track
[3] Previous           - Go back
[4] Toggle repeat      - On/Off
[5] Toggle shuffle     - On/Off
[6] Clear queue        - Empty queue
[7] Add tracks         - Add to queue
[8-9] Pages            - Navigation
[10] Back              - Exit (saves)
```

## Duration Format

```
Always use: MM:SS format
Examples:
- 3 minutes 30 seconds → 03:30
- 1 minute 5 seconds → 01:05
- 45 seconds → 00:45
```

## Keyboard Shortcuts

```
Ctrl+C  - Exit app immediately
Enter   - Confirm/Continue
0       - Cancel operations
```

## Tips & Tricks

### Add Tracks Faster
1. Go to Music Library
2. Add new track
3. Enter all details
4. Track auto-sorts in library

### Create Queue Quickly
1. Queue & Player menu
2. Select library/playlist
3. Instant queue ready to play

### Search Tracks
1. In playlists
2. Search by title
3. Add directly to playlist

### Shuffle Smart
- Current track stays as "now playing"
- Unshuffle returns to original order
- Both operations in O(1) time

### Repeat Behavior
- No repeat: Stop at last track
- With repeat: Loop back to first
- First track previous: Goes to last

## File Structure

```
MAIN/
├── main.py              - Start here
├── models.py            - Data structures
├── storage.py           - Data saving
├── ui.py                - Display stuff
├── library_interface.py - Tracks
├── playlist_interface.py- Playlists
├── queue_interface.py   - Player
├── data/
│   ├── tracks.json
│   ├── playlists.json
│   └── queue.json
└── [Other setup files]
```

## Data Storage Locations

```
Tracks:    data/tracks.json
Playlists: data/playlists.json
Queue:     data/queue.json
```

## Common Issues

| Issue | Solution |
|-------|----------|
| "Track already exists" | That track is already in this playlist |
| "Playlist name exists" | Use a unique name |
| Empty queue | Create queue from library or playlist |
| Data not saving | Use Exit menu, not Ctrl+C |
| Sample data not loading | Run: python init_sample_data.py |

## Sample Data

**20 tracks included:**
- Gangnam Style, Call Me Maybe, Timber
- Roar, I Knew You Were Trouble, Just Dance
- Domino, Payphone, Blinded in Chains
- Counting Stars, Bad Romance, GAS GAS GAS
- Levitating, Heat Waves, Blinding Lights
- Anti-Hero, As It Was, Unholy
- Cruel Summer, Arctic Monkeys

**4 playlists included:**
- Pop Hits (5 tracks)
- Dance Party (5 tracks)
- Workout Mix (4 tracks)
- Chill Vibes (4 tracks)

## Performance Notes

```
Operation          Time    Note
Next Track         O(1)    Instant pointer move
Previous Track     O(1)    Instant pointer move
Add to Queue       O(1)    Append to list
Shuffle           O(n)    Randomize n-1 tracks
Search            O(n)    Linear scan
Sort Tracks       O(n log n) Automatic on load
```

## Requirements Met ✓

- ✅ Music Library (add, search, delete)
- ✅ Playlists (create, manage, distinct tracks)
- ✅ Queues (shuffle, repeat, O(1) operations)
- ✅ Search functionality
- ✅ Persistent JSON storage
- ✅ Pagination (10+ playlists, 10 tracks/page)
- ✅ Current track preservation
- ✅ All user requirements

## Menu Navigation

```
MAIN MENU
├─ [1] LIBRARY
│  ├─ View all
│  ├─ Add track
│  ├─ Search
│  ├─ Delete
│  └─ Play
├─ [2] PLAYLISTS
│  ├─ Create
│  ├─ Open
│  └─ Delete
├─ [3] QUEUE
│  ├─ Create
│  ├─ Play
│  ├─ Control
│  └─ Manage
├─ [4] ABOUT
└─ [5] EXIT
```

## Input Tips

```
✓ DO:
- Use exact names when prompted
- Enter duration as MM:SS
- Select from numbered options
- Press Enter to confirm

✗ DON'T:
- Use Ctrl+C to exit (data may not save)
- Use special characters in names
- Enter invalid duration formats
- Skip required fields
```

## Getting Help

```
In App:
- Press Enter for help
- Select [4] About for info
- Menu options show available actions

Files:
- README.md - Full documentation
- SETUP.md - Setup instructions
- IMPLEMENTATION_SUMMARY.md - Detailed info
```

## Success Checklist

- ✓ Sample data initialized
- ✓ App runs without errors
- ✓ Can add and view tracks
- ✓ Can create playlists
- ✓ Can play with shuffle/repeat
- ✓ Data saves automatically
- ✓ Queue resumes after restart

---

**Quick Start**: `python init_sample_data.py` then `python main.py`

**Questions?** Check README.md and IMPLEMENTATION_SUMMARY.md
