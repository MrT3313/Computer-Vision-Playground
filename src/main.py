import sys
import signal
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    """
    Main entry point for the Computer Vision Playground application.
    Initializes the Qt application, sets up signal handling, and displays the main window.
    """

    # Create the Qt application instance
    # sys.argv passes command-line arguments to the application
    app = QApplication(sys.argv)

    # Set the application name
    app.setApplicationName("Computer Vision Playground")

    # Enable Ctrl+C handling - this tells Qt to quit on interrupt signals
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    # Create an instance of the main application window and show it on screen
    window = MainWindow()
    window.show()
    
    # Start the Qt event loop and exit with its return code when the app closes
    # exec() blocks here until the application quits
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
