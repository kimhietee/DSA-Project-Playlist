import json
import os
from pprint import pprint



def load_data(file) -> dict:
    if not os.path.exists(file):
        with open(file, "w") as f:
            f.write("[]")
    with open(file, "r") as f:
        return json.load(f)

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)


filepath = 'library.json'
x = load_data(filepath)


def delete_song(library):
    pass
# fp = 'playlists.json'

# pprint(type(x))



# for i in x:
#     # pprint(i)
#     pprint(i['album'])
# print()
# for i in x:
#     pprint(i['artist'])
# print()
# for i in x:
#     pprint(i['album'])
# print()
# for i in x:
#     pprint(i['album'])


# import main



def delete_song(library):
    if not library:
        print("Library is empty.")
        return library

    title = input("Enter track title to delete: ").strip().lower()

    # find matches
    matches = [t for t in library if t["title"].lower() == title]

    if not matches:
        print("No track with that title found.")
        return library

    # if only one, delete immediately
    if len(matches) == 1:
        library.remove(matches[0])
        print("Track deleted successfully.")
        return library

    # multiple tracks with the same title → choose which one
    print("\nMultiple tracks found with the same title:")
    for i, t in enumerate(matches, 1):
        print(f"[{i}] {t['title']} – {t['artist']} ({t['duration']})")

    try:
        choice = int(input("Select which track to delete: "))
        if 1 <= choice <= len(matches):
            library.remove(matches[choice - 1])
            print("Track deleted successfully.")
        else:
            print("Invalid option.")
    except:
        print("Invalid input.")

    return library