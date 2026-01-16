from PySide6.QtWidgets import QFrame, QVBoxLayout, QGroupBox, QWidget, QLabel, QSizePolicy
from PySide6.QtCore import Qt

from core.kernel_grid import KernelGridModel
from .kernel_grid_widget import KernelGridWidget
from .final_kernel_grid_widget import FinalKernelGridWidget
from ui.common.number_input import NumberInputWidget
from consts import (
    DEFAULT_KERNEL_SIZE, MIN_KERNEL_SIZE, MAX_KERNEL_SIZE,
    DEFAULT_CONSTANT_MULTIPLIER, MIN_CONSTANT_MULTIPLIER, MAX_CONSTANT_MULTIPLIER,
    CONSTANT_MULTIPLIER_STEP, CONSTANT_MULTIPLIER_DECIMALS
)

class KernelConfigWidget(QFrame):
    def __init__(self):
        super().__init__()
        # Initialize the kernel grid model with default size (2k+1 where k is the kernel radius)
        self._kernel_model = KernelGridModel(2 * DEFAULT_KERNEL_SIZE + 1)
        self._setup_ui()
    
    def _setup_ui(self):
        # Configure the frame's visual appearance with a box border
        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(2) # Set border thickness to 2 pixels
        
        # Create the main vertical layout that will contain all child widgets
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0) # Remove padding around edges
        main_layout.setSpacing(0) # Remove spacing between child widgets
        
        # Create the title bar frame at the top of the panel
        title_bar = QFrame()
        title_bar.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border-bottom: 1px solid rgba(0, 0, 0, 0.3);")
        title_bar.setFixedHeight(30) # Fixed height of 30 pixels for title bar
        
        # Create layout for the title bar to hold the title label
        title_layout = QVBoxLayout(title_bar)
        title_layout.setContentsMargins(5, 0, 5, 0) # Add 5px padding on left and right
        
        # Create the title label
        title_label = QLabel("2. Kernel Config")
        title_label.setStyleSheet("font-size: 12px; font-weight: bold; background: transparent; border: none;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter) # Align text to the left and vertically centered
        
        # Add the title label to the title bar layout
        title_layout.addWidget(title_label)
        
        # Create the content area widget that will hold all kernel configuration controls
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(10, 10, 10, 10) # Add 10px padding on all sides
        content_layout.setSpacing(10) # Add 10px spacing between widgets
        
        # Create group box for kernel size configuration
        kernel_size_group = QGroupBox()
        kernel_size_group.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        kernel_size_group_layout = QVBoxLayout()
        # Create number input widget for kernel size (k) parameter
        self.kernel_size_input = NumberInputWidget(
            label="Kernel Size (k):",
            default_value=DEFAULT_KERNEL_SIZE,
            min_value=MIN_KERNEL_SIZE,
            max_value=MAX_KERNEL_SIZE
        )
        # Connect value changes to handler that updates the kernel grid size
        self.kernel_size_input.value_changed.connect(self._on_kernel_size_changed)
        kernel_size_group_layout.addWidget(self.kernel_size_input)
        kernel_size_group.setLayout(kernel_size_group_layout)
        content_layout.addWidget(kernel_size_group)
        
        # Create the editable kernel grid widget where users can click to modify values
        self.kernel_grid = KernelGridWidget(self._kernel_model)
        content_layout.addWidget(self.kernel_grid, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Create group box for constant multiplier configuration
        constant_group = QGroupBox()
        constant_group.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        constant_group_layout = QVBoxLayout()
        # Create number input widget for constant multiplier with decimal precision
        self.constant_input = NumberInputWidget(
            label="Constant:",
            default_value=DEFAULT_CONSTANT_MULTIPLIER,
            min_value=MIN_CONSTANT_MULTIPLIER,
            max_value=MAX_CONSTANT_MULTIPLIER,
            step=CONSTANT_MULTIPLIER_STEP,
            decimals=CONSTANT_MULTIPLIER_DECIMALS
        )
        # Connect value changes to handler that updates the final kernel display
        self.constant_input.value_changed.connect(self._on_constant_changed)
        constant_group_layout.addWidget(self.constant_input)
        constant_group.setLayout(constant_group_layout)
        content_layout.addWidget(constant_group)
        
        # Create the final kernel grid widget that displays kernel values multiplied by constant
        self.final_kernel_grid = FinalKernelGridWidget(self._kernel_model, DEFAULT_CONSTANT_MULTIPLIER)
        content_layout.addWidget(self.final_kernel_grid, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Add both the title bar and content area to the main layout
        main_layout.addWidget(title_bar) # Title bar at the top
        main_layout.addWidget(content_area, 1) # Content area below with stretch factor 1
    
    def _on_kernel_size_changed(self, k: int) -> None:
        # Convert kernel radius (k) to full grid size (2k+1) and update the model
        grid_size = 2 * k + 1
        self._kernel_model.set_grid_size(grid_size)
    
    def _on_constant_changed(self, value: float) -> None:
        # Update the constant multiplier in the final kernel grid display
        self.final_kernel_grid.set_constant(value)
    
    def set_filter(self, filter_name: str) -> None:
        if filter_name == "Mean":
            self._kernel_model.set_all_values(1.0)
            self.kernel_grid.setEnabled(False)
            self.kernel_grid.setToolTip("Mean filter uses a fixed kernel with all values set to 1")
            self.constant_input.set_value(1.0)
        else:
            self.kernel_grid.setEnabled(True)
            self.kernel_grid.setToolTip("")