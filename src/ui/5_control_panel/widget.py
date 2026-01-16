from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QGroupBox
from PySide6.QtCore import Signal
from consts import DEFAULT_GRID_SIZE, MIN_GRID_SIZE, MAX_GRID_SIZE


class ControlPanelWidget(QWidget):
    # Signal emitted when the grid size value changes, passes the new grid size as an integer
    grid_size_changed = Signal(int)
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
    
    def _setup_ui(self):
        # Create the main vertical layout for the control panel
        layout = QVBoxLayout(self)
        
        # Create a group box to contain grid configuration controls
        grid_group = QGroupBox("Grid Configuration")
        grid_layout = QVBoxLayout()
        
        # Create a horizontal layout for the grid size control row
        grid_size_layout = QHBoxLayout()
        grid_size_layout.addWidget(QLabel("Grid Size:"))

        # Create spin box for grid size input
        self.grid_size_spin = QSpinBox()
        self.grid_size_spin.setMinimum(MIN_GRID_SIZE)
        self.grid_size_spin.setMaximum(MAX_GRID_SIZE)
        self.grid_size_spin.setValue(DEFAULT_GRID_SIZE)
        self.grid_size_spin.valueChanged.connect(self.grid_size_changed.emit)
        grid_size_layout.addWidget(self.grid_size_spin)
        
        # Add the grid size control row to the grid configuration layout
        grid_layout.addLayout(grid_size_layout)
        
        # Set the layout for the grid configuration group box
        grid_group.setLayout(grid_layout)
        
        # Add the grid configuration group to the main layout
        layout.addWidget(grid_group)
        layout.addStretch() # Add stretchable space at the bottom to push controls to the top
