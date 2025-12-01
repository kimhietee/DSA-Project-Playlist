from ui import print_boxed, print_menu, prompt_choice, show_help
from sorting import sort_tracks
from ui import display_tracks

def add_song(library):
    print_boxed("Add Song")
    def get_input(label):
        while True:
            value = input(f"{label}: ").strip()
            if value == "":
                print(f"❌ {label} cannot be empty.\n")
            else:
                return value

    title = get_input("Title")
    artist = get_input("Artist")
    album = get_input("Album")
    duration = get_input("Duration (MM:SS)")
    genre = get_input("Genre")

    for song in library:
        if song["title"].lower() == title.lower() and song["artist"].lower() == artist.lower():
            print(f"\n❌ Duplicate song detected! '{title}' by '{artist}' already exists.\n")
            return
        
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
        print("❌ No songs yet. Use option 1 to add songs.\n")
        return

    while True:
        display_tracks("Library View", library)
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
            sort_tracks(library, "title")
        elif c == "2":
            sort_tracks(library, "artist")
        elif c == "3":
            sort_tracks(library, "album")
        elif c == "4":
            sort_tracks(library, "duration")
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
        print("❌ No results found.\n")
        return

    print_boxed("Search Results")
    display_tracks("Matches", results)
    print()

def delete_song(library):
    if not library:
        print("❌ Library is empty.")
        return library

    title = input("Enter track title to delete: ").strip().lower()

    matches = [t for t in library if t["title"].lower() == title]

    if not matches:
        print("❌ No track with that title found.")
        return library

    if len(matches) == 1:
        library.remove(matches[0])
        print("✅ Track deleted successfully.")
        return library

    print("\nMultiple tracks found with the same title:")
    for i, t in enumerate(matches, 1):
        print(f"[{i}] {t['title']} – {t['artist']} ({t['duration']})")

    try:
        choice = int(input("Select which track to delete: "))
        if 1 <= choice <= len(matches):
            library.remove(matches[choice - 1])
            print("✅ Track deleted successfully.")
        else:
            print("❌ Invalid option.")
    except:
        print("❌ Invalid input.")

    return library