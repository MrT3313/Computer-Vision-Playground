from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QWidget
from PySide6.QtCore import Qt
from typing import Optional


class TitleBarWidget(QFrame):
    def __init__(self, title: str, right_widget: Optional[QWidget] = None):
        super().__init__()
        self._setup_ui(title, right_widget)
    
    def _setup_ui(self, title: str, right_widget: Optional[QWidget]) -> None:
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border-bottom: 1px solid rgba(0, 0, 0, 0.3);")
        self.setFixedHeight(30)
        
        if right_widget:
            layout = QHBoxLayout(self)
            layout.setContentsMargins(5, 0, 5, 0)
            layout.setSpacing(5)
        else:
            layout = QVBoxLayout(self)
            layout.setContentsMargins(5, 0, 5, 0)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 12px; font-weight: bold; background: transparent; border: none;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(title_label)
        
        if right_widget:
            layout.addStretch()
            layout.addWidget(right_widget)
