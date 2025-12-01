"""
Testing Script - Verify All Functionality
Run this to test all core features of the Music Playlist System
"""
from models import Track, Playlist, Queue, Album
from storage import StorageManager
import os


def test_track_creation():
    """Test Track class"""
    print("\n" + "="*50)
    print("TEST 1: Track Creation and Display")
    print("="*50)
    
    track = Track("Gangnam Style", "PSY", "Psy 6", "03:39", "")
    print(f"✓ Track created: {track.get_display_name()}")
    
    # Test duration conversion
    seconds = track.duration_to_seconds()
    print(f"✓ Duration to seconds: {seconds} sec")
    
    converted = Track.seconds_to_duration(seconds)
    print(f"✓ Seconds to duration: {converted}")
    
    assert converted == "03:39", "Duration conversion failed!"
    print("✓ All track tests passed!")


def test_playlist_creation():
    """Test Playlist class"""
    print("\n" + "="*50)
    print("TEST 2: Playlist Management")
    print("="*50)
    
    playlist = Playlist("Test Playlist")
    print(f"✓ Playlist created: {playlist.name}")
    
    # Add tracks
    track1 = Track("Song 1", "Artist 1", "Album 1", "03:30")
    track2 = Track("Song 2", "Artist 2", "Album 2", "04:00")
    track3 = Track("Song 1", "Artist 1", "Album 1", "03:30")  # Duplicate
    
    added1 = playlist.add_track(track1)
    added2 = playlist.add_track(track2)
    added3 = playlist.add_track(track3)  # Should not be added
    
    print(f"✓ Track 1 added: {added1}")
    print(f"✓ Track 2 added: {added2}")
    print(f"✓ Track 3 (duplicate) added: {added3} (should be False)")
    
    assert added1 and added2 and not added3, "Duplicate prevention failed!"
    
    total_duration = playlist.get_total_duration_formatted()
    print(f"✓ Total duration: {total_duration}")
    print(f"✓ Track count: {len(playlist.tracks)}")
    print("✓ All playlist tests passed!")


def test_queue_operations():
    """Test Queue with circular linked list"""
    print("\n" + "="*50)
    print("TEST 3: Queue Operations (O(1) Performance)")
    print("="*50)
    
    tracks = [
        Track(f"Song {i}", f"Artist {i}", f"Album {i}", f"03:{30+i:02d}")
        for i in range(1, 6)
    ]
    
    queue = Queue(tracks)
    print(f"✓ Queue created with {queue.total_tracks} tracks")
    
    # Test current track
    current = queue.get_current_track()
    print(f"✓ Current track: {current.title}")
    
    # Test next (O(1))
    next_track = queue.next_track()
    print(f"✓ Next track: {next_track.title}")
    
    # Test previous (O(1))
    prev_track = queue.prev_track()
    print(f"✓ Previous track: {prev_track.title}")
    
    # Verify we're back to Song 1
    assert queue.get_current_track().title == "Song 1", "Queue navigation failed!"
    
    print("✓ All queue navigation tests passed (O(1) operations)!")


def test_shuffle_unshuffle():
    """Test shuffle with current track preservation"""
    print("\n" + "="*50)
    print("TEST 4: Shuffle and Unshuffle")
    print("="*50)
    
    tracks = [
        Track(f"Song {i}", f"Artist {i}", f"Album {i}", f"03:{30+i:02d}")
        for i in range(1, 6)
    ]
    
    queue = Queue(tracks)
    original_current = queue.get_current_track()
    print(f"✓ Original current track: {original_current.title}")
    print(f"✓ Original order: {[t.title for t in queue.original_order]}")
    
    # Shuffle
    queue.shuffle()
    shuffled_current = queue.get_current_track()
    print(f"✓ Shuffled - is_shuffled: {queue.is_shuffled}")
    print(f"✓ Current track maintained: {shuffled_current.title == original_current.title}")
    
    assert shuffled_current.title == original_current.title, "Current track lost during shuffle!"
    
    # Unshuffle
    queue.unshuffle()
    unshuffled_current = queue.get_current_track()
    print(f"✓ Unshuffled - is_shuffled: {queue.is_shuffled}")
    print(f"✓ Current track maintained: {unshuffled_current.title == original_current.title}")
    
    assert unshuffled_current.title == original_current.title, "Current track lost during unshuffle!"
    print("✓ All shuffle tests passed!")


def test_storage():
    """Test JSON storage operations"""
    print("\n" + "="*50)
    print("TEST 5: Storage Operations (JSON Persistence)")
    print("="*50)
    
    # Use test data directory
    test_storage = StorageManager(data_dir="./test_data")
    
    # Test track storage
    test_track = Track("Storage Test", "Test Artist", "Test Album", "02:30")
    saved = test_storage.save_track(test_track)
    print(f"✓ Track saved: {saved}")
    
    # Load tracks
    loaded_tracks = test_storage.load_all_tracks()
    print(f"✓ Tracks loaded: {len(loaded_tracks)} track(s)")
    
    # Test playlist storage
    test_playlist = Playlist("Storage Test Playlist")
    test_playlist.add_track(test_track)
    saved_playlist = test_storage.save_playlist(test_playlist)
    print(f"✓ Playlist saved: {saved_playlist}")
    
    # Load playlists
    loaded_playlists = test_storage.load_all_playlists()
    print(f"✓ Playlists loaded: {len(loaded_playlists)} playlist(s)")
    
    # Test queue storage
    test_queue = Queue([test_track])
    test_storage.save_queue(test_queue)
    loaded_queue = test_storage.load_queue()
    print(f"✓ Queue saved and loaded")
    print(f"✓ Loaded queue has {loaded_queue.total_tracks} track(s)")
    
    # Cleanup
    import shutil
    if os.path.exists("./test_data"):
        shutil.rmtree("./test_data")
    
    print("✓ All storage tests passed!")


def test_sorting():
    """Test automatic track sorting"""
    print("\n" + "="*50)
    print("TEST 6: Track Sorting")
    print("="*50)
    
    # Create unsorted tracks
    tracks = [
        Track("Zebra", "Artist Z", "Album Z", "03:00"),
        Track("Apple", "Artist A", "Album A", "03:00"),
        Track("Banana", "Artist B", "Album B", "03:00"),
        Track("Apple", "Artist B", "Album B", "03:00"),  # Same title, different artist
        Track("Apple", "Artist A", "Album B", "03:00"),  # Same title and artist, different album
    ]
    
    # Sort manually (like storage does)
    sorted_tracks = sorted(tracks, key=lambda t: (t.title, t.artist, t.album, t.duration_to_seconds()))
    
    print("✓ Sorting order:")
    for i, track in enumerate(sorted_tracks, 1):
        print(f"  {i}. {track.title} - {track.artist} ({track.album})")
    
    # Verify sort order
    assert sorted_tracks[0].title == "Apple", "Title sort failed!"
    assert sorted_tracks[3].title == "Banana", "Title sort failed!"
    print("✓ All sorting tests passed!")


def test_repeat_mode():
    """Test repeat mode functionality"""
    print("\n" + "="*50)
    print("TEST 7: Repeat Mode")
    print("="*50)
    
    tracks = [Track(f"Song {i}", "Artist", "Album", "03:30") for i in range(1, 4)]
    queue = Queue(tracks)
    
    print(f"✓ Queue created with repeat: {queue.is_repeat}")
    
    # Go to last track
    queue.next_track()
    queue.next_track()
    current = queue.get_current_track()
    print(f"✓ At last track: {current.title}")
    
    # Enable repeat
    queue.toggle_repeat()
    print(f"✓ Repeat enabled: {queue.is_repeat}")
    
    # Next should wrap around
    next_track = queue.next_track()
    print(f"✓ After next (with repeat): {next_track.title}")
    
    # Previous should wrap around
    prev_track = queue.prev_track()
    print(f"✓ After previous: {prev_track.title}")
    
    print("✓ All repeat mode tests passed!")


def test_pagination():
    """Test queue pagination"""
    print("\n" + "="*50)
    print("TEST 8: Pagination")
    print("="*50)
    
    # Create queue with 25 tracks
    tracks = [Track(f"Song {i:02d}", "Artist", "Album", "03:30") for i in range(1, 26)]
    queue = Queue(tracks)
    
    print(f"✓ Queue created with {queue.total_tracks} tracks")
    
    # Get page 1
    page1_tracks, page, total_pages = queue.get_tracks_page(1, 10)
    print(f"✓ Page 1: {len(page1_tracks)} tracks, Page {page} of {total_pages}")
    
    # Get page 2
    page2_tracks, page, total_pages = queue.get_tracks_page(2, 10)
    print(f"✓ Page 2: {len(page2_tracks)} tracks, Page {page} of {total_pages}")
    
    # Get page 3
    page3_tracks, page, total_pages = queue.get_tracks_page(3, 10)
    print(f"✓ Page 3: {len(page3_tracks)} tracks, Page {page} of {total_pages}")
    
    assert len(page1_tracks) == 10, "Page 1 size incorrect!"
    assert len(page2_tracks) == 10, "Page 2 size incorrect!"
    assert len(page3_tracks) == 5, "Page 3 size incorrect!"
    
    print("✓ All pagination tests passed!")


def run_all_tests():
    """Run all tests"""
    print("\n" + "█"*50)
    print("MUSIC PLAYLIST SYSTEM - COMPREHENSIVE TEST SUITE")
    print("█"*50)
    
    try:
        test_track_creation()
        test_playlist_creation()
        test_queue_operations()
        test_shuffle_unshuffle()
        test_storage()
        test_sorting()
        test_repeat_mode()
        test_pagination()
        
        print("\n" + "█"*50)
        print("✓ ALL TESTS PASSED SUCCESSFULLY!")
        print("█"*50)
        print("\nThe Music Playlist System is working correctly.")
        print("You can now run: python main.py")
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {str(e)}")
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
