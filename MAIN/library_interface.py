"""
Music Playlist System - Library Management Interface
"""
from ui import *
from models import Track


class LibraryInterface:
    """Handles music library management"""
    
    def __init__(self, storage):
        self.storage = storage
    
    def show_library(self):
        """Main library menu"""
        while True:
            clear_screen()
            print_header("Music Library")
            
            all_tracks = self.storage.load_all_tracks()
            
            print_section("Library Statistics")
            print(f"  Total Tracks: {Colors.YELLOW}{len(all_tracks)}{Colors.RESET}")
            
            if all_tracks:
                total_seconds = sum(t.duration_to_seconds() for t in all_tracks)
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                total_duration = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
                print(f"  Total Duration: {Colors.YELLOW}{total_duration}{Colors.RESET}")
            
            print()
            print_section("Options")
            print_menu_option(1, "View all tracks")
            print_menu_option(2, "Add new track")
            print_menu_option(3, "Search track")
            print_menu_option(4, "Delete track")
            print_menu_option(5, "Play from library")
            print_menu_option(6, "Back to main menu")
            
            choice = get_input("\nEnter choice: ").strip()
            
            if choice == '1':
                self._view_all_tracks()
            elif choice == '2':
                self.add_new_track()
            elif choice == '3':
                self._search_track()
            elif choice == '4':
                self._delete_track()
            elif choice == '5':
                self._play_from_library()
            elif choice == '6':
                break
    
    def add_new_track(self):
        """Add a new track to the library"""
        clear_screen()
        print_header("Add New Track")
        
        title = get_input("Track title: ").strip()
        if not title:
            print_error("Title cannot be empty")
            pause()
            return
        
        artist = get_input("Artist name: ").strip()
        if not artist:
            print_error("Artist cannot be empty")
            pause()
            return
        
        album = get_input("Album name: ").strip()
        if not album:
            print_error("Album cannot be empty")
            pause()
            return
        
        duration = self._get_duration_input()
        if not duration:
            return
        
        additional_artists = get_input("Additional artists (comma-separated, or leave blank): ").strip()
        
        track = Track(title, artist, album, duration, additional_artists)
        
        if self.storage.save_track(track):
            print_success(f"Track '{title}' added successfully")
            
            # Auto-create album
            album_obj = self.storage.get_or_create_album(album)
            album_obj.add_track(track)
            self.storage.save_album(album_obj)
            print_info(f"Album '{album}' updated")
            
            pause()
        else:
            print_warning("Track already exists in library")
            pause()
    
    def _get_duration_input(self) -> str:
        """Get duration input in mm:ss format"""
        while True:
            duration = get_input("Duration (mm:ss format, e.g., 03:45): ").strip()
            
            if not duration:
                print_error("Duration cannot be empty")
                continue
            
            parts = duration.split(':')
            if len(parts) != 2:
                print_error("Invalid format. Use mm:ss")
                continue
            
            try:
                minutes = int(parts[0])
                seconds = int(parts[1])
                
                if minutes < 0 or seconds < 0 or seconds >= 60:
                    print_error("Invalid duration values")
                    continue
                
                return f"{minutes:02d}:{seconds:02d}"
            except ValueError:
                print_error("Duration must contain only numbers")
    
    def _view_all_tracks(self):
        """View all tracks in library"""
        clear_screen()
        print_header("Music Library - All Tracks")
        
        all_tracks = self.storage.load_all_tracks()
        
        if not all_tracks:
            print_info("No tracks in library")
            pause()
            return
        
        # Display with pagination
        page_size = 15
        total_pages = (len(all_tracks) + page_size - 1) // page_size
        current_page = 1
        
        while True:
            clear_screen()
            print_header(f"Music Library - Page {current_page} of {total_pages}")
            
            start_idx = (current_page - 1) * page_size
            end_idx = min(start_idx + page_size, len(all_tracks))
            
            print_section("Tracks")
            for i in range(start_idx, end_idx):
                track = all_tracks[i]
                print(f"  {Colors.BOLD}[{i + 1}]{Colors.RESET} {track.get_display_name()}")
            
            print()
            
            if total_pages > 1:
                print_divider()
                print(f"{Colors.DIM}Page {current_page} of {total_pages}{Colors.RESET}")
                print()
                
                options_str = ""
                if current_page > 1:
                    print_menu_option(1, "Previous page")
                    options_str = "(1) Previous  "
                if current_page < total_pages:
                    print_menu_option(2, "Next page")
                    options_str += "(2) Next  "
                print_menu_option(3, "Back")
                
                choice = get_input("\nEnter choice: ").strip()
                
                if choice == '1' and current_page > 1:
                    current_page -= 1
                elif choice == '2' and current_page < total_pages:
                    current_page += 1
                elif choice == '3':
                    break
            else:
                print_menu_option(1, "Back")
                if get_input("\nEnter choice: ").strip() == '1':
                    break
    
    def _search_track(self):
        """Search for tracks by title"""
        clear_screen()
        print_header("Search Tracks")
        
        search_query = get_input("Enter track title to search: ").strip()
        if not search_query:
            return
        
        results = self.storage.search_tracks(search_query)
        
        if not results:
            print_warning(f"No tracks found matching '{search_query}'")
            pause()
            return
        
        clear_screen()
        print_header(f"Search Results - '{search_query}'")
        print(f"Found {Colors.YELLOW}{len(results)}{Colors.RESET} track(s)")
        
        print_section("Results")
        for i, track in enumerate(results, 1):
            print(f"  {Colors.BOLD}[{i}]{Colors.RESET} {track.get_display_name()}")
        
        print()
        print_menu_option(1, "Back")
        pause()
    
    def _delete_track(self):
        """Delete a track from library"""
        clear_screen()
        print_header("Delete Track")
        
        all_tracks = self.storage.load_all_tracks()
        
        if not all_tracks:
            print_warning("No tracks to delete")
            pause()
            return
        
        print_section("Tracks")
        for i, track in enumerate(all_tracks, 1):
            print(f"  {Colors.BOLD}[{i}]{Colors.RESET} {track.get_display_name()}")
        
        print()
        try:
            choice = int(get_input("Select track number to delete (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(all_tracks):
                track = all_tracks[choice - 1]
                if confirm(f"Delete '{track.title}' by {track.artist}?"):
                    if self.storage.delete_track(track.title, track.artist, track.album):
                        print_success("Track deleted")
                    else:
                        print_error("Failed to delete track")
                pause()
            else:
                print_error("Invalid selection")
                pause()
        except ValueError:
            print_error("Invalid input")
            pause()
    
    def _play_from_library(self):
        """Play all tracks from library as queue"""
        clear_screen()
        print_header("Play from Library")
        
        all_tracks = self.storage.load_all_tracks()
        
        if not all_tracks:
            print_warning("No tracks in library")
            pause()
            return
        
        print_info(f"Creating queue with {len(all_tracks)} tracks...")
        
        from queue_interface import QueueInterface
        from models import Queue
        
        queue = self.storage.load_queue() or Queue()
        queue.clear()
        
        for track in all_tracks:
            queue.add_track(track)
        
        queue_interface = QueueInterface(queue, self.storage)
        queue_interface.display_queue()
