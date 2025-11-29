import json
import random
import os
import shutil

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
# UI Helpers (Boxed header, tabular menus)
# ===========================

def terminal_width(default=80):
    try:
        cols = shutil.get_terminal_size().columns
        return max(60, cols)
    except Exception:
        return default

def print_boxed(title):
    w = terminal_width()
    line = "+" + "-" * (w - 2) + "+"
    print(line)
    print("|" + title.center(w - 2) + "|")
    print(line)

def print_menu(menu_items):
    # menu_items: list of (key, description)
    w = terminal_width()
    key_col = 6
    desc_col = w - key_col - 7
    top = "+" + "-" * (key_col + desc_col + 5) + "+"
    row = "+" + "-" * (key_col + 2) + "+" + "-" * (desc_col + 2) + "+"
    print(top)
    print("| {:^{k}} | {:^{d}} |".format("Key", "Action", k=key_col, d=desc_col))
    print(row)
    for k, desc in menu_items:
        print("| {:^{k}} | {:<{d}} |".format(k, desc, k=key_col, d=desc_col))
    print(row)

def prompt_choice(prompt_text="Choose"): 
    return input(f"{prompt_text} (or H for Help): ").strip()

def show_help():
    print_boxed("HELP")
    print("- Input the number or letter on the left to choose an action.")
    print("- You can press 'H' or '?' anytime to view this help screen.")
    print("- When adding songs, provide the requested fields; durations like '03:25' are recommended.")
    print()


# ===========================
# Display Playlist (ASCII Table)
# ===========================

def display_playlist(name, songs):
    title_w = 30
    artist_w = 20
    album_w = 24
    duration_w = 10

    total_w = title_w + artist_w + album_w + duration_w + 11

    def trim(text, max_w):
        text = str(text)
        return text[:max_w-3] + "..." if len(text) > max_w else text
    
    w = terminal_width()
    key_col = 6
    desc_col = w - key_col - 7
    top = "+" + "-" * (key_col + desc_col + 5) + "+"
    row = "+" + "-" * (key_col + 2) + "+" + "-" * (desc_col + 2) + "+"

    print(top)
    print("|{:^{width}}|".format(f"Playlist: {name}", width=total_w))
    print(row)

    print("| {:<{}} | {:<{}} | {:<{}} | {:>{}} |".format(
        "Title", title_w,
        "Artist", artist_w,
        "Album", album_w,
        "Duration", duration_w
    ))
    print(row)

    if len(songs) == 0:
        for _ in range(4):
            print("| {:<{}} | {:<{}} | {:<{}} | {:>{}} |".format(
                "", title_w, "", artist_w, "", album_w, "00:00", duration_w
            ))
    else:
        for s in songs:
            print("| {:<{}} | {:<{}} | {:<{}} | {:>{}} |".format(
                trim(s.get("title", ""), title_w), title_w,
                trim(s.get("artist", ""), artist_w), artist_w,
                trim(s.get("album", ""), album_w), album_w,
                s.get("duration","00:00"), duration_w
            ))

    print(row)

# sort
def sort_playlist(songs, mode):
    pass





    # if not songs:
    #     print("Nothing to sort.\n")
    #     return
    
    # if mode == "DURATION":
    #     songs.sort(key=lambda s: sum(int(x) * 60 ** i for i, x in enumerate(reversed(s.get("duration", "0:0").split(":")))))
    # else:
    #     key = mode.lower()
    #     songs.sort(key=lambda s: s.get(key,"").lower())

    # print(f"✅ Sorted by {mode}!\n")


# ===========================
# Core Features (Add/View/Search/Shuffle)
# ===========================

def add_song(library):
    print_boxed("Add Song")
    title = input("Title: ").strip()
    artist = input("Artist: ").strip()
    album = input("Album: ").strip()
    duration = input("Duration (MM:SS): ").strip()
    genre = input("Genre: ").strip()

    new_song = {
        "title": title,
        "artist": artist,
        "album": album,
        "duration": duration,
        "genre": genre
    }

    library.append(new_song)
    print(f"\n🎵 Song '{title}' added successfully!\n")

def view_songs(library):
    print_boxed("Song Library")

    if len(library) == 0:
        print("No songs yet. Use option 1 to add songs.\n")
        return

    while True:
        display_playlist("Library View", library)
        sort_menu = [
            ("1", "Sort by Title"),
            ("2", "Sort by Artist"),
            ("3", "Sort by Album"),
            ("4", "Sort by Duration"),
            ("B", "Back")
        ]
        print_menu(sort_menu)
        choice = prompt_choice("Sort Library")

        c = choice.upper()
        if c == "1":
            sort_playlist(library, "TITLE")
        elif c == "2":
            sort_playlist(library, "ARTIST")
        elif c == "3":
            sort_playlist(library, "ALBUM")
        elif c == "4":
            sort_playlist(library, "DURATION")
        elif c == "B":
            return
        elif c in ("H","?"):
            show_help()
        else:
            print("Invalid option.\n")

def search_song(library):
    print_boxed("Search Songs")
    keyword = input("Search (title/artist/album): ").lower().strip()
    
    results = [
        s for s in library if 
        keyword in s.get("title", "").lower() or
        keyword in s.get("artist", "").lower() or
        keyword in s.get("album", "").lower()
    ]

    if not results:
        print("No results found.\n")
        return

    print_boxed("Search Results")
    display_playlist("Matches", results)
    print()

def shuffle_play(library):
    if not library:
        print("No songs to shuffle.\n")
        return

    shuffled = library[:]
    random.shuffle(shuffled)
    first = shuffled[0]
    print_boxed("Shuffle Play")
    print(f"🔀 Shuffling {len(shuffled)} songs...")
    print(f"🎶 Now playing: {first.get('title','')} — {first.get('artist','')}\n")


# ===========================
# Playlist Management
# ===========================

def create_playlist(playlists):
    print_boxed("Create Playlist")
    name = input("Playlist name: ").strip()

    if not name:
        print("Name cannot be empty.\n")
        return
    if name in playlists:
        print("Playlist already exists.\n")
        return
    playlists[name] = []
    print(f"✅ Playlist '{name}' created!\n")

def add_to_playlist(library, playlists):
    print_boxed("Add to Playlist")
    playlist = input("Playlist name: ").strip()
    if playlist not in playlists:
        print("Playlist does not exist.\n")
        return
    title = input("Song title to add: ").strip()
    for s in library:
        if s.get("title", "").lower() == title.lower():
            playlists[playlist].append(s)
            print(f"🎵 '{title}' added to playlist '{playlist}'\n")
            return
    print("Song not found.\n")

def view_playlist(playlists):
    print_boxed("View Playlist")
    name = input("Playlist name: ").strip()
    if name not in playlists:
        print("Playlist does not exist.\n")
        return
    
    songs = playlists[name]
    while True:
        print_boxed(f"Playlist: {name}")
        display_playlist(name, songs)

        sort_menu = [
            ("1", "Sort by Title"),
            ("2", "Sort by Artist"),
            ("3", "Sort by Album"),
            ("4", "Sort by Duration"),
            ("B", "Back")
        ]
        print_menu(sort_menu)
        choice = prompt_choice("Sort Playlist")

        c = choice.upper()
        if c == "1":
            sort_playlist(songs, "TITLE")
        elif c == "2":
            sort_playlist(songs, "ARTIST")
        elif c == "3":
            sort_playlist(songs, "ALBUM")
        elif c == "4":
            sort_playlist(songs, "DURATION")
        elif c == "B":
            return
        elif c in ("H","?"):
            show_help()
        else:
            print("Invalid option.\n")

# ===========================
# Queue System
# ===========================

def queue_add(queue, library):
    title = input("Song title to queue: ").strip().lower()
    for s in library:
        if s.get("title","").lower() == title:
            queue.append(s)
            print(f"🎵 '{s.get('title','')}' added to queue!\n")
            return
    print("Song not found.\n")

def play_queue(queue):
    if not queue:
        print("Queue is empty.\n")
        return
    print_boxed("Play Queue")
    print(f"▶️ Playing queue ({len(queue)} songs):")
    for s in queue:
        print(f"🎶 {s.get('title','')} — {s.get('artist','')}")
    print()
    queue.clear()


# ===========================
# MAIN PROGRAM LOOP
# ===========================

def main():
    library = load_data("library.json")
    playlists = load_data("playlists.json")
    queue = []

    menu = [
        ("1", "Add Song"),
        ("2", "View Songs"),
        ("3", "Search Song"),
        ("4", "Shuffle Play"),
        ("5", "Create Playlist"),
        ("6", "Add to Playlist"),
        ("7", "View / Sort Playlist"),
        ("8", "Add to Queue"),
        ("9", "Play Queue"),
        ("0", "Save & Exit"),
        ("H", "Help")
    ]

    while True:
        print_boxed("Terminal Music Player")
        print_menu(menu)

        choice = prompt_choice()
        if not choice:
            print("No input. Please choose an option.\n")
            continue

        c = choice.strip().upper()
        if c in ("H", "?"):
            show_help()
            continue

        if c == "1":
            add_song(library)
        elif c == "2":
            view_songs(library)
        elif c == "3":
            search_song(library)
        elif c == "4":
            shuffle_play(library)
        elif c == "5":
            create_playlist(playlists)
        elif c == "6":
            add_to_playlist(library, playlists)
        elif c == "7":
            view_playlist(playlists)
        elif c == "8":
            queue_add(queue, library)
        elif c == "9":
            play_queue(queue)
        elif c == "0":
            save_data("library.json", library)
            save_data("playlists.json", playlists)
            print("\nGoodbye.\n")
            break
        else:
            print("Invalid choice. Press H for help.\n")


if __name__ == '__main__':
    main()
