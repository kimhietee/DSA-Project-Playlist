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
'''
sort by:
title
artist
album
duration

'''

def sort_playlist(songs, mode):
    pass


class TimSort:
    #class vars
    minRUN = 32
    
    @staticmethod
    def calcMinRun(n):
        r = 0
        while n >= TimSort.minRUN:
            r |= n & 1
            n >>= 1
        return n + r

    # Insertion sort for small ranges
    @staticmethod
    def insertionSort(arr, left, right):
        for i in range(left + 1, right + 1):
            key = arr[i]
            j = i - 1
            while j >= left and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key

    # Merge two sorted subarrays [l..m] and [m+1..r]
    @staticmethod
    def merge(arr, l, m, r):
        left = arr[l:m+1]
        right = arr[m+1:r+1]
        i = j = 0
        k = l
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1

    # Detect ascending/descending run starting at index "start"
    @staticmethod
    def findRun(arr, start, n):
        end = start + 1
        if end == n: return end
        if arr[end] < arr[start]:
            # descending
            while end < n and arr[end] < arr[end - 1]:
                end += 1
            arr[start:end] = reversed(arr[start:end])
        else:
            # ascending
            while end < n and arr[end] >= arr[end - 1]:
                end += 1
        return end

    # Timsort main function
    @staticmethod
    def timsort(arr):
        n = len(arr)
        minRun = TimSort.calcMinRun(n)
        runs = []

        i = 0
        while i < n:
            runEnd = TimSort.findRun(arr, i, n)
            runLen = runEnd - i

            if runLen < minRun:
                end = min(i + minRun, n)
                TimSort.insertionSort(arr, i, end - 1)
                runEnd = end

            runs.append((i, runEnd))
            i = runEnd

            while len(runs) > 1:
                l1, r1 = runs[-2]
                l2, r2 = runs[-1]
                len1, len2 = r1 - l1, r2 - l2
                if len1 <= len2:
                    TimSort.merge(arr, l1, r1 - 1, r2 - 1)
                    runs.pop()
                    runs[-1] = (l1, r2)
                else:
                    break

        while len(runs) > 1:
            l1, r1 = runs[-2]
            l2, r2 = runs[-1]
            TimSort.merge(arr, l1, r1 - 1, r2 - 1)
            runs.pop()
            runs[-1] = (l1, r2)


# sort_playlist = TimSort().timsort

def sort_playlist(songs, mode="title"):
    if not songs:
        print("Nothing to sort.\n")
        return

    mode = mode.lower()

    # Duration: convert MM:SS → seconds
    if mode == "duration":
        def key_func(s):
            mm, ss = s.get("duration", "0:0").split(":")
            return int(mm) * 60 + int(ss)
    else:
        # title / artist / album
        key_func = lambda s: s.get(mode, "").lower()

    # Build sortable array for your TimSort
    sortable = [(key_func(s), i, s) for i, s in enumerate(songs)]

    TimSort().timsort(sortable)

    # write back sorted songs
    for i in range(len(songs)):
        songs[i] = sortable[i][2]


# def sort_playlist(songs, mode):
#     if not songs:
#         print("Nothing to sort.\n")
#         return
    
#     # if mode == "DURATION":
#     #     songs.sort(key=lambda s: sum(int(x) * 60 ** i for i, x in enumerate(reversed(s.get("duration", "0:0").split(":")))))
#     if mode == "DURATION":
#         # convert MM:SS to total seconds
#         songs.sort(key=lambda s: sum(int(x) * 60 ** i 
#                                      for i, x in enumerate(reversed(s.get("duration", "0:0").split(":")))))
#     else:
#         key = mode.lower()
#         songs.sort(key=lambda s: s.get(key,"").lower())

#     print(f"✅ Sorted by {mode}!\n")


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
            sort_playlist(library, "title")
        elif c == "2":
            sort_playlist(library, "artist")
        elif c == "3":
            sort_playlist(library, "album")
        elif c == "4":
            sort_playlist(library, "duration")
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
            sort_playlist(songs, "title")
        elif c == "2":
            sort_playlist(songs, "artist")
        elif c == "3":
            sort_playlist(songs, "album")
        elif c == "4":
            sort_playlist(songs, "duration")

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
