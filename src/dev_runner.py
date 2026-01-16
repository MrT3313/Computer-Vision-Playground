#!/usr/bin/env python3

import sys
import subprocess
import time
from pathlib import Path
from watchfiles import watch


def run_app():
    return subprocess.Popen(
        [sys.executable, "src/main.py"],
        cwd=Path(__file__).parent.parent,
    )


def main():
    print("Starting development mode with auto-restart...")
    print("Watching for changes in src/...")
    print("Press Ctrl+C to stop\n")
    
    process = run_app()
    
    try:
        for changes in watch(
            Path(__file__).parent,
            watch_filter=lambda change, path: path.endswith('.py') and '__pycache__' not in path
        ):
            print(f"\n{'='*60}")
            print("Changes detected:")
            for change_type, path in changes:
                print(f"  - {Path(path).relative_to(Path.cwd())}")
            print(f"{'='*60}")
            print("Restarting application...\n")
            
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
            
            time.sleep(0.2)
            process = run_app()
            
    except KeyboardInterrupt:
        print("\n\nStopping development mode...")
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
        print("Done.")


if __name__ == "__main__":
    main()
