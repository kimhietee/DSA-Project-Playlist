import os
import time
from math import ceil

from track import Track
from library import MusicLibrary
from playlist import Playlist
from queue_system import MusicQueue
from utils.duration import seconds_to_mmss
from utils.file_manager import FileManager

#File Paths---------------------------
DATA_DIR = "data"
TRACKS_FILE = os.path.join(DATA_DIR, "tracks.json")
PLAYLISTS_FILE = os.path.join(DATA_DIR, "playlists.json")
QUEUE_FILE = os.path.join(DATA_DIR, "queue.json")


#Setup------------------------------------
def ensure_data_files():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(TRACKS_FILE):
        FileManager.save(TRACKS_FILE, [])

    if not os.path.exists(PLAYLISTS_FILE):
        FileManager.save(PLAYLISTS_FILE, {})

    if not os.path.exists(QUEUE_FILE):
        FileManager.save(QUEUE_FILE, {})


def pause(msg="Press Enter to continue..."):
    input("\n{}".format(msg))


#PLAYLIST MANAGER----------------------------------
class PlaylistManager:
    def __init__(self, file_path=PLAYLISTS_FILE):
        self.file_path = file_path
        self.load()

    def load(self):
        data = FileManager.load(self.file_path)
        if not isinstance(data, dict):
            data = {}
        self.data = data

    def save(self):
        FileManager.save(self.file_path, self.data)

    def list_playlist_names(self):
        return list(self.data.keys())

    def create_playlist(self, name):
        if name in self.data:
            return False
        self.data[name] = []
        self.save()
        return True

    def delete_playlist(self, name):
        if name in self.data:
            del self.data[name]
            self.save()
            return True
        return False

    def add_track_to_playlist(self, playlist_name, track):
        if playlist_name not in self.data:
            return False, "Playlist does not exist."

        for t in self.data[playlist_name]:
            if t["title"] == track.title and t["artist"] == track.artist and t["duration"] == track.duration:
                return False, "Track already in playlist."

        self.data[playlist_name].append(track.to_dict())
        self.save()
        return True, "Track added."

    def get_playlist_tracks(self, playlist_name):
        return [Track.from_dict(t) for t in self.data.get(playlist_name, [])]

    def playlist_total_duration_seconds(self, playlist_name):
        total = 0
        for t in self.data.get(playlist_name, []):
            m, s = map(int, t["duration"].split(":"))
            total += m * 60 + s
        return total


# ============================
#      DISPLAY HELPERS
# ============================
def display_tracks(tracks, page=1, per_page=10):
    total = len(tracks)
    if total == 0:
        print("(No tracks found)\n")
        return

    pages = ceil(total / per_page)
    start = (page - 1) * per_page
    end = min(start + per_page, total)

    for i in range(start, end):
        t = tracks[i]
        print("{}. {} – {} ({})".format(i + 1, t.title, t.display_artists(), t.duration))

    print("\n<Page {} of {}>".format(page, pages))


# ============================
#       LIBRARY MENU
# ============================
def library_menu(lib, pm):
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("=== MUSIC LIBRARY ===\n")
        print("[1] List Tracks")
        print("[2] Add Track")
        print("[3] Search Track")
        print("[4] Add Track to Playlist")
        print("[5] Back")

        choice = input("\nChoose: ").strip()

        # --- List Tracks ---
        if choice == "1":
            os.system("cls" if os.name == "nt" else "clear")
            print("=== TRACK LIST ===\n")
            display_tracks(lib.list_tracks(), 1)
            pause()

        # --- Add Track ---
        elif choice == "2":
            os.system("cls" if os.name == "nt" else "clear")
            print("=== ADD NEW TRACK ===\n")

            title = input("Title: ")
            artist = input("Main Artist: ")
            additional = input("Additional Artists (comma separated): ")
            album = input("Album: ")
            duration = input("Duration (mm:ss): ")

            additional_list = [a.strip() for a in additional.split(",")] if additional else []

            try:
                m, s = map(int, duration.split(":"))
            except:
                print("\nInvalid duration format.")
                pause()
                continue

            track = Track(title, artist, additional_list, album, "{:02d}:{:02d}".format(m, s))
            lib.add_track(track)

            print("\nTrack '{}' added successfully.".format(title))
            pause()

        # --- Search Track ---
        elif choice == "3":
            keyword = input("\nEnter keyword: ")
            matches = [t for t in lib.list_tracks() if keyword.lower() in t.title.lower()]

            print("\n=== SEARCH RESULTS ===\n")
            display_tracks(matches, 1)
            pause()

        # --- Add Track to Playlist ---
        elif choice == "4":
            keyword = input("\nSearch for track: ")
            found = [t for t in lib.list_tracks() if keyword.lower() in t.title.lower()]

            if not found:
                print("\nNo tracks found.")
                pause()
                continue

            print("\nSelect a track:")
            for i, t in enumerate(found, 1):
                print("{}. {} – {} ({})".format(i, t.title, t.artist, t.duration))

            track_choice = input("\nChoose track number: ")
            if not track_choice.isdigit():
                pause("\nInvalid.")
                continue

            track = found[int(track_choice) - 1]

            playlists = pm.list_playlist_names()
            print("\nChoose playlist:")
            for i, name in enumerate(playlists, 1):
                print("[{}] {}".format(i, name))

            p_choice = input("\nPlaylist number: ")
            if not p_choice.isdigit():
                pause("Invalid.")
                continue

            playlist_name = playlists[int(p_choice) - 1]
            ok, msg = pm.add_track_to_playlist(playlist_name, track)

            print("\n{}".format(msg))
            pause()

        else:
            break


# ============================
#      SINGLE PLAYLIST MENU
# ============================
def view_single_playlist(pm, name, lib, queue):
    tracks = pm.get_playlist_tracks(name)
    per_page = 10
    page = 1

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("=== PLAYLIST: {} ===\n".format(name))

        display_tracks(tracks, page)

        total_dur = seconds_to_mmss(pm.playlist_total_duration_seconds(name))
        print("\nTotal Duration: {}\n".format(total_dur))

        print("[a] Add Track")
        print("[r] Remove Track")
        print("[p] Play Playlist")
        print("[n] Next Page")
        print("[b] Back")

        choice = input("\nChoose: ").strip().lower()

        if choice == "a":
            keyword = input("\nSearch track title: ")
            found = [t for t in lib.list_tracks() if keyword.lower() in t.title.lower()]

            if not found:
                print("\nNo results.")
                pause()
                continue

            print("\nSelect track to add:")
            for i, t in enumerate(found, 1):
                print("{}. {} – {}".format(i, t.title, t.artist))

            pick = input("\nChoose number: ")
            if pick.isdigit() and 1 <= int(pick) <= len(found):
                ok, msg = pm.add_track_to_playlist(name, found[int(pick) - 1])
                print("\n{}".format(msg))
            pause()

            tracks = pm.get_playlist_tracks(name)

        elif choice == "r":
            num = input("\nTrack number to remove: ")
            if num.isdigit():
                idx = int(num) - 1
                if 0 <= idx < len(tracks):
                    td = tracks[idx].to_dict()
                    for i, item in enumerate(pm.data[name]):
                        if item["title"] == td["title"]:
                            pm.data[name].pop(i)
                            pm.save()
                            print("\nTrack removed.")
                            break
                    tracks = pm.get_playlist_tracks(name)
                else:
                    print("\nInvalid.")
            pause()

        elif choice == "p":
            queue.set_queue(tracks)
            print("\nQueue loaded from playlist.")
            pause()
            queue_menu(queue)
            break

        elif choice == "n":
            page += 1

        else:
            break


# ============================
#      PLAYLISTS MENU
# ============================
def playlists_menu(pm, lib):
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("=== PLAYLISTS ===\n")

        names = pm.list_playlist_names()

        if names:
            for i, name in enumerate(names, 1):
                dur = seconds_to_mmss(pm.playlist_total_duration_seconds(name))
                print("[{}] {} — {}".format(i, name, dur))
        else:
            print("(No playlists yet)")

        print("\n[c] Create Playlist")
        print("[v] View Playlist")
        print("[d] Delete Playlist")
        print("[b] Back")

        choice = input("\nChoose: ").strip().lower()

        if choice == "c":
            n = input("\nEnter playlist name: ")
            ok = pm.create_playlist(n)
            print("\nCreated." if ok else "\nPlaylist exists.")
            pause()

        elif choice == "v":
            num = input("\nPlaylist number: ")
            if num.isdigit() and 1 <= int(num) <= len(names):
                view_single_playlist(pm, names[int(num) - 1], lib, queue)
            else:
                print("\nInvalid.")
                pause()

        elif choice == "d":
            n = input("\nName to delete: ")
            print("\nDeleted." if pm.delete_playlist(n) else "\nNot found.")
            pause()

        else:
            break


# ============================
#          QUEUE MENU
# ============================
def queue_menu(queue):
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("=== QUEUE ===\n")

        if not queue.tracks:
            print("(Queue empty)\n")
        else:
            cur = queue.current()
            print("Now Playing: {} – {} ({})\n".format(
                cur["title"], cur["artist"], cur["duration"]
            ))
            print("Repeat: {}".format("ON" if queue.repeat else "OFF"))
            print("Shuffle: {}\n".format("ON" if queue.shuffled else "OFF"))

        print("[1] Play")
        print("[2] Next")
        print("[3] Previous")
        print("[4] Toggle Repeat")
        print("[5] Toggle Shuffle")
        print("[6] Add Track")
        print("[7] Add Playlist")
        print("[8] Clear Queue")
        print("[9] Back")

        choice = input("\nChoose: ")

        if choice == "1":
            print("\nPlaying...\n")
            time.sleep(0.5)
            pause()

        elif choice == "2":
            nxt = queue.next()
            if nxt:
                print("\nNow: {} – {}".format(nxt["title"], nxt["artist"]))
            else:
                print("\nEnd of queue.")
            pause()

        elif choice == "3":
            prev = queue.previous()
            if prev:
                print("\nNow: {} – {}".format(prev["title"], prev["artist"]))
            else:
                print("\nStart of queue.")
            pause()

        elif choice == "4":
            queue.repeat = not queue.repeat
            queue.save()
            print("\nRepeat toggled.")
            pause()

        elif choice == "5":
            queue.shuffle()
            print("\nShuffle toggled.")
            pause()

        elif choice == "6":
            keyword = input("\nSearch track: ")
            found = [t for t in lib.list_tracks() if keyword.lower() in t.title.lower()]

            if not found:
                print("\nNothing found.")
                pause()
                continue

            print("\nSelect track:")
            for i, t in enumerate(found, 1):
                print("{}. {} – {}".format(i, t.title, t.artist))

            pick = input("\nNumber: ")
            if pick.isdigit() and 1 <= int(pick) <= len(found):
                queue.tracks.append(found[int(pick) - 1].to_dict())
                queue.save()
                print("\nAdded.")
            pause()

        elif choice == "7":
            pl = pm.list_playlist_names()
            print("\nChoose playlist:")
            for i, p in enumerate(pl, 1):
                print("[{}] {}".format(i, p))

            pick = input("\nNumber: ")
            if pick.isdigit() and 1 <= int(pick) <= len(pl):
                tracks = pm.get_playlist_tracks(pl[int(pick) - 1])
                queue.tracks.extend([t.to_dict() for t in tracks])
                queue.save()
                print("\nPlaylist added to queue.")
            pause()

        elif choice == "8":
            queue.tracks = []
            queue.index = 0
            queue.save()
            print("\nQueue cleared.")
            pause()

        else:
            break


# ============================
#         MAIN RUNNER
# ============================
def main_menu():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("=== SIMPLE SPOTIFY-LIKE PLAYER ===\n")
        print("[1] Music Library")
        print("[2] Playlists")
        print("[3] Queue")
        print("[4] Exit")

        c = input("\nChoose: ")

        if c == "1":
            library_menu(lib, pm)

        elif c == "2":
            playlists_menu(pm, lib)

        elif c == "3":
            queue_menu(queue)

        elif c == "4":
            print("\nGoodbye sweetheart ❤️")
            break

        else:
            pause("Invalid option.")


# ============================
#         PROGRAM START
# ============================
if __name__ == "__main__":
    ensure_data_files()
    lib = MusicLibrary(file_path=TRACKS_FILE)
    pm = PlaylistManager(file_path=PLAYLISTS_FILE)
    queue = MusicQueue(file_path=QUEUE_FILE)

    main_menu()
