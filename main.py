import json
import random
import os

# ===========================
# JSON File Loader/Saver
# ===========================

def load_data(file):
    if not os.path.exists(file):
        with open(file, "w") as f:
            f.write("[]")
    with open(file, "r") as f:
        return json.load(f)

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# ===========================
# Display Playlist (ASCII Table)
# ===========================

def display_playlist():
    print("=" * 113)
    print("{0:>64}".format("(Playlist Name)"))
    print("=" * 113)
    print("| {0:<40} | {1:<20} | {2:<30} | {3:<10} |".format("Title", "Artist", "Album", "Duration"))
    print("=" * 113)
    for track in tracks:
        print("| {0:<40} | {1:<20} | {2:<30} | {3:<10} |".format(
            track["title"],
            track["artist"],
            track["album"],
            track["duration"]
        ))
        
    if len(songs) == 0:
        for _ in range(4):
            print("| {:<{}} | {:<{}} | {:<{}} | {:>{}} |".format(
                "", title_w, "", artist_w, "", album_w, "00:00", duration_w
            ))
    else:
        for s in songs:
            print("| {:<{}} | {:<{}} | {:<{}} | {:>{}} |".format(
                s["title"], title_w,
                s["artist"], artist_w,
                s["album"], album_w,
                s["duration"], duration_w
            ))

    print(row_border)

# ===========================
# Add Song
# ===========================

def add_song(library):
    print("\nEnter song details:")

    title = input("Title: ")
    artist = input("Artist: ")
    album = input("Album: ")
    duration = input("Duration (MM:SS): ")
    genre = input("Genre: ")

    new_song = {
        "title": title,
        "artist": artist,
        "album": album,
        "duration": duration,
        "genre": genre
    }

    library.append(new_song)
    print("\n🎵 Song '{}' added successfully!\n".format(title))

# ===========================
# View Songs
# ===========================

def view_songs(library):
    print("\n=== SONG LIBRARY ===\n")

    if len(library) == 0:
        print("No songs yet, sweetheart.\n")
        return

    for i, song in enumerate(library):
        print("{}{}. {} - {} ({}) [{}] [{}]".format(
            "", i+1,
            song["title"],
            song["artist"],
            song["album"],
            song["duration"],
            song["genre"]
        ))
    print()

# ===========================
# Search Song
# ===========================

def search_song(library):
    keyword = input("\nSearch: ").lower()
    results = [s for s in library if keyword in s["title"].lower()]

    if len(results) == 0:
        print("\nNo results found.\n")
        return

    print("\n=== SEARCH RESULTS ===")
    for i, song in enumerate(results):
        print("{}. {} - {} ({}) [{}]".format(
            i+1,
            song["title"],
            song["artist"],
            song["album"],
            song["duration"]
        ))
    print()

# ===========================
# Shuffle Play
# ===========================

def shuffle_play(library):
    if len(library) == 0:
        print("\nNo songs to shuffle.\n")
        return

    shuffled = library[:]
    random.shuffle(shuffled)

    print("🔀 Shuffling {} songs...".format(len(shuffled)))
    first = shuffled[0]
    print("🎶 Playing: {} by {}\n".format(first["title"], first["artist"]))

# ===========================
# Playlist Management
# ===========================

def create_playlist(playlists):
    name = input("\nPlaylist name: ")

    if name in playlists:
        print("Playlist already exists.\n")
        return

    playlists[name] = []
    print("✅ Playlist '{}' created!\n".format(name))

def add_to_playlist(library, playlists):
    playlist = input("\nPlaylist name: ")

    if playlist not in playlists:
        print("Playlist does not exist.\n")
        return

    title = input("Song title to add: ")
    for s in library:
        if s["title"].lower() == title.lower():
            playlists[playlist].append(s)
            print("🎵 '{}' added to playlist '{}'\n".format(title, playlist))
            return

    print("Song not found.\n")

def view_playlist(playlists):
    name = input("\nWhich playlist: ")

    if name not in playlists:
        print("Playlist does not exist.\n")
        return

    songs = playlists[name]
    display_playlist(name, songs)

# ===========================
# Queue System
# ===========================

def queue_add(queue, library):
    title = input("Song title to queue: ").lower()

    for s in library:
        if s["title"].lower() == title:
            queue.append(s)
            print("🎵 '{}' added to queue!\n".format(s["title"]))
            return

    print("Song not found.\n")

def play_queue(queue):
    if len(queue) == 0:
        print("\nQueue is empty.\n")
        return

    print("\n▶️ Playing queue ({} songs)...".format(len(queue)))

    for s in queue:
        print("🎶 {} by {}".format(s["title"], s["artist"]))

    print()
    queue.clear()

# ===========================
# MAIN PROGRAM LOOP
# ===========================

def main():
    library = load_data("library.json")
    playlists = load_data("playlists.json")
    queue = []

    while True:
        print("\n--- Terminal Music Player ---")
        print("1. Add Song")
        print("2. View Songs")
        print("3. Search Song")
        print("4. Shuffle Play")
        print("5. Create Playlist")
        print("6. Add to Playlist")
        print("7. View Playlist")
        print("8. Add to Queue")
        print("9. Play Queue")
        print("0. Exit")

        choice = input("\nChoose: ")

        if choice == "1":
            add_song(library)

        elif choice == "2":
            view_songs(library)

        elif choice == "3":
            search_song(library)

        elif choice == "4":
            shuffle_play(library)

        elif choice == "5":
            create_playlist(playlists)

        elif choice == "6":
            add_to_playlist(library, playlists)

        elif choice == "7":
            view_playlist(playlists)

        elif choice == "8":
            queue_add(queue, library)

        elif choice == "9":
            play_queue(queue)

        elif choice == "0":
            save_data("library.json", library)
            save_data("playlists.json", playlists)
            print("\nGoodbye, sweetheart. I’ll miss you. 💋\n")
            break

        else:
            print("Invalid choice.\n")

main()
