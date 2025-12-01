from data_storage import load_data, save_data
from ui import print_boxed, print_menu, prompt_choice, show_help
from library import add_song, view_songs, delete_song, search_song
from playlist import Playlist
from queue import queue_add, shuffle_queue, play_queue, view_queue

def main():
    library = load_data("library.json")
    playlists = load_data("playlists.json")
    queue = load_data("queue.json")

    menu = [
        ("1", "Library"),
        ("2", "Playlist"),
        ("3", "Music Queue"),
        ("4", "Save Changes"),
        ("5", "Save & Exit"),
        ("H", "Help"),
    ]

    while True:
        print_boxed("Terminal Music Player")
        print_menu(menu)

        choice = prompt_choice()
        if not choice:
            print("❌ No input. Please choose an option.\n")
            continue

        c = choice.strip().upper()
        if c in ("H", "?"):
            show_help()
            continue

        if c == "1":
            l_menu = [
                ("1", "Add Song"),
                ("2", "Delete Songs"),
                ("3", "View Songs"),
                ("4", "Search Songs"),
                ("B", "Back"),
                ("H", "Help")
            ]

            while True:
                print_boxed("LIBRARY")
                print_menu(l_menu)

                choice = prompt_choice()
                if not choice:
                    print("❌ No input. Please choose an option.\n")
                    continue

                c = choice.strip().upper()
                if c in ("H", "?"):
                    show_help()
                    continue

                if c == "1":
                    add_song(library)
                elif c == "2":
                    library = delete_song(library)
                    # save_data(library)   # if you have a save function
                elif c == "3":
                    view_songs(library)
                elif c == "4":
                    search_song(library)
                elif c == "B":
                    break
                else:
                    print("❌ Invalid choice. Press H for help.\n")

        elif c == "2":
            p_menu = [
                ("1", "Create Playlist"),
                ("2", "Add to Playlist"),
                ("3", "View a Playlist"),
                ("B", "Back"),
                ("H", "Help")
            ]
                
            while True:
                print_boxed("PLAYLIST")
                print_menu(p_menu)

                choice = prompt_choice()
                if not choice:
                    print("❌ No input. Please choose an option.\n")
                    continue

                c = choice.strip().upper()
                if c in ("H", "?"):
                    show_help()
                    continue

                if c == "1":
                    Playlist.create_playlist(playlists)
                elif c == "2":
                    Playlist.add_to_playlist(library, playlists)
                elif c == "3":
                    Playlist.view_playlist(playlists)
                elif c == "B":
                    break
                else:
                    print("❌ Invalid choice. Press H for help.\n")

        elif c == "3":
            q_menu = [
                ("1", "Play Queue"),
                ("2", "Add to Queue"),
                ("3", "View Queue"),
                ("4", "Shuffle Queue"),
                ("B", "Back"),
                ("H", "Help")
            ]

            while True:
                print_boxed("MUSIC QUEUE")
                print_menu(q_menu)

                choice = prompt_choice()
                if not choice:
                    print("❌ No input. Please choose an option.\n")
                    continue

                c = choice.strip().upper()
                if c in ("H", "?"):
                    show_help()
                    continue

                if c == "1":
                    play_queue(queue)
                elif c == "2":
                    queue_add(queue, library)
                elif c == "3":
                    view_queue(queue)
                elif c == "4":
                    shuffle_queue(queue)
                elif c == "b":
                    break
                else:
                    print("❌ Invalid choice. Press H for help.\n")

        elif c == "4":
            save_data("library.json", library)
            save_data("playlists.json", playlists)
            save_data("queue.json", queue)
            print("✅ Changes have been saved.")

        elif c == "5":
            save_data("library.json", library)
            save_data("playlists.json", playlists)
            save_data("queue.json", queue)
            print("✅ Changes have been saved.")
            print("\nThank you. Goodbye.\n")
            break

        else:
            print("❌ Invalid choice. Press H for help.\n")


if __name__ == '__main__':
    main()
