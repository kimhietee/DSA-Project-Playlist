"""
Music Playlist System - Playlist Management Interface
"""
from ui import *
from models import Playlist, Track


class PlaylistInterface:
    """Handles playlist management and operations"""
    
    def __init__(self, storage):
        self.storage = storage
        self.current_page = 1
        self.page_size = 10
    
    def show_playlists(self):
        """Main playlist menu"""
        while True:
            clear_screen()
            print_header("Playlists")
            
            playlists = self.storage.load_all_playlists()
            
            if not playlists:
                print_info("No playlists yet")
                print()
                print_menu_option(1, "Create new playlist")
                print_menu_option(2, "Back to main menu")
                
                choice = get_input("\nEnter choice: ").strip()
                if choice == '1':
                    self.create_playlist()
                elif choice == '2':
                    break
                continue
            
            # Display playlists with pagination
            self._display_playlists_page(playlists)
            
            # Show menu
            print_section("Options")
            print_menu_option(1, "Create new playlist")
            print_menu_option(2, "Open playlist")
            print_menu_option(3, "Delete playlist")
            print_menu_option(4, "Back to main menu")
            
            choice = get_input("\nEnter choice: ").strip()
            
            if choice == '1':
                self.create_playlist()
            elif choice == '2':
                self.open_playlist()
            elif choice == '3':
                self.delete_playlist()
            elif choice == '4':
                break
    
    def _display_playlists_page(self, playlists: list):
        """Display playlists with pagination"""
        total_pages = (len(playlists) + self.page_size - 1) // self.page_size
        self.current_page = max(1, min(self.current_page, total_pages))
        
        start_idx = (self.current_page - 1) * self.page_size
        end_idx = min(start_idx + self.page_size, len(playlists))
        
        print_section("Your Playlists")
        for i in range(start_idx, end_idx):
            playlist = playlists[i]
            duration = playlist.get_total_duration_formatted()
            track_count = len(playlist.tracks)
            print(f"  {Colors.BOLD}[{i + 1}]{Colors.RESET} {playlist.name}")
            print(f"    {Colors.DIM}{duration} • {track_count} track{'s' if track_count != 1 else ''}{Colors.RESET}")
        
        print_divider()
        print(f"{Colors.DIM}Page {self.current_page} of {total_pages}{Colors.RESET}")
        
        if total_pages > 1:
            if self.current_page > 1:
                print_menu_option(11, "Previous page")
            if self.current_page < total_pages:
                print_menu_option(12, "Next page")
    
    def create_playlist(self):
        """Create a new playlist"""
        clear_screen()
        print_header("Create New Playlist")
        
        name = get_input("Enter playlist name: ").strip()
        
        if not name:
            print_error("Playlist name cannot be empty")
            pause()
            return
        
        # Check if name already exists
        existing = self.storage.get_playlist_by_name(name)
        if existing:
            print_error(f"Playlist '{name}' already exists")
            pause()
            return
        
        playlist = Playlist(name)
        if self.storage.save_playlist(playlist):
            print_success(f"Playlist '{name}' created successfully")
            pause()
        else:
            print_error(f"Failed to create playlist '{name}'")
            pause()
    
    def open_playlist(self):
        """Open and manage a playlist"""
        clear_screen()
        print_header("Select Playlist to Open")
        
        playlists = self.storage.load_all_playlists()
        if not playlists:
            print_warning("No playlists available")
            pause()
            return
        
        for i, playlist in enumerate(playlists, 1):
            duration = playlist.get_total_duration_formatted()
            print(f"  {Colors.BOLD}[{i}]{Colors.RESET} {playlist.name} ({len(playlist.tracks)} tracks, {duration})")
        
        print()
        try:
            choice = int(get_input("Select playlist number (0 to cancel): "))
            if choice == 0:
                return
            if 1 <= choice <= len(playlists):
                self.manage_playlist(playlists[choice - 1])
            else:
                print_error("Invalid selection")
                pause()
        except ValueError:
            print_error("Invalid input")
            pause()
    
    def manage_playlist(self, playlist: Playlist):
        """Manage tracks in a playlist"""
        while True:
            clear_screen()
            print_header(f"Playlist: {playlist.name}")
            
            print_section("Playlist Information")
            print(f"  Tracks: {Colors.YELLOW}{len(playlist.tracks)}{Colors.RESET}")
            print(f"  Duration: {Colors.YELLOW}{playlist.get_total_duration_formatted()}{Colors.RESET}")
            
            if playlist.tracks:
                print_section("Tracks")
                current_page = 1
                page_size = 10
                total_pages = (len(playlist.tracks) + page_size - 1) // page_size
                
                start_idx = (current_page - 1) * page_size
                end_idx = min(start_idx + page_size, len(playlist.tracks))
                
                for i in range(start_idx, end_idx):
                    track = playlist.tracks[i]
                    print(f"  {Colors.BOLD}[{i + 1}]{Colors.RESET} {track.get_display_name()}")
            else:
                print_info("No tracks in playlist")
            
            print()
            print_section("Options")
            print_menu_option(1, "Add track to playlist")
            print_menu_option(2, "Search and add track")
            print_menu_option(3, "Remove track")
            print_menu_option(4, "Play this playlist")
            print_menu_option(5, "Back to playlists")
            
            choice = get_input("\nEnter choice: ").strip()
            
            if choice == '1':
                self._add_track_to_playlist(playlist)
            elif choice == '2':
                self._search_and_add_track(playlist)
            elif choice == '3':
                self._remove_track_from_playlist(playlist)
            elif choice == '4':
                from queue_interface import QueueInterface
                queue = self.storage.load_queue() or __import__('models').Queue()
                queue.clear()
                queue.add_playlist(playlist)
                queue_interface = QueueInterface(queue, self.storage)
                queue_interface.display_queue()
            elif choice == '5':
                break
    
    def _add_track_to_playlist(self, playlist: Playlist):
        """Add individual track from library to playlist"""
        clear_screen()
        print_header("Add Track to Playlist")
        
        all_tracks = self.storage.load_all_tracks()
        if not all_tracks:
            print_warning("No tracks in library")
            pause()
            return
        
        print_section("Available Tracks")
        for i, track in enumerate(all_tracks, 1):
            print(f"  {Colors.BOLD}[{i}]{Colors.RESET} {track.get_display_name()}")
        
        print()
        try:
            choice = int(get_input("Select track number (0 to cancel): "))
            if choice == 0:
                return
            if 1 <= choice <= len(all_tracks):
                if playlist.add_track(all_tracks[choice - 1]):
                    self.storage.update_playlist(playlist)
                    print_success(f"Added: {all_tracks[choice - 1].get_display_name()}")
                else:
                    print_warning("Track already exists in playlist")
                pause()
            else:
                print_error("Invalid selection")
                pause()
        except ValueError:
            print_error("Invalid input")
            pause()
    
    def _search_and_add_track(self, playlist: Playlist):
        """Search for track by title and add to playlist"""
        clear_screen()
        print_header("Search and Add Track")
        
        search_query = get_input("Search for track: ").strip()
        if not search_query:
            return
        
        results = self.storage.search_tracks(search_query)
        if not results:
            print_warning(f"No tracks found matching '{search_query}'")
            pause()
            return
        
        print_section("Search Results")
        for i, track in enumerate(results, 1):
            print(f"  {Colors.BOLD}[{i}]{Colors.RESET} {track.get_display_name()}")
        
        print()
        try:
            choice = int(get_input("Select track number (0 to cancel): "))
            if choice == 0:
                return
            if 1 <= choice <= len(results):
                if playlist.add_track(results[choice - 1]):
                    self.storage.update_playlist(playlist)
                    print_success(f"Added: {results[choice - 1].get_display_name()}")
                else:
                    print_warning("Track already exists in playlist")
                pause()
            else:
                print_error("Invalid selection")
                pause()
        except ValueError:
            print_error("Invalid input")
            pause()
    
    def _remove_track_from_playlist(self, playlist: Playlist):
        """Remove track from playlist"""
        clear_screen()
        print_header("Remove Track from Playlist")
        
        if not playlist.tracks:
            print_warning("No tracks in playlist")
            pause()
            return
        
        print_section("Tracks in Playlist")
        for i, track in enumerate(playlist.tracks, 1):
            print(f"  {Colors.BOLD}[{i}]{Colors.RESET} {track.get_display_name()}")
        
        print()
        try:
            choice = int(get_input("Select track number to remove (0 to cancel): "))
            if choice == 0:
                return
            if 1 <= choice <= len(playlist.tracks):
                track = playlist.tracks[choice - 1]
                if confirm(f"Remove '{track.title}'?"):
                    playlist.remove_track(choice - 1)
                    self.storage.update_playlist(playlist)
                    print_success("Track removed")
                pause()
            else:
                print_error("Invalid selection")
                pause()
        except ValueError:
            print_error("Invalid input")
            pause()
    
    def delete_playlist(self):
        """Delete a playlist"""
        clear_screen()
        print_header("Delete Playlist")
        
        playlists = self.storage.load_all_playlists()
        if not playlists:
            print_warning("No playlists to delete")
            pause()
            return
        
        for i, playlist in enumerate(playlists, 1):
            print(f"  {Colors.BOLD}[{i}]{Colors.RESET} {playlist.name}")
        
        print()
        try:
            choice = int(get_input("Select playlist number to delete (0 to cancel): "))
            if choice == 0:
                return
            if 1 <= choice <= len(playlists):
                playlist_name = playlists[choice - 1].name
                if confirm(f"Delete playlist '{playlist_name}'?"):
                    if self.storage.delete_playlist(playlist_name):
                        print_success(f"Playlist '{playlist_name}' deleted")
                    else:
                        print_error("Failed to delete playlist")
                pause()
            else:
                print_error("Invalid selection")
                pause()
        except ValueError:
            print_error("Invalid input")
            pause()
