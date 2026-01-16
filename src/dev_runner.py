#!/usr/bin/env python3

import sys
import subprocess
import time
from pathlib import Path
from watchfiles import watch


def run_app():
    """
    Starts the main application as a subprocess.
    
    Returns:
        subprocess.Popen: A process object representing the running application
    """

    # Launch the main.py script using the current Python interpreter
    # cwd sets the working directory to the parent of this script's directory
    return subprocess.Popen(
        [sys.executable, "src/main.py"],
        cwd=Path(__file__).parent.parent,
    )


def main():
    """
    Main function that implements a development mode with automatic restart.
    Watches for file changes and restarts the application when Python files are modified.
    """

    print("Starting development mode with auto-restart...")
    print("Watching for changes in src/...")
    print("Press Ctrl+C to stop\n")
    
    # Start the application for the first time
    process = run_app()
    
    try:
        # Watch for changes in the directory containing this script
        # The watch_filter ensures we only respond to .py files and ignore __pycache__ directories
        for changes in watch(
            Path(__file__).parent,
            watch_filter=lambda change, path: path.endswith('.py') and '__pycache__' not in path
        ):
            # Print terminal UI for user to see what changed
            print(f"\n{'='*60}")
            print("Changes detected:")
            for change_type, path in changes:
                print(f"  - {Path(path).relative_to(Path.cwd())}")
            print(f"{'='*60}")
            print("Restarting application...\n")
            
            # RESTART APP WHEN CHANGES ARE DETECTED ###########################
            ###################################################################
            # Check if the process is still running (poll() returns None if running)
            if process.poll() is None:
                # Gracefully terminate the process
                process.terminate()
                try:
                    # Wait up to 3 seconds for the process to terminate gracefully
                    process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    # If it doesn't terminate in time, force kill it
                    process.kill()
                    # Wait for the process to be fully killed
                    process.wait()
            
            # Small delay to ensure clean shutdown before restart
            time.sleep(0.2)

            # Start a fresh instance of the application
            process = run_app()
            
    # Handle Ctrl+C to gracefully close the application #######################
    ###########################################################################
    except KeyboardInterrupt:
        print("\n\nStopping development mode...")
        
        # Check if the process is still running
        if process.poll() is None:
            # Attempt graceful termination
            process.terminate()
            try:
                # Wait up to 3 seconds for graceful shutdown
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                # Force kill if graceful shutdown fails
                process.kill()
                # Wait for the kill to complete
                process.wait()
        print("Done.")


if __name__ == "__main__":
    main()
