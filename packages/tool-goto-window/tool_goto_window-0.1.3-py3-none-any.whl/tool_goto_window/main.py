import typer
from typing import Annotated
import pywinctl as pwc

def switch_to_window(
    window_name: Annotated[str, typer.Argument(help="Name of the window to switch to")]
):
    """Switch to a window that matches the given name (case-insensitive partial match)"""
    try:
        # Get windows matching the name (case-insensitive)
        matching_windows = pwc.getWindowsWithTitle(
            window_name, 
            condition=pwc.Re.CONTAINS, 
            flags=pwc.Re.IGNORECASE
        )
        
        if not matching_windows:
            print(f"No windows found matching '{window_name}'")
            return
        
        # Activate the most recent window (first in the reversed list)
        window = list(reversed(matching_windows))[0]
        window.activate()
        print(f"Switched to window: {window.title}")
        
    except Exception as e:
        print(f"Error switching windows: {e}")

def show_recent_windows(
    app_name: Annotated[str, typer.Argument(help="Name of the application to show recent windows for")],
    limit: Annotated[int, typer.Option(help="Number of recent windows to show")] = None
):
    """Show recent windows for a given application"""
    try:
        # Get windows matching the name (case-insensitive)
        matching_windows = pwc.getWindowsWithTitle(
            app_name,
            condition=pwc.Re.CONTAINS,
            flags=pwc.Re.IGNORECASE
        )
        
        if not matching_windows:
            print(f"No windows found for '{app_name}'")
            return
        
        # Reverse the list to get most recent first and apply limit if specified
        recent_windows = list(reversed(matching_windows))
        if limit:
            recent_windows = recent_windows[:limit]
        
        print(f"\nRecent windows for '{app_name}':")
        for i, window in enumerate(recent_windows, 1):
            print(f"{i}. {window.title}")
            
    except Exception as e:
        print(f"Error listing windows: {e}")

def main():
    print("[START] tool-goto-window")
