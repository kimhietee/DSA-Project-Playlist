from ui import print_boxed, display_tracks, print_menu, prompt_choice, show_help
from sorting import sort_tracks 
import random

def queue_add(queue, library):
    title = input("Song title to queue: ").strip().lower()
    for s in library:
        if s.get("title","").lower() == title:
            queue.append(s)
            print(f"🎵 '{s.get('title','')}' added to queue!\n")
            return
    print("❌ Song not found.\n")

def play_queue(queue):
    if not queue:
        print("❌ Queue is empty.\n")
        return
    print_boxed("Play Queue")
    print(f"▶️ Playing queue ({len(queue)} songs):")
    for s in queue:
        print(f"🎶 {s.get('title','')} — {s.get('artist','')}")
    print()
    queue.clear()

def shuffle_queue(queue):
    random.shuffle(queue)
    print("🔀 Queue shuffled!\n")

def view_queue(queue):
    print_boxed("Queue")

    if len(queue) == 0:
        print("❌ No songs yet. Use option 1 to add songs.\n")
        return

    while True:
        display_tracks("Queue View", queue)
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
            sort_tracks(queue, "title")
        elif c == "2":
            sort_tracks(queue, "artist")
        elif c == "3":
            sort_tracks(queue, "album")
        elif c == "4":
            sort_tracks(queue, "duration")
        elif c == "B":
            return
        elif c in ("H","?"):
            show_help()
        else:
            print("Invalid option.\n")
