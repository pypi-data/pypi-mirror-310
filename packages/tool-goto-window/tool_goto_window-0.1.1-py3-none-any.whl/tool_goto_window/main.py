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
        
        # Activate the first matching window
        window = matching_windows[0]
        window.activate()
        print(f"Switched to window: {window.title}")
        
    except Exception as e:
        print(f"Error switching windows: {e}")

def main():
    print("[START] tool-goto-window")
