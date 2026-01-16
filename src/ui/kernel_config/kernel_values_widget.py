from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QDoubleSpinBox
from PySide6.QtCore import Signal, Qt

from src.core.filter_config import KernelConfig
from src.ui.control_panel.kernel_grid_widget import KernelGridWidget
from src.ui.kernel_config.final_kernel_grid_widget import FinalKernelGridWidget
from src.consts.defaults import (
    DEFAULT_CONSTANT_MULTIPLIER,
    DEFAULT_CONSTANT_MULTIPLIER_MIN,
    DEFAULT_CONSTANT_MULTIPLIER_MAX,
    DEFAULT_CONSTANT_MULTIPLIER_STEP,
    DEFAULT_CONSTANT_MULTIPLIER_DECIMALS,
)


class KernelValuesWidget(QWidget):
    value_changed = Signal()
    kernel_size_changed = Signal(int)
    constant_changed = Signal(float)
    
    def __init__(self, kernel_config: KernelConfig, parent=None):
        super().__init__(parent)
        self.kernel_config = kernel_config
        self.constant = DEFAULT_CONSTANT_MULTIPLIER
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        kernel_size_layout = QHBoxLayout()
        kernel_size_layout.addStretch()
        kernel_size_layout.addWidget(QLabel("Kernel Size:"))
        self.kernel_size_combo = QComboBox()
        self.kernel_size_combo.addItems(["3x3", "5x5", "7x7", "9x9"])
        self.kernel_size_combo.currentTextChanged.connect(self._on_kernel_size_changed)
        kernel_size_layout.addWidget(self.kernel_size_combo)
        kernel_size_layout.addStretch()
        layout.addLayout(kernel_size_layout)
        
        layout.addSpacing(10)
        
        self.lock_label = QLabel("Fixed values (Mean filter)")
        self.lock_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lock_label.setStyleSheet("color: #888; font-style: italic; padding: 5px;")
        self.lock_label.setVisible(False)
        layout.addWidget(self.lock_label)
        
        self.kernel_grid = KernelGridWidget(self.kernel_config)
        self.kernel_grid.value_changed.connect(self._on_kernel_value_changed)
        layout.addWidget(self.kernel_grid, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addSpacing(10)
        
        constant_layout = QHBoxLayout()
        constant_layout.addStretch()
        constant_layout.addWidget(QLabel("Constant Multiplier:"))
        self.constant_spin = QDoubleSpinBox()
        self.constant_spin.setRange(DEFAULT_CONSTANT_MULTIPLIER_MIN, DEFAULT_CONSTANT_MULTIPLIER_MAX)
        self.constant_spin.setValue(DEFAULT_CONSTANT_MULTIPLIER)
        self.constant_spin.setSingleStep(DEFAULT_CONSTANT_MULTIPLIER_STEP)
        self.constant_spin.setDecimals(DEFAULT_CONSTANT_MULTIPLIER_DECIMALS)
        self.constant_spin.valueChanged.connect(self._on_constant_changed)
        constant_layout.addWidget(self.constant_spin)
        constant_layout.addStretch()
        layout.addLayout(constant_layout)
        
        layout.addSpacing(10)
        
        self.final_kernel_grid = FinalKernelGridWidget(self.kernel_config, self.constant)
        layout.addWidget(self.final_kernel_grid, alignment=Qt.AlignmentFlag.AlignCenter)
    
    def update_kernel_grid(self):
        self.kernel_grid.update_size()
        self.kernel_grid.update()
        self.final_kernel_grid.update_size()
        self.final_kernel_grid.update()
    
    def update_kernel_values_state(self, category: str, filter_selection: str):
        if category == "Linear" and filter_selection == "Custom":
            self.kernel_grid.setEnabled(True)
            self.kernel_grid.setToolTip("Click cells to edit kernel values")
            self.lock_label.setVisible(False)
        else:
            self.kernel_grid.setEnabled(False)
            if filter_selection == "Mean":
                self.kernel_grid.setToolTip("Kernel values are fixed for Mean filter (all values are 1)")
                self.lock_label.setText("Fixed values (Mean filter)")
                self.lock_label.setVisible(True)
            elif filter_selection == "Median":
                self.kernel_grid.setToolTip("Kernel values are not used for Median filter")
                self.lock_label.setText("Not used (Median filter)")
                self.lock_label.setVisible(True)
            else:
                self.kernel_grid.setToolTip("Kernel values cannot be edited in this mode")
                self.lock_label.setVisible(False)
    
    def set_constant(self, value: float):
        self.constant = value
        self.constant_spin.setValue(value)
        self.final_kernel_grid.set_constant(value)
    
    def _on_kernel_size_changed(self, text: str):
        kernel_size = int(text.split('x')[0])
        self.kernel_size_changed.emit(kernel_size)
    
    def _on_constant_changed(self, value: float):
        self.constant = value
        self.final_kernel_grid.set_constant(value)
        self.constant_changed.emit(value)
    
    def _on_kernel_value_changed(self):
        self.final_kernel_grid.update()
        self.value_changed.emit()
