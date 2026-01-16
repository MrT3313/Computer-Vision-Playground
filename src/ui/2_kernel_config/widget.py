from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class KernelConfigWidget(QFrame):
    def __init__(self):
        super().__init__()
        self._setup_ui()
    
    def _setup_ui(self):
        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(2)
        self.setStyleSheet("background-color: grey;")
        self.setMinimumHeight(200)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        title_bar = QFrame()
        title_bar.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border-bottom: 1px solid rgba(0, 0, 0, 0.3);")
        title_bar.setFixedHeight(30)
        
        title_layout = QVBoxLayout(title_bar)
        title_layout.setContentsMargins(5, 0, 5, 0)
        
        title_label = QLabel("2. Kernel Config")
        title_label.setStyleSheet("font-size: 12px; font-weight: bold; background: transparent; border: none;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        title_layout.addWidget(title_label)
        
        content_area = QFrame()
        content_area.setStyleSheet("background: transparent; border: none;")
        
        main_layout.addWidget(title_bar)
        main_layout.addWidget(content_area, 1)
