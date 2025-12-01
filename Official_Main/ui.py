import shutil

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

def display_tracks(name, songs):
    title_w = 30
    artist_w = 20
    album_w = 24
    duration_w = 10
    total_w = title_w + artist_w + album_w + duration_w + 11

    def trim(text, max_w):
        text = str(text)
        return text[:max_w-3] + "..." if len(text) > max_w else text

    total = len(songs)
    if total == 0:
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
        for _ in range(4):
            print("| {:<{}} | {:<{}} | {:<{}} | {:>{}} |".format(
                "", title_w, "", artist_w, "", album_w, "00:00", duration_w
            ))
        print(row)
        print("\nNo items to display.\n")
        return

    page_size = 10
    total_pages = (total + page_size - 1) // page_size
    page = 1

    def print_page(p):
        start = (p - 1) * page_size
        end = min(start + page_size, total)

        w = terminal_width()
        key_col = 6
        desc_col = w - key_col - 7
        top = "+" + "-" * (key_col + desc_col + 5) + "+"
        row = "+" + "-" * (key_col + 2) + "+" + "-" * (desc_col + 2) + "+"

        print(top)
        header_title = f"Playlist: {name}  (Page {p}/{total_pages})"
        print("|{:^{width}}|".format(header_title, width=total_w))
        print(row)

        print("| {:<{}} | {:<{}} | {:<{}} | {:>{}} |".format(
            "Title", title_w,
            "Artist", artist_w,
            "Album", album_w,
            "Duration", duration_w
        ))
        print(row)

        for s in songs[start:end]:
            t = trim(s.get("title", ""), title_w)
            a = trim(s.get("artist", ""), artist_w)
            al = trim(s.get("album", ""), album_w)
            d = s.get("duration", "")
            print("| {:<{}} | {:<{}} | {:<{}} | {:>{}} |".format(
                t, title_w,
                a, artist_w,
                al, album_w,
                d, duration_w
            ))

        print(row)

    while True:
        print_page(page)
        if total_pages <= 1:
            break

        choice = input(f"Page {page}/{total_pages} - press 'n' for next page, 'p' for previous, or Enter to continue: ").strip().lower()
        if choice == 'n' and page < total_pages:
            page += 1
            continue
        elif choice == 'p' and page > 1:
            page -= 1
            continue
        else:
            break
