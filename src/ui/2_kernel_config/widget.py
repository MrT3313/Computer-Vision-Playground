from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QDoubleSpinBox, QGroupBox, QWidget
from PySide6.QtCore import Qt

from core.kernel_grid import KernelGridModel
from ui.common.kernel_grid_widget import KernelGridWidget
from ui.common.final_kernel_grid_widget import FinalKernelGridWidget
from consts import (
    DEFAULT_KERNEL_SIZE, MIN_KERNEL_SIZE, MAX_KERNEL_SIZE,
    DEFAULT_CONSTANT_MULTIPLIER, MIN_CONSTANT_MULTIPLIER, MAX_CONSTANT_MULTIPLIER,
    CONSTANT_MULTIPLIER_STEP, CONSTANT_MULTIPLIER_DECIMALS
)

class KernelConfigWidget(QFrame):
    def __init__(self):
        super().__init__()
        self._kernel_model = KernelGridModel(2 * DEFAULT_KERNEL_SIZE + 1)
        self._setup_ui()
    
    def _setup_ui(self):
        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(2)
        
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
        
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(10)
        
        kernel_size_group = QGroupBox()
        kernel_size_group_layout = QVBoxLayout()
        kernel_size_layout = QHBoxLayout()
        kernel_size_layout.addWidget(QLabel("Kernel Size (k):"))
        self.kernel_size_spin = QSpinBox()
        self.kernel_size_spin.setMinimum(MIN_KERNEL_SIZE)
        self.kernel_size_spin.setMaximum(MAX_KERNEL_SIZE)
        self.kernel_size_spin.setValue(DEFAULT_KERNEL_SIZE)
        self.kernel_size_spin.valueChanged.connect(self._on_kernel_size_changed)
        kernel_size_layout.addWidget(self.kernel_size_spin)
        kernel_size_group_layout.addLayout(kernel_size_layout)
        kernel_size_group.setLayout(kernel_size_group_layout)
        content_layout.addWidget(kernel_size_group)
        
        self.kernel_grid = KernelGridWidget(self._kernel_model)
        content_layout.addWidget(self.kernel_grid, alignment=Qt.AlignmentFlag.AlignCenter)
        
        constant_group = QGroupBox()
        constant_group_layout = QVBoxLayout()
        constant_layout = QHBoxLayout()
        constant_layout.addWidget(QLabel("Constant:"))
        self.constant_spin = QDoubleSpinBox()
        self.constant_spin.setMinimum(MIN_CONSTANT_MULTIPLIER)
        self.constant_spin.setMaximum(MAX_CONSTANT_MULTIPLIER)
        self.constant_spin.setValue(DEFAULT_CONSTANT_MULTIPLIER)
        self.constant_spin.setSingleStep(CONSTANT_MULTIPLIER_STEP)
        self.constant_spin.setDecimals(CONSTANT_MULTIPLIER_DECIMALS)
        self.constant_spin.valueChanged.connect(self._on_constant_changed)
        constant_layout.addWidget(self.constant_spin)
        constant_group_layout.addLayout(constant_layout)
        constant_group.setLayout(constant_group_layout)
        content_layout.addWidget(constant_group)
        
        self.final_kernel_grid = FinalKernelGridWidget(self._kernel_model, DEFAULT_CONSTANT_MULTIPLIER)
        content_layout.addWidget(self.final_kernel_grid, alignment=Qt.AlignmentFlag.AlignCenter)
        
        main_layout.addWidget(title_bar)
        main_layout.addWidget(content_area, 1)
    
    def _on_kernel_size_changed(self, k: int) -> None:
        grid_size = 2 * k + 1
        self._kernel_model.set_grid_size(grid_size)
    
    def _on_constant_changed(self, value: float) -> None:
        self.final_kernel_grid.set_constant(value)
