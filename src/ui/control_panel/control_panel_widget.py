from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QSpinBox, QComboBox, QPushButton, QGroupBox, QCheckBox
)
from PySide6.QtCore import Signal

from src.core.filter_config import KernelConfig
from src.consts.defaults import (
    DEFAULT_GRID_SIZE,
    DEFAULT_GRID_SIZE_MIN,
    DEFAULT_GRID_SIZE_MAX,
    DEFAULT_SHOW_COLORS,
    DEFAULT_SHOW_PIXEL_VALUES,
)


class ControlPanel(QWidget):
    grid_size_changed = Signal(int)
    show_colors_changed = Signal(bool)
    show_pixel_values_changed = Signal(bool)
    category_changed = Signal(str)
    operation_type_changed = Signal(str)
    filter_selection_changed = Signal(str)
    kernel_value_changed = Signal()
    raw_image_mode_changed = Signal(str)
    previous_position = Signal()
    next_position = Signal()
    reset_position = Signal()
    
    def __init__(self, kernel_config: KernelConfig, parent=None):
        super().__init__(parent)
        self.kernel_config = kernel_config
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        grid_group = QGroupBox("Grid Configuration")
        grid_layout = QVBoxLayout()
        
        grid_size_layout = QHBoxLayout()
        grid_size_layout.addWidget(QLabel("Grid Size:"))
        self.grid_size_spin = QSpinBox()
        self.grid_size_spin.setMinimum(DEFAULT_GRID_SIZE_MIN)
        self.grid_size_spin.setMaximum(DEFAULT_GRID_SIZE_MAX)
        self.grid_size_spin.setValue(DEFAULT_GRID_SIZE)
        self.grid_size_spin.valueChanged.connect(self.grid_size_changed.emit)
        grid_size_layout.addWidget(self.grid_size_spin)
        grid_layout.addLayout(grid_size_layout)
        
        self.show_colors_checkbox = QCheckBox("Show Colors")
        self.show_colors_checkbox.setChecked(DEFAULT_SHOW_COLORS)
        self.show_colors_checkbox.stateChanged.connect(
            lambda state: self.show_colors_changed.emit(state == 2)
        )
        grid_layout.addWidget(self.show_colors_checkbox)
        
        self.show_pixel_values_checkbox = QCheckBox("Show Pixel Values")
        self.show_pixel_values_checkbox.setChecked(DEFAULT_SHOW_PIXEL_VALUES)
        self.show_pixel_values_checkbox.stateChanged.connect(
            lambda state: self.show_pixel_values_changed.emit(state == 2)
        )
        grid_layout.addWidget(self.show_pixel_values_checkbox)
        
        grid_group.setLayout(grid_layout)
        layout.addWidget(grid_group)
        
        raw_image_group = QGroupBox("Input Image Configuration")
        raw_image_layout = QVBoxLayout()
        
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("Mode:"))
        self.raw_image_mode_combo = QComboBox()
        self.raw_image_mode_combo.addItems(["Toggle", "Custom"])
        self.raw_image_mode_combo.currentTextChanged.connect(self.raw_image_mode_changed.emit)
        mode_layout.addWidget(self.raw_image_mode_combo)
        raw_image_layout.addLayout(mode_layout)
        
        raw_image_group.setLayout(raw_image_layout)
        layout.addWidget(raw_image_group)
        
        kernel_group = QGroupBox("Filter Configuration")
        kernel_layout = QVBoxLayout()
        
        category_layout = QHBoxLayout()
        category_layout.addWidget(QLabel("Category:"))
        self.category_combo = QComboBox()
        self.category_combo.addItems(["Linear", "Non-Linear"])
        self.category_combo.currentTextChanged.connect(self._on_category_changed)
        category_layout.addWidget(self.category_combo)
        kernel_layout.addLayout(category_layout)
        
        operation_type_layout = QHBoxLayout()
        operation_type_layout.addWidget(QLabel("Type:"))
        self.operation_type_combo = QComboBox()
        self.operation_type_combo.addItems(["Convolution", "Cross-Correlation"])
        self.operation_type_combo.currentTextChanged.connect(self.operation_type_changed.emit)
        operation_type_layout.addWidget(self.operation_type_combo)
        kernel_layout.addLayout(operation_type_layout)
        
        filter_selection_layout = QHBoxLayout()
        filter_selection_layout.addWidget(QLabel("Filter Selection:"))
        self.filter_selection_combo = QComboBox()
        self.filter_selection_combo.addItems(["Mean", "Custom"])
        self.filter_selection_combo.currentTextChanged.connect(self.filter_selection_changed.emit)
        filter_selection_layout.addWidget(self.filter_selection_combo)
        kernel_layout.addLayout(filter_selection_layout)
        
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
        
        layout.addStretch()
    
    def _on_category_changed(self, category: str):
        if category == "Linear":
            self.operation_type_combo.setVisible(True)
            self.filter_selection_combo.clear()
            self.filter_selection_combo.addItems(["Mean", "Custom"])
        else:
            self.operation_type_combo.setVisible(False)
            self.filter_selection_combo.clear()
            self.filter_selection_combo.addItems(["Median"])
        
        self.category_changed.emit(category)
    
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
