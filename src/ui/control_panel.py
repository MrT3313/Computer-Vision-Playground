from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QSpinBox, QComboBox, QPushButton, QGroupBox
)
from PySide6.QtCore import Signal

from src.core.kernel_config import KernelConfig
from src.ui.kernel_grid_widget import KernelGridWidget


class ControlPanel(QWidget):
    grid_size_changed = Signal(int)
    kernel_size_changed = Signal(int)
    filter_type_changed = Signal(str)
    kernel_value_changed = Signal()
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
        self.grid_size_spin.setMinimum(5)
        self.grid_size_spin.setMaximum(50)
        self.grid_size_spin.setValue(10)
        self.grid_size_spin.valueChanged.connect(self.grid_size_changed.emit)
        grid_size_layout.addWidget(self.grid_size_spin)
        grid_layout.addLayout(grid_size_layout)
        
        grid_group.setLayout(grid_layout)
        layout.addWidget(grid_group)
        
        kernel_group = QGroupBox("Kernel Configuration")
        kernel_layout = QVBoxLayout()
        
        kernel_size_layout = QHBoxLayout()
        kernel_size_layout.addWidget(QLabel("Kernel Size:"))
        self.kernel_size_combo = QComboBox()
        self.kernel_size_combo.addItems(["3x3", "5x5", "7x7", "9x9"])
        self.kernel_size_combo.currentTextChanged.connect(self._on_kernel_size_changed)
        kernel_size_layout.addWidget(self.kernel_size_combo)
        kernel_layout.addLayout(kernel_size_layout)
        
        filter_type_layout = QHBoxLayout()
        filter_type_layout.addWidget(QLabel("Filter Type:"))
        self.filter_type_combo = QComboBox()
        self.filter_type_combo.addItems(
            [
                "Mean",
                # "Blur",
                # "Sharpen", 
                # "Custom"
            ]
        )
        self.filter_type_combo.currentTextChanged.connect(self.filter_type_changed.emit)
        filter_type_layout.addWidget(self.filter_type_combo)
        kernel_layout.addLayout(filter_type_layout)
        
        self.kernel_values_label = QLabel("Kernel Values:")
        kernel_layout.addWidget(self.kernel_values_label)
        
        self.kernel_grid = KernelGridWidget(self.kernel_config)
        self.kernel_grid.value_changed.connect(self.kernel_value_changed.emit)
        kernel_layout.addWidget(self.kernel_grid)
        
        self.update_kernel_values_state("Mean")
        
        kernel_group.setLayout(kernel_layout)
        layout.addWidget(kernel_group)
        
        nav_group = QGroupBox("Navigation")
        nav_layout = QVBoxLayout()
        
        self.position_label = QLabel("Position: 0 / 0")
        nav_layout.addWidget(self.position_label)
        
        nav_buttons_layout = QHBoxLayout()
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_position.emit)
        nav_buttons_layout.addWidget(self.reset_button)
        
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.previous_position.emit)
        nav_buttons_layout.addWidget(self.prev_button)
        
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_position.emit)
        nav_buttons_layout.addWidget(self.next_button)
        
        nav_layout.addLayout(nav_buttons_layout)
        
        nav_group.setLayout(nav_layout)
        layout.addWidget(nav_group)
        
        layout.addStretch()
    
    def _on_kernel_size_changed(self, text: str):
        kernel_size = int(text.split('x')[0])
        self.kernel_size_changed.emit(kernel_size)
    
    def update_position_label(self, current: int, total: int):
        self.position_label.setText(f"Position: {current + 1} / {total}")
    
    def enable_navigation(self, enabled: bool):
        self.prev_button.setEnabled(enabled)
        self.next_button.setEnabled(enabled)
        self.reset_button.setEnabled(enabled)
    
    def update_kernel_grid(self):
        self.kernel_grid.update_size()
        self.kernel_grid.update()
    
    def update_kernel_values_state(self, filter_type: str):
        if filter_type == "Mean":
            self.kernel_grid.setEnabled(False)
            self.kernel_values_label.setText("Kernel Values: (disabled for Mean filter)")
            self.kernel_values_label.setStyleSheet("color: gray;")
        else:
            self.kernel_grid.setEnabled(True)
            self.kernel_values_label.setText("Kernel Values:")
            self.kernel_values_label.setStyleSheet("")
