"""
Music Playlist System - Main Application
"""
import os
from ui import *
from storage import StorageManager
from library_interface import LibraryInterface
from playlist_interface import PlaylistInterface
from queue_interface import QueueInterface
from models import Queue


class MusicPlaylistApp:
    """Main application class"""
    
    def __init__(self):
        self.storage = StorageManager(data_dir="./data")
        self.library_interface = LibraryInterface(self.storage)
        self.playlist_interface = PlaylistInterface(self.storage)
        self.current_queue = None
    
    def run(self):
        """Run the main application"""
        while True:
            clear_screen()
            self._display_main_menu()
            
            choice = get_input("\nEnter your choice: ").strip()
            
            if choice == '1':
                self.library_interface.show_library()
            elif choice == '2':
                self.playlist_interface.show_playlists()
            elif choice == '3':
                self._show_queue_menu()
            elif choice == '4':
                self._show_about()
            elif choice == '5':
                self._exit_app()
                break
            else:
                print_error("Invalid choice")
                pause()
    
    def _display_main_menu(self):
        """Display main menu"""
        print_header("🎵 Music Playlist System 🎵")
        
        print_section("Main Menu")
        print_menu_option(1, "Music Library")
        print_menu_option(2, "Playlists")
        print_menu_option(3, "Queue & Player")
        print_menu_option(4, "About")
        print_menu_option(5, "Exit")
    
    def _show_queue_menu(self):
        """Show queue and player menu"""
        clear_screen()
        print_header("Queue & Player")
        
        # Load existing queue or create new
        self.current_queue = self.storage.load_queue()
        
        if self.current_queue is None:
            print_info("No queue available")
            print()
            print_menu_option(1, "Create new queue from library")
            print_menu_option(2, "Create new queue from playlist")
            print_menu_option(3, "Back to main menu")
            
            choice = get_input("\nEnter choice: ").strip()
            
            if choice == '1':
                self._create_queue_from_library()
            elif choice == '2':
                self._create_queue_from_playlist()
            return
        
        # Queue exists, show player
        print_success("Queue loaded")
        pause()
        
        queue_interface = QueueInterface(self.current_queue, self.storage)
        queue_interface.display_queue()
    
    def _create_queue_from_library(self):
        """Create queue from entire library"""
        all_tracks = self.storage.load_all_tracks()
        
        if not all_tracks:
            print_warning("No tracks in library")
            pause()
            return
        
        self.current_queue = Queue()
        for track in all_tracks:
            self.current_queue.add_track(track)
        
        print_success(f"Queue created with {len(all_tracks)} tracks")
        pause()
        
        queue_interface = QueueInterface(self.current_queue, self.storage)
        queue_interface.display_queue()
    
    def _create_queue_from_playlist(self):
        """Create queue from playlist"""
        clear_screen()
        print_header("Select Playlist")
        
        playlists = self.storage.load_all_playlists()
        
        if not playlists:
            print_warning("No playlists available")
            pause()
            return
        
        for i, playlist in enumerate(playlists, 1):
            print(f"  {Colors.BOLD}[{i}]{Colors.RESET} {playlist.name} ({len(playlist.tracks)} tracks)")
        
        print()
        try:
            choice = int(get_input("Select playlist number (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(playlists):
                playlist = playlists[choice - 1]
                self.current_queue = Queue()
                self.current_queue.add_playlist(playlist)
                
                print_success(f"Queue created from '{playlist.name}'")
                pause()
                
                queue_interface = QueueInterface(self.current_queue, self.storage)
                queue_interface.display_queue()
            else:
                print_error("Invalid selection")
                pause()
        except ValueError:
            print_error("Invalid input")
            pause()
    
    def _show_about(self):
        """Show about screen"""
        clear_screen()
        print_header("About Music Playlist System")
        
        print("""
╔════════════════════════════════════════════════════════════╗
║            Music Playlist System v1.0                      ║
║                                                            ║
║  A comprehensive music management application with:        ║
║  • Music library management                               ║
║  • Playlist creation and management                       ║
║  • Queue with shuffle and repeat modes                    ║
║  • O(1) queue operations                                  ║
║  • Persistent data storage (JSON)                         ║
║                                                            ║
║  Features:                                                ║
║  • Add, search, and manage tracks                         ║
║  • Create and organize playlists                          ║
║  • Play music with queue controls                         ║
║  • Shuffle and repeat functionality                       ║
║  • Pagination for large lists                            ║
║                                                            ║
║  Data Structure:                                          ║
║  • Circular Linked List for queue                        ║
║  • Sorted tracks by title, artist, album                 ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
        """)
        
        pause()
    
    def _exit_app(self):
        """Save and exit application"""
        clear_screen()
        print_header("Exit")
        
        if self.current_queue:
            print_info("Saving queue...")
            self.storage.save_queue(self.current_queue)
        
        print_success("Application closed. Goodbye!")
        print()


def main():
    """Main entry point"""
    try:
        app = MusicPlaylistApp()
        app.run()
    except KeyboardInterrupt:
        clear_screen()
        print_warning("\nApplication interrupted by user")
        print_info("Changes have been saved")
    except Exception as e:
        print_error(f"\nAn error occurred: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
