'''
Demonstration of Music Library System
- Create and manage tracks
- Create and manage playlists
- Create and manage music queues
- Search for tracks
'''

from file import File, MusicLibrary, PlaylistManager, MusicQueue

# Initialize the system
file_manager = File('data.json')
library = MusicLibrary(file_manager)
playlist_manager = PlaylistManager(file_manager)
music_queue = MusicQueue(file_manager)

print("=" * 60)
print("MUSIC LIBRARY SYSTEM DEMO")
print("=" * 60)

# 1. ADD NEW TRACKS TO LIBRARY
print("\n1. ADDING NEW TRACKS TO LIBRARY")
print("-" * 60)
library.add_track('Toby Fox', 'Megalovania', 'Undertale', '4:08', 'Electronic')
library.add_track('Toby Fox', 'Hopes and Dreams', 'Undertale', '5:09', 'Electronic')
library.add_track('Yoko Kanno', 'Tank!', 'Cowboy Bebop', '1:34', 'Jazz')
library.add_track('Yoko Kanno', 'The Real Folk Blues', 'Cowboy Bebop', '3:17', 'Jazz')

# Display the library
print("\nCurrent Library:")
library.display_library()

# 2. CREATE PLAYLISTS AND ADD TRACKS
print("\n2. CREATING PLAYLISTS AND ADDING TRACKS")
print("-" * 60)
playlist1 = playlist_manager.create_playlist('Gaming Anthems')
playlist_manager.add_to_playlist('Gaming Anthems', 'Toby Fox', 'Megalovania')
playlist_manager.add_to_playlist('Gaming Anthems', 'Toby Fox', 'Hopes and Dreams')

playlist2 = playlist_manager.create_playlist('Anime Favorites')
playlist_manager.add_to_playlist('Anime Favorites', 'Yoko Kanno', 'Tank!')
playlist_manager.add_to_playlist('Anime Favorites', 'Yoko Kanno', 'The Real Folk Blues')

print("\nPlaylist 'Gaming Anthems':", playlist_manager.get_playlist('Gaming Anthems'))
print("Playlist 'Anime Favorites':", playlist_manager.get_playlist('Anime Favorites'))

# 3. CREATE MUSIC QUEUE
print("\n3. CREATING MUSIC QUEUE")
print("-" * 60)
print("Adding tracks from library to queue...")
music_queue.add_from_library(library, 'Toby Fox', 'Megalovania')
music_queue.add_from_library(library, 'Yoko Kanno', 'Tank!')

print("\nAdding entire 'Gaming Anthems' playlist to queue...")
music_queue.add_from_playlist(playlist_manager, 'Gaming Anthems')

print("\nCurrent Queue:")
print(music_queue.get_queue())

# 4. SEARCH FOR TRACKS
print("\n4. SEARCHING FOR TRACKS")
print("-" * 60)

# Search by artist
print("\nSearch results for 'Toby Fox':")
results = library.search_tracks('Toby Fox')
print(results)

# Search by genre
print("\nSearch results for 'Jazz':")
results = library.search_tracks('Jazz')
print(results)

# Search by track name
print("\nSearch results for 'Tank':")
results = library.search_tracks('Tank')
print(results)

# 5. SKIP AND MODIFY QUEUE
print("\n5. SKIPPING TRACKS IN QUEUE")
print("-" * 60)
current_track = music_queue.skip()
print(f"Now playing: {current_track}")
print(f"Remaining queue: {music_queue.get_queue()}")

print("\n" + "=" * 60)
print("DATA HAS BEEN PERMANENTLY SAVED TO:")
print("- data.json (music library)")
print("- playlists.json (playlists)")
print("- queue.json (music queue)")
print("=" * 60)
