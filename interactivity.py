import json
import random
from playsound import playsound

SONG_DB = "songs.json"
queue = []

# ------------------- Helper Functions -------------------
def load_songs():
    with open(SONG_DB, "r") as f:
        return json.load(f)

def save_songs(data):
    with open(SONG_DB, "w") as f:
        json.dump(data, f, indent=4)

# ------------------- Song Management -------------------
def add_song():
    title = input("Enter song title: ")
    album = input("Enter album: ")
    artist = input("Enter artist: ")
    duration = input("Enter duration (e.g. 3:45): ")
    genre = input("Enter genre: ")
    file_path = input("Enter file path: ")

    data = load_songs()
    data["songs"].append({
        "title": title,
        "album": album,
        "artist": artist,
        "duration": duration,
        "genre": genre,
        "file_path": file_path
    })

    save_songs(data)
    print("🎵 Song '{}' added successfully!\n".format(title))

def view_songs():
    data = load_songs()
    if not data["songs"]:
        print("No songs available yet! 😢\n")
        return

    print("\nAvailable Songs:")
    for i, song in enumerate(data["songs"]):
        print("{}. {} - {} | {} • {} ({})".format(
            i+1,
            song["title"],
            song["album"],
            song["artist"],
            song["duration"],
            song["genre"]
        ))
    print("")

def play_song():
    data = load_songs()

    if not data["songs"]:
        print("No songs to play! 😢\n")
        return

    view_songs()

    try:
        choice = int(input("Select song number to play: ")) - 1
        if choice < 0 or choice >= len(data["songs"]):
            print("Invalid selection 😅\n")
            return
    except ValueError:
        print("Please type a number 💕\n")
        return

    song = data["songs"][choice]
    print("🎶 Playing '{}' by {} ({})".format(song["title"], song["artist"], song["duration"]))
    playsound(song["file_path"])

# ------------------- Search -------------------
def search_song():
    query = input("Search songs: ").lower()
    data = load_songs()

    results = [
        song for song in data["songs"]
        if query in song["title"].lower()
        or query in song["album"].lower()
        or query in song["artist"].lower()
        or query in song["genre"].lower()
    ]

    if not results:
        print("No matching songs found 😢\n")
        return

    print("\nSearch Results:")
    for i, song in enumerate(results):
        print("{}. {} - {} | {} • {} ({})".format(
            i+1,
            song["title"],
            song["album"],
            song["artist"],
            song["duration"],
            song["genre"]
        ))
    print("")

# ------------------- Shuffle -------------------
def shuffle_play():
    data = load_songs()

    if not data["songs"]:
        print("No songs to shuffle 😢\n")
        return

    shuffled = data["songs"][:]
    random.shuffle(shuffled)

    print("🔀 Shuffling {} songs...".format(len(shuffled)))

    for song in shuffled:
        print("🎶 Playing '{}' by {} ({})".format(song["title"], song["artist"], song["duration"]))
        playsound(song["file_path"])

# ------------------- Playlists -------------------
def add_playlist():
    name = input("Playlist name: ")
    data = load_songs()

    if name in data["playlists"]:
        print("Playlist already exists! 😅\n")
        return

    data["playlists"][name] = []
    save_songs(data)

    print("✅ Playlist '{}' created!\n".format(name))

def add_song_to_playlist():
    data = load_songs()

    if not data["playlists"]:
        print("No playlists available 😢\n")
        return

    print("Available playlists:")
    for playlist in data["playlists"]:
        print("- {}".format(playlist))

    playlist = input("Choose playlist: ")

    if playlist not in data["playlists"]:
        print("Playlist does not exist 😅\n")
        return

    view_songs()

    try:
        choice = int(input("Select song number to add: ")) - 1
        if choice < 0 or choice >= len(data["songs"]):
            print("Invalid selection 😅")
            return
    except ValueError:
        print("Please type a number 💕")
        return

    song_title = data["songs"][choice]["title"]

    data["playlists"][playlist].append(song_title)
    save_songs(data)

    print("🎵 '{}' added to playlist '{}'!\n".format(song_title, playlist))

def play_playlist():
    data = load_songs()

    if not data["playlists"]:
        print("No playlists available 😢\n")
        return

    print("Playlists:")
    for playlist in data["playlists"]:
        print("- {}".format(playlist))

    playlist = input("Choose playlist: ")

    if playlist not in data["playlists"]:
        print("Playlist does not exist 😅\n")
        return

    print("🎶 Playing playlist: {}".format(playlist))

    for title in data["playlists"][playlist]:
        for song in data["songs"]:
            if song["title"] == title:
                print("🎵 {} - {} ({})".format(song["title"], song["artist"], song["duration"]))
                playsound(song["file_path"])

# ------------------- Queue System -------------------
def add_to_queue():
    data = load_songs()
    view_songs()

    try:
        choice = int(input("Select song to add to queue: ")) - 1
        if choice < 0 or choice >= len(data["songs"]):
            print("Invalid selection 😅\n")
            return
    except ValueError:
        print("Please type a number 💕\n")
        return

    song = data["songs"][choice]
    queue.append(song)

    print("🎵 '{}' added to queue!\n".format(song["title"]))

def play_queue():
    global queue

    if not queue:
        print("Queue is empty 😢\n")
        return

    print("▶️ Playing queue ({} songs)...".format(len(queue)))

    while queue:
        song = queue.pop(0)
        print("🎶 {} - {} ({})".format(song["title"], song["artist"], song["duration"]))
        playsound(song["file_path"])

# ------------------- Main Menu -------------------
def menu():
    while True:
        print("\n--- Terminal Music Player ❤️ ---")
        print("1. Add Song")
        print("2. View Songs")
        print("3. Play Song")
        print("4. Search Songs")
        print("5. Shuffle Play")
        print("6. Create Playlist")
        print("7. Add Song to Playlist")
        print("8. Play Playlist")
        print("9. Add to Queue")
        print("10. Play Queue")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1": add_song()
        elif choice == "2": view_songs()
        elif choice == "3": play_song()
        elif choice == "4": search_song()
        elif choice == "5": shuffle_play()
        elif choice == "6": add_playlist()
        elif choice == "7": add_song_to_playlist()
        elif choice == "8": play_playlist()
        elif choice == "9": add_to_queue()
        elif choice == "10": play_queue()
        elif choice == "0":
            print("Goodbye, sweetheart ❤️")
            break
        else:
            print("Invalid option 😅 Try again!")

if __name__ == "__main__":
    menu()
