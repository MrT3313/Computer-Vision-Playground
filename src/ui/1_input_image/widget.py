from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class InputImageWidget(QFrame):
    def __init__(self):
        super().__init__()
        self._setup_ui()
    
    def _setup_ui(self):
        # Configure the frame's visual appearance with a box border
        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(2) # Set border thickness to 2 pixels
        self.setStyleSheet("background-color: grey;") # Set background color
        self.setMinimumSize(200, 200) # Ensure minimum size of 200x200 pixels
        
        # Create the main vertical layout that will contain all child widgets
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0) # Remove padding around edges
        main_layout.setSpacing(0) # Remove spacing between child widgets
        
        # Create the title bar frame at the top of the panel
        title_bar = QFrame()
        title_bar.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border-bottom: 1px solid rgba(0, 0, 0, 0.3);")
        title_bar.setFixedHeight(30) # Fixed height of 30 pixels for title bar
        
        # Create layout for the title bar to hold the title label
        title_layout = QVBoxLayout(title_bar)
        title_layout.setContentsMargins(5, 0, 5, 0) # Add 5px padding on left and right
        
        # Create the title label
        title_label = QLabel("1. Input Image")
        title_label.setStyleSheet("font-size: 12px; font-weight: bold; background: transparent; border: none;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter) # Align text to the left and vertically centered
        
        # Add the title label to the title bar layout
        title_layout.addWidget(title_label)
        
        # Create the content area frame that will hold the main panel content
        content_area = QFrame()
        content_area.setStyleSheet("background: transparent; border: none;")
        
        # Add both the title bar and content area to the main layout
        main_layout.addWidget(title_bar) # Title bar at the top
        main_layout.addWidget(content_area, 1) # Content area below with stretch factor 1
