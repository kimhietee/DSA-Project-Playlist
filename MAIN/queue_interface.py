"""
Music Playlist System - Queue Interface
"""
from ui import *
from models import Queue, Track
from typing import Optional


class QueueInterface:
    """Handles queue display and playback controls"""
    
    def __init__(self, queue: Queue, storage):
        self.queue = queue
        self.storage = storage
        self.current_page = 1
        self.page_size = 10
    
    def display_queue(self):
        """Main queue display interface"""
        while True:
            clear_screen()
            
            if self.queue.total_tracks == 0:
                print_header("Queue")
                print_info("Queue is empty")
                print()
                
                choice = get_input("Enter 'q' to go back: ").lower()
                if choice == 'q':
                    break
                continue
            
            self._display_queue_content()
            self._display_queue_menu()
            
            choice = get_input("\nEnter your choice: ").lower()
            if not self._handle_queue_command(choice):
                break
    
    def _display_queue_content(self):
        """Display queue content"""
        print_header("Queue")
        
        # Display queue info
        print_section("Queue Information")
        print(f"  Total Duration: {Colors.YELLOW}{self.queue.get_total_duration_formatted()}{Colors.RESET}")
        print(f"  Shuffled: {Colors.YELLOW}{'Yes' if self.queue.is_shuffled else 'No'}{Colors.RESET}")
        print(f"  Repeat: {Colors.YELLOW}{'Yes' if self.queue.is_repeat else 'No'}{Colors.RESET}")
        
        # Display current track
        current_track = self.queue.get_current_track()
        print_section("Currently Playing")
        if current_track:
            status = "(Paused)"
            print(f"  {Colors.BOLD}{current_track.get_display_name()}{Colors.RESET} {status}")
        
        # Display next tracks
        print_section("Next Tracks")
        tracks, page, total_pages = self.queue.get_tracks_page(self.current_page, self.page_size)
        
        # Skip current track from display if it's on first page
        if page == 1 and tracks and tracks[0] == current_track:
            for i, track in enumerate(tracks[1:], 1):
                print(f"  {Colors.BOLD}({i}){Colors.RESET} {track.get_display_name()}")
        else:
            for i, track in enumerate(tracks, 1):
                print(f"  {Colors.BOLD}({i}){Colors.RESET} {track.get_display_name()}")
        
        # Pagination info
        print_divider()
        print(f"{Colors.DIM}Page {page} of {total_pages}{Colors.RESET}")
    
    def _display_queue_menu(self):
        """Display queue control menu"""
        print_section("Controls")
        print_menu_option(1, "Play")
        print_menu_option(2, "Next")
        print_menu_option(3, "Previous")
        
        if self.queue.is_repeat:
            print_menu_option(4, "Turn off repeat")
        else:
            print_menu_option(4, "Turn on repeat")
        
        if self.queue.is_shuffled:
            print_menu_option(5, "Turn off shuffle")
        else:
            print_menu_option(5, "Turn on shuffle")
        
        print_menu_option(6, "Clear queue")
        print_menu_option(7, "Add tracks to queue")
        
        tracks, page, total_pages = self.queue.get_tracks_page(self.current_page, self.page_size)
        if total_pages > 1:
            if page > 1:
                print_menu_option(8, "Previous page")
            if page < total_pages:
                print_menu_option(9, "Next page")
        
        print_menu_option(10, "Back to main menu")
    
    def _handle_queue_command(self, command: str) -> bool:
        """Handle queue commands. Returns False to exit"""
        try:
            choice = int(command)
        except ValueError:
            print_error("Invalid input")
            pause()
            return True
        
        if choice == 1:
            self._play()
        elif choice == 2:
            self._next()
        elif choice == 3:
            self._previous()
        elif choice == 4:
            self.queue.toggle_repeat()
            print_success(f"Repeat {'enabled' if self.queue.is_repeat else 'disabled'}")
            pause()
        elif choice == 5:
            self.queue.toggle_shuffle()
            print_success(f"Shuffle {'enabled' if self.queue.is_shuffled else 'disabled'}")
            pause()
        elif choice == 6:
            if confirm("Clear entire queue?"):
                self.queue.clear()
                self.storage.clear_queue()
                print_success("Queue cleared")
                pause()
                return False
        elif choice == 7:
            self._add_tracks_to_queue()
        elif choice == 8:
            self.current_page = max(1, self.current_page - 1)
        elif choice == 9:
            tracks, page, total_pages = self.queue.get_tracks_page(self.current_page, self.page_size)
            if page < total_pages:
                self.current_page += 1
        elif choice == 10:
            self.storage.save_queue(self.queue)
            return False
        else:
            print_error("Invalid choice")
            pause()
        
        return True
    
    def _play(self):
        """Play current track"""
        current = self.queue.get_current_track()
        if current:
            print_header("Playing")
            print(f"  {current.get_display_name()}")
            print_info("Playing started (simulated)")
            pause()
    
    def _next(self):
        """Skip to next track"""
        if self.queue.is_repeat or self.queue.total_tracks > 0:
            next_track = self.queue.next_track()
            if next_track:
                print_success(f"Playing: {next_track.get_display_name()}")
            else:
                print_warning("No more tracks")
            pause()
    
    def _previous(self):
        """Go to previous track"""
        prev_track = self.queue.prev_track()
        if prev_track:
            print_success(f"Playing: {prev_track.get_display_name()}")
        else:
            print_warning("Already at first track")
        pause()
    
    def _add_tracks_to_queue(self):
        """Add tracks to queue from library or playlist"""
        clear_screen()
        print_header("Add Tracks to Queue")
        
        print_menu_option(1, "Add from music library")
        print_menu_option(2, "Add entire playlist")
        print_menu_option(3, "Back")
        
        choice = get_input("\nSelect option: ").strip()
        
        if choice == '1':
            self._add_from_library()
        elif choice == '2':
            self._add_entire_playlist()
    
    def _add_from_library(self):
        """Add individual tracks from library"""
        clear_screen()
        print_header("Add from Library")
        
        all_tracks = self.storage.load_all_tracks()
        if not all_tracks:
            print_warning("No tracks in library")
            pause()
            return
        
        # Show library and get selection
        for i, track in enumerate(all_tracks, 1):
            print(f"  {Colors.BOLD}[{i}]{Colors.RESET} {track.get_display_name()}")
        
        print()
        try:
            choice = int(get_input("Select track number (0 to cancel): "))
            if choice == 0:
                return
            if 1 <= choice <= len(all_tracks):
                self.queue.add_track(all_tracks[choice - 1])
                print_success(f"Added: {all_tracks[choice - 1].get_display_name()}")
                pause()
            else:
                print_error("Invalid selection")
                pause()
        except ValueError:
            print_error("Invalid input")
            pause()
    
    def _add_entire_playlist(self):
        """Add entire playlist to queue"""
        clear_screen()
        print_header("Add Playlist to Queue")
        
        playlists = self.storage.load_all_playlists()
        if not playlists:
            print_warning("No playlists available")
            pause()
            return
        
        # Show playlists
        for i, playlist in enumerate(playlists, 1):
            duration = playlist.get_total_duration_formatted()
            print(f"  {Colors.BOLD}[{i}]{Colors.RESET} {playlist.name} ({duration}, {len(playlist.tracks)} tracks)")
        
        print()
        try:
            choice = int(get_input("Select playlist number (0 to cancel): "))
            if choice == 0:
                return
            if 1 <= choice <= len(playlists):
                self.queue.add_playlist(playlists[choice - 1])
                print_success(f"Added playlist: {playlists[choice - 1].name}")
                pause()
            else:
                print_error("Invalid selection")
                pause()
        except ValueError:
            print_error("Invalid input")
            pause()
