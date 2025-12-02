import shutil

def terminal_width(default=80):
    try:
        cols = shutil.get_terminal_size().columns
        return max(60, cols)
    except Exception:
        return default

def duration_to_seconds(d):
    try:
        mm, ss = d.split(":")
        return int(mm) * 60 + int(ss)
    except:
        return 0
        
def seconds_to_hhmmss(total):
    h = total // 3600
    m = (total % 3600) // 60
    s = total % 60
    if h > 0:
        return f"{h:02}:{m:02}:{s:02}"
    return f"{m:02}:{s:02}"

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

def sort_playlist(songs, mode):
    pass

class TimSort:
    minRUN = 16
    
    @staticmethod
    def calcMinRun(n):
        r = 0
        while n >= TimSort.minRUN:
            r |= n & 1
            n >>= 1
        return n + r
        
    @staticmethod
    def insertionSort(arr, left, right):
        for i in range(left + 1, right + 1):
            key = arr[i]
            j = i - 1
            while j >= left and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key

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

    @staticmethod
    def findRun(arr, start, n):
        end = start + 1
        if end == n: return end
        if arr[end] < arr[start]:
            while end < n and arr[end] < arr[end - 1]:
                end += 1
            arr[start:end] = reversed(arr[start:end])
        else:
            while end < n and arr[end] >= arr[end - 1]:
                end += 1
        return end

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


def sort_playlist(songs, mode="title"):
    if not songs:
        print("❌ Nothing to sort.\n")
        return

    mode = (mode or 'title').lower()

    def duration_seconds(s):
        mm_ss = s.get("duration", "0:0")
        try:
            mm, ss = mm_ss.split(":")
            return int(mm) * 60 + int(ss)
        except Exception:
            return 0

    def composite_key(s):
        if mode == 'duration':
            primary = duration_seconds(s)
        else:
            primary = (s.get(mode, '') or '').lower()

        title = (s.get('title', '') or '').lower()
        artist = (s.get('artist', '') or '').lower()
        album = (s.get('album', '') or '').lower()
        duration_val = duration_seconds(s)
        date_val = s.get('date_added', '') or ''

        return (primary, title, artist, album, duration_val, date_val)

    songs.sort(key=composite_key)


