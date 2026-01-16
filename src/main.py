import sys
import signal
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Computer Vision Playground")
    
    signal.signal(signal.SIGINT, lambda *args: app.quit())
    timer = QTimer()
    timer.timeout.connect(lambda: None)
    timer.start(100)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
