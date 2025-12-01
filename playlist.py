from ui import print_boxed, display_tracks, print_menu, prompt_choice, show_help, terminal_width
from sorting import sort_tracks

class Playlist:
    def create_playlist(playlists):
        print_boxed("Create Playlist")
        name = input("Playlist name: ").strip()

        if not name:
            print("❌ Playlist name cannot be empty.")
            return
        if name in playlists:
            print("❌ Playlist already exists.\n")
            return
        playlists[name] = []
        print(f"✅ Playlist '{name}' created!\n")

    def add_to_playlist(library, playlists):
        print_boxed("Add to Playlist")
        Playlist.show_playlists_only(playlists)
        playlist = input("Playlist name: ").strip()
        
        if playlist not in playlists:
            print("❌ Playlist does not exist.\n")
            return
        display_tracks("Library View", library)
        title = input("Song title to add: ").strip()

        found = None
        for s in library:
            if s.get("title", "").lower() == title.lower():
                found = s
                break

        if not found:
            print("❌ Song not found in library.\n")
            return

        for s in playlists[playlist]:
            if (s.get("title", "").lower() == found.get("title", "").lower() and
                s.get("artist", "").lower() == found.get("artist", "").lower()):
                print(f"\n❌ Song '{found.get('title','')}' by '{found.get('artist','')}' is already in the playlist!\n")
                return

        playlists[playlist].append(found.copy())
        print(f"\n🎵 Added: {found.get('title','')} → {playlist}\n")

    def show_playlists_only(pl):
        keys = list(pl.keys())
        if not keys:
            print("No playlists available.")
            return

        page_size = 10
        total = len(keys)
        total_pages = (total + page_size - 1) // page_size
        page = 1

        while True:
            start = (page - 1) * page_size
            end = min(start + page_size, total)
            for idx in range(start, end):
                print(f"{idx+1}. {keys[idx]}")

            w = terminal_width()
            key_col = 6
            desc_col = w - key_col - 7
            top = "+" + "-" * (key_col + desc_col + 5) + "+"
            row = "+" + "-" * (key_col + 2) + "-" + "-" * (desc_col + 2) + "+"
            print(row)
            if total_pages <= 1:
                break
            choice = input(f"Page {page}/{total_pages} - press 'n' for next, 'p' for previous, or Enter to continue: ").strip().lower()
            if choice == 'n' and page < total_pages:
                page += 1
                continue
            elif choice == 'p' and page > 1:
                page -= 1
                continue
            else:
                break

    def view_playlist(playlists): 
        print_boxed("View a Playlist")
        Playlist.show_playlists_only(playlists)
        name = input("Playlist name: ").strip()
        if name not in playlists:
            print("❌ Playlist does not exist.\n")
            return
        
        songs = playlists[name]
        while True:
            print_boxed(f"Playlist: {name}")
            display_tracks(name, songs)

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
                sort_tracks(songs, "title")
            elif c == "2":
                sort_tracks(songs, "artist")
            elif c == "3":
                sort_tracks(songs, "album")
            elif c == "4":
                sort_tracks(songs, "duration")

            elif c == "B":
                return
            elif c in ("H","?"):
                show_help()
            else:
                print("❌ Invalid option.\n")