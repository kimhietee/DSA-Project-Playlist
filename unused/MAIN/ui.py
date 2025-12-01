"""
Music Playlist System - UI Utilities and Helpers
"""
import os
import sys


class Colors:
    """ANSI color codes for terminal output"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'


def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title: str):
    """Print formatted header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}")
    print(f"{title.center(60)}")
    print(f"{'='*60}{Colors.RESET}\n")


def print_section(title: str):
    """Print section title"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{title}{Colors.RESET}")
    print(f"{Colors.DIM}{'-'*40}{Colors.RESET}")


def print_success(message: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")


def print_error(message: str):
    """Print error message"""
    print(f"{Colors.RED}✗ {message}{Colors.RESET}")


def print_info(message: str):
    """Print info message"""
    print(f"{Colors.CYAN}ℹ {message}{Colors.RESET}")


def print_warning(message: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.RESET}")


def print_menu_option(number: int, description: str, disabled: bool = False):
    """Print a menu option"""
    if disabled:
        print(f"  {Colors.DIM}[{number}] {description}{Colors.RESET}")
    else:
        print(f"  {Colors.BOLD}[{number}]{Colors.RESET} {description}")


def get_input(prompt: str = "Enter your choice: ") -> str:
    """Get user input"""
    return input(f"{Colors.BOLD}{Colors.CYAN}{prompt}{Colors.RESET}").strip()


def get_int_input(prompt: str = "Enter your choice: ") -> int:
    """Get integer input from user"""
    while True:
        try:
            return int(get_input(prompt))
        except ValueError:
            print_error("Please enter a valid number")


def print_divider():
    """Print a divider line"""
    print(f"{Colors.DIM}{'-'*60}{Colors.RESET}")


def pause():
    """Pause and wait for user to press Enter"""
    input(f"{Colors.DIM}Press Enter to continue...{Colors.RESET}")


def print_track_list(tracks: list, start_index: int = 0):
    """Print a formatted list of tracks"""
    for i, track in enumerate(tracks, start_index):
        print(f"  {Colors.BOLD}({i}){Colors.RESET} {track.get_display_name()}")


def print_formatted_duration(seconds: int) -> str:
    """Format seconds to readable duration"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours} hr {minutes} min {secs} sec"
    elif minutes > 0:
        return f"{minutes} min {secs} sec"
    return f"{secs} sec"


class Table:
    """Simple table formatter"""
    
    def __init__(self, columns: list, column_widths: list = None):
        self.columns = columns
        self.column_widths = column_widths or [20] * len(columns)
        self.rows = []
    
    def add_row(self, row: list):
        """Add a row to the table"""
        self.rows.append(row)
    
    def print_table(self):
        """Print the table"""
        # Print header
        header = " | ".join(
            f"{col:<{width}}" for col, width in zip(self.columns, self.column_widths)
        )
        print(f"{Colors.BOLD}{Colors.CYAN}{header}{Colors.RESET}")
        print(f"{Colors.DIM}{'-'*len(header)}{Colors.RESET}")
        
        # Print rows
        for row in self.rows:
            row_str = " | ".join(
                f"{str(val):<{width}}" for val, width in zip(row, self.column_widths)
            )
            print(row_str)


def confirm(prompt: str = "Are you sure?") -> bool:
    """Get yes/no confirmation from user"""
    while True:
        response = get_input(f"{prompt} (y/n): ").lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print_error("Please enter 'y' or 'n'")
