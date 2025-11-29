"""
Sample data initialization script
Run this once to populate the application with sample tracks and playlists
"""
from storage import StorageManager
from models import Track, Playlist


def initialize_sample_data():
    """Initialize the application with sample data"""
    storage = StorageManager(data_dir="./data")
    
    # Sample tracks
    sample_tracks = [
        Track("Gangnam Style", "PSY", "Psy 6 (Six Rules), Part 1", "03:39"),
        Track("Call Me Maybe", "Carly Rae Jepsen", "Kiss", "03:13"),
        Track("Timber", "Kesha", "Cannibal", "03:24", "Pitbull"),
        Track("Roar", "Katy Perry", "Prism", "03:44"),
        Track("I Knew You Were Trouble", "Taylor Swift", "Red", "03:40"),
        Track("Just Dance", "Lady Gaga", "The Fame", "04:02", "Colby O'Donis"),
        Track("Domino", "Jessie J", "Who Is Jessie J?", "03:52"),
        Track("Payphone", "Maroon 5", "Overexposed", "03:51", "Wiz Khalifa"),
        Track("Blinded in Chains", "Avenged Sevenfold", "Nightmare", "06:34"),
        Track("Counting Stars", "OneRepublic", "Native", "04:17"),
        Track("Bad Romance", "Lady Gaga", "The Fame Monster", "04:55"),
        Track("GAS GAS GAS EXTENDED MIX", "Manuel", "GAS", "04:21"),
        Track("Levitating", "Dua Lipa", "Future Nostalgia", "03:23", "DaBaby"),
        Track("Heat Waves", "Glass Animals", "Dreamland", "03:56"),
        Track("Blinding Lights", "The Weeknd", "After Hours", "03:20"),
        Track("Anti-Hero", "Taylor Swift", "Midnights", "03:20"),
        Track("As It Was", "Harry Styles", "Harry's House", "02:45"),
        Track("Unholy", "Sam Smith", "Gloria", "04:11", "Kim Petras"),
        Track("Cruel Summer", "Taylor Swift", "Lover", "03:58"),
        Track("Arctic Monkeys", "Do I Wanna Know?", "AM", "04:13"),
    ]
    
    print("Adding sample tracks...")
    added = 0
    for track in sample_tracks:
        if storage.save_track(track):
            added += 1
            print(f"  ✓ Added: {track.title}")
        else:
            print(f"  - Skipped (already exists): {track.title}")
    
    print(f"\nTotal tracks added: {added}/{len(sample_tracks)}")
    
    # Create sample playlists
    print("\nCreating sample playlists...")
    
    # Playlist 1: Pop Hits
    pop_hits = Playlist("Pop Hits")
    for track in sample_tracks[:5]:
        pop_hits.add_track(track)
    storage.save_playlist(pop_hits)
    print("  ✓ Created: Pop Hits")
    
    # Playlist 2: Dance Party
    dance_party = Playlist("Dance Party")
    for track in [sample_tracks[0], sample_tracks[1], sample_tracks[2], 
                  sample_tracks[6], sample_tracks[7]]:
        dance_party.add_track(track)
    storage.save_playlist(dance_party)
    print("  ✓ Created: Dance Party")
    
    # Playlist 3: Workout Mix
    workout_mix = Playlist("Workout Mix")
    for track in [sample_tracks[8], sample_tracks[11], sample_tracks[13],
                  sample_tracks[15]]:
        workout_mix.add_track(track)
    storage.save_playlist(workout_mix)
    print("  ✓ Created: Workout Mix")
    
    # Playlist 4: Chill Vibes
    chill_vibes = Playlist("Chill Vibes")
    for track in [sample_tracks[4], sample_tracks[9], sample_tracks[10],
                  sample_tracks[14]]:
        chill_vibes.add_track(track)
    storage.save_playlist(chill_vibes)
    print("  ✓ Created: Chill Vibes")
    
    print("\n✓ Sample data initialized successfully!")
    print("\nYou can now run: python main.py")


if __name__ == "__main__":
    print("=" * 50)
    print("Music Playlist System - Sample Data Initialization")
    print("=" * 50)
    print()
    
    initialize_sample_data()
