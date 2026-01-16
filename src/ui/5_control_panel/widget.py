from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QGroupBox
from PySide6.QtCore import Signal
from consts import DEFAULT_GRID_SIZE, MIN_GRID_SIZE, MAX_GRID_SIZE


class ControlPanelWidget(QWidget):
    grid_size_changed = Signal(int)
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        grid_group = QGroupBox("Grid Configuration")
        grid_layout = QVBoxLayout()
        
        grid_size_layout = QHBoxLayout()
        grid_size_layout.addWidget(QLabel("Grid Size:"))
        self.grid_size_spin = QSpinBox()
        self.grid_size_spin.setMinimum(MIN_GRID_SIZE)
        self.grid_size_spin.setMaximum(MAX_GRID_SIZE)
        self.grid_size_spin.setValue(DEFAULT_GRID_SIZE)
        self.grid_size_spin.valueChanged.connect(self.grid_size_changed.emit)
        grid_size_layout.addWidget(self.grid_size_spin)
        grid_layout.addLayout(grid_size_layout)
        
        grid_group.setLayout(grid_layout)
        layout.addWidget(grid_group)
        layout.addStretch()
