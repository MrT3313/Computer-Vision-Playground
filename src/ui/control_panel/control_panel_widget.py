from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QSpinBox, QComboBox, QPushButton, QGroupBox
)
from PySide6.QtCore import Signal

from src.core.kernel_config import KernelConfig
from src.ui.control_panel.kernel_grid_widget import KernelGridWidget


class ControlPanel(QWidget):
    """
    Control panel for configuring the convolution playground settings.
    
    Provides controls for:
    - Grid size (input image dimensions)
    - Kernel size (filter window size)
    - Filter type (mean, blur, etc.)
    - Kernel values (custom filter weights)
    - Navigation through kernel positions
    
    Signals:
        grid_size_changed: Emitted when grid size changes (int: new size)
        kernel_size_changed: Emitted when kernel size changes (int: new size)
        filter_type_changed: Emitted when filter type changes (str: filter name)
        kernel_value_changed: Emitted when any kernel value is edited
        previous_position: Emitted when user clicks Previous button
        next_position: Emitted when user clicks Next button
        reset_position: Emitted when user clicks Reset button
    """
    grid_size_changed = Signal(int)
    kernel_size_changed = Signal(int)
    filter_type_changed = Signal(str)
    kernel_value_changed = Signal()
    previous_position = Signal()
    next_position = Signal()
    reset_position = Signal()
    
    def __init__(self, kernel_config: KernelConfig, parent=None):
        """
        Initialize the control panel.
        
        Args:
            kernel_config: Kernel configuration object to manage
            parent: Optional parent widget
        """
        super().__init__(parent)
        self.kernel_config = kernel_config
        self.setup_ui()
    
    def setup_ui(self):
        """
        Create and arrange all UI components for the control panel.
        Organized into three groups: Grid Configuration, Kernel Configuration, and Navigation.
        """
        layout = QVBoxLayout(self)
        
        # === Grid Configuration Section ===
        grid_group = QGroupBox("Grid Configuration")
        grid_layout = QVBoxLayout()
        
        # Spinner to control the size of the input image (5x5 to 50x50)
        grid_size_layout = QHBoxLayout()
        grid_size_layout.addWidget(QLabel("Grid Size:"))
        self.grid_size_spin = QSpinBox()
        self.grid_size_spin.setMinimum(5)
        self.grid_size_spin.setMaximum(50)
        self.grid_size_spin.setValue(10)  # Default 10x10 grid
        self.grid_size_spin.valueChanged.connect(self.grid_size_changed.emit)
        grid_size_layout.addWidget(self.grid_size_spin)
        grid_layout.addLayout(grid_size_layout)
        
        grid_group.setLayout(grid_layout)
        layout.addWidget(grid_group)
        
        # === Kernel Configuration Section ===
        kernel_group = QGroupBox("Kernel Configuration")
        kernel_layout = QVBoxLayout()
        
        # Dropdown to select kernel size (3x3, 5x5, 7x7, or 9x9)
        kernel_size_layout = QHBoxLayout()
        kernel_size_layout.addWidget(QLabel("Kernel Size:"))
        self.kernel_size_combo = QComboBox()
        self.kernel_size_combo.addItems(["3x3", "5x5", "7x7", "9x9"])
        self.kernel_size_combo.currentTextChanged.connect(self._on_kernel_size_changed)
        kernel_size_layout.addWidget(self.kernel_size_combo)
        kernel_layout.addLayout(kernel_size_layout)
        
        # Dropdown to select filter type (currently only Mean is available)
        filter_type_layout = QHBoxLayout()
        filter_type_layout.addWidget(QLabel("Filter Type:"))
        self.filter_type_combo = QComboBox()
        self.filter_type_combo.addItems(
            [
                "Mean",
                # Future filter types can be added here:
                # "Blur",
                # "Sharpen", 
                # "Custom"
            ]
        )
        self.filter_type_combo.currentTextChanged.connect(self.filter_type_changed.emit)
        filter_type_layout.addWidget(self.filter_type_combo)
        kernel_layout.addLayout(filter_type_layout)
        
        # Label for the kernel values grid
        self.kernel_values_label = QLabel("Kernel Values:")
        kernel_layout.addWidget(self.kernel_values_label)
        
        # Interactive grid to edit kernel values (disabled for Mean filter)
        self.kernel_grid = KernelGridWidget(self.kernel_config)
        self.kernel_grid.value_changed.connect(self.kernel_value_changed.emit)
        kernel_layout.addWidget(self.kernel_grid)
        
        # Set initial state (Mean filter has kernel grid disabled)
        self.update_kernel_values_state("Mean")
        
        kernel_group.setLayout(kernel_layout)
        layout.addWidget(kernel_group)
        
        # === Navigation Section ===
        nav_group = QGroupBox("Navigation")
        nav_layout = QVBoxLayout()
        
        # Label showing current position out of total positions
        self.position_label = QLabel("Position: 0 / 0")
        nav_layout.addWidget(self.position_label)
        
        # Buttons to navigate through kernel positions
        nav_buttons_layout = QHBoxLayout()
        
        # Reset: Clear output and return to first position
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_position.emit)
        nav_buttons_layout.addWidget(self.reset_button)
        
        # Previous: Move kernel one position backward
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.previous_position.emit)
        nav_buttons_layout.addWidget(self.prev_button)
        
        # Next: Move kernel one position forward
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_position.emit)
        nav_buttons_layout.addWidget(self.next_button)
        
        nav_layout.addLayout(nav_buttons_layout)
        
        nav_group.setLayout(nav_layout)
        layout.addWidget(nav_group)
        
        # Add stretchy space at bottom to push controls to top
        layout.addStretch()
    
    def _on_kernel_size_changed(self, text: str):
        """
        Handle kernel size combo box changes.
        Parses "3x3" format and emits the numeric size.
        
        Args:
            text: Combo box text (e.g., "3x3", "5x5")
        """
        kernel_size = int(text.split('x')[0])  # Extract "3" from "3x3"
        self.kernel_size_changed.emit(kernel_size)
    
    def update_position_label(self, current: int, total: int):
        """
        Update the position display label.
        
        Args:
            current: Current position index (0-based, displayed as 1-based)
            total: Total number of positions
        """
        self.position_label.setText(f"Position: {current + 1} / {total}")
    
    def enable_navigation(self, enabled: bool):
        """
        Enable or disable navigation buttons.
        Disabled when kernel cannot fit on the image.
        
        Args:
            enabled: True to enable buttons, False to disable
        """
        self.prev_button.setEnabled(enabled)
        self.next_button.setEnabled(enabled)
        self.reset_button.setEnabled(enabled)
    
    def update_kernel_grid(self):
        """
        Refresh the kernel grid widget after size changes.
        Updates widget dimensions and redraws.
        """
        self.kernel_grid.update_size()
        self.kernel_grid.update()
    
    def update_kernel_values_state(self, filter_type: str):
        """
        Enable or disable kernel value editing based on filter type.
        Mean filter doesn't use custom kernel values, so editing is disabled.
        
        Args:
            filter_type: Type of filter selected
        """
        if filter_type == "Mean":
            # Mean filter doesn't use custom kernel values
            self.kernel_grid.setEnabled(False)
            self.kernel_values_label.setText("Kernel Values: (disabled for Mean filter)")
            self.kernel_values_label.setStyleSheet("color: gray;")
        else:
            # Other filters allow custom kernel values
            self.kernel_grid.setEnabled(True)
            self.kernel_values_label.setText("Kernel Values:")
            self.kernel_values_label.setStyleSheet("")
