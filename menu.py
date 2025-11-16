def display_playlist():
    print("=" * 113)
    print("{0:>64}".format("(Playlist Name)"))
    print("=" * 113)
    print("| {0:<40} | {1:<20} | {2:<30} | {3:<10} |".format("Title", "Artist", "Album", "Duration"))
    print("=" * 113)
    print()
    print("=" * 113)

while True:
    print("=" * 113)
    print("{0:>61}".format("MAIN MENU"))
    print("=" * 113)
    print("[1] Library")
    print("[2] Playlists")
    print("[3] Music Queue")
    print("[4] Exit")
    print("=" * 113)
    choice = input("Enter your choice: ")

    if choice == '1':
        print("=" * 113)
        print("{0:>63}".format("MUSIC LIBRARY"))
        print("=" * 113)
        print("[1] Enqueue Library to Queue")
        print("[2] Play Library")
        print("[3] View Music Library")
        print("[4] Add Track to Library")
        print("[5] Add Track to Queue")
        print("[6] Back")
        print("=" * 113)
        choice = input("Enter your choice: ")

        # if choice == '1':
            
        # elif choice == '2':

        # elif choice == '3':   
        if choice == '3':
            display_playlist()
             
        # elif choice == '4':
             
        # elif choice == '5':
             
        # elif choice == '6':
        #     break
    # elif choice == '2':

    # elif choice == '3':

    elif choice == '4':
        print("=" * 50)
        print("Thank you for using our service.")
        print("=" * 50)
        break
