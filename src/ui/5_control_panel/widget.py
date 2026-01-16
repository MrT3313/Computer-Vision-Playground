from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox
from PySide6.QtCore import Signal
from consts import DEFAULT_GRID_SIZE, MIN_GRID_SIZE, MAX_GRID_SIZE
from ui.common.number_input import NumberInputWidget


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
        
        # Create number input widget for grid size
        self.grid_size_input = NumberInputWidget(
            label="Grid Size:",
            default_value=DEFAULT_GRID_SIZE,
            min_value=MIN_GRID_SIZE,
            max_value=MAX_GRID_SIZE
        )
        self.grid_size_input.value_changed.connect(self.grid_size_changed.emit)
        grid_layout.addWidget(self.grid_size_input)
        
        # Set the layout for the grid configuration group box
        grid_group.setLayout(grid_layout)
        
        # Add the grid configuration group to the main layout
        layout.addWidget(grid_group)
        layout.addStretch() # Add stretchable space at the bottom to push controls to the top
