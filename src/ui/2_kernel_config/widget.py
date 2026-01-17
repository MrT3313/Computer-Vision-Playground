from PySide6.QtWidgets import QFrame, QVBoxLayout, QGroupBox, QWidget, QLabel, QSizePolicy
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QImage
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import io

from core.kernel_grid import KernelGridModel
from .kernel_grid_widget import KernelGridWidget
from .final_kernel_grid_widget import FinalKernelGridWidget
from ui.common.number_input import NumberInputWidget
from ui.common.dropdown import DropdownWidget
from consts import (
    DEFAULT_KERNEL_SIZE, MIN_KERNEL_SIZE, MAX_KERNEL_SIZE,
    DEFAULT_CONSTANT_MULTIPLIER, MIN_CONSTANT_MULTIPLIER, MAX_CONSTANT_MULTIPLIER,
    CONSTANT_MULTIPLIER_STEP, CONSTANT_MULTIPLIER_DECIMALS,
    DEFAULT_KERNEL_PRESET, KERNEL_PRESETS,
    DEFAULT_KERNEL_VALUE
)

class KernelConfigWidget(QFrame):
    def __init__(self):
        super().__init__()
        # Initialize the kernel grid model with default size (2k+1 where k is the kernel radius)
        self._kernel_model = KernelGridModel(2 * DEFAULT_KERNEL_SIZE + 1)
        # Store current sigma value for Gaussian filter
        self._sigma = 1.0
        # Store current normalize setting for Gaussian filter
        self._normalize = True
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
        
        # Add kernel preset dropdown to the same group box
        self.kernel_preset_dropdown = DropdownWidget(
            label="Kernel Preset:",
            options=KERNEL_PRESETS,
            default_option=DEFAULT_KERNEL_PRESET
        )
        self.kernel_preset_dropdown.value_changed.connect(self._on_preset_changed)
        kernel_size_group_layout.addWidget(self.kernel_preset_dropdown)
        
        kernel_size_group.setLayout(kernel_size_group_layout)
        content_layout.addWidget(kernel_size_group)
        
        # Create Gaussian formula display widget (initially hidden)
        self.gaussian_formula_label = QLabel()
        self.gaussian_formula_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gaussian_formula_label.setVisible(False)
        self.gaussian_formula_label.setContentsMargins(0, 0, 0, 0)
        self.gaussian_formula_label.setStyleSheet("padding: 0px; margin: 0px;")
        self._render_gaussian_formula()
        content_layout.addWidget(self.gaussian_formula_label, 0, Qt.AlignmentFlag.AlignCenter)
        
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
        self.kernel_preset_dropdown.set_value(DEFAULT_KERNEL_PRESET)
    
    def _on_constant_changed(self, value: float) -> None:
        # Update the constant multiplier in the final kernel grid display
        self.final_kernel_grid.set_constant(value)
    
    def _on_preset_changed(self, preset_name: str) -> None:
        if preset_name == "Identity":
            self._apply_identity_preset()
        elif preset_name == DEFAULT_KERNEL_PRESET:
            self._kernel_model.set_all_values(DEFAULT_KERNEL_VALUE)
    
    def _apply_identity_preset(self) -> None:
        size = self._kernel_model.get_grid_size()
        center = size // 2
        for row in range(size):
            for col in range(size):
                value = 1.0 if (row == center and col == center) else 0.0
                self._kernel_model.set_cell(row, col, value)
    
    def set_filter(self, filter_name: str) -> None:
        if filter_name == "Mean":
            self._kernel_model.set_all_values(DEFAULT_KERNEL_VALUE)
            self.kernel_grid.setEnabled(False)
            self.kernel_grid.setToolTip("Mean filter uses a fixed kernel with all values set to 1")
            self.constant_input.set_value(DEFAULT_CONSTANT_MULTIPLIER)
            self.kernel_preset_dropdown.set_value(DEFAULT_KERNEL_PRESET)
            self.kernel_preset_dropdown.combobox.setEnabled(False)
            self.gaussian_formula_label.setVisible(False)
        elif filter_name == "Gaussian":
            self.kernel_grid.setEnabled(False)
            self.kernel_grid.setToolTip("Gaussian filter kernel values are auto-generated from the formula")
            self.kernel_preset_dropdown.set_value(DEFAULT_KERNEL_PRESET)
            self.kernel_preset_dropdown.combobox.setEnabled(False)
            self.gaussian_formula_label.setVisible(True)
            self._apply_gaussian_kernel()
        elif filter_name == "Custom":
            self.kernel_grid.setEnabled(True)
            self.kernel_grid.setToolTip("")
            self.kernel_preset_dropdown.combobox.setEnabled(True)
            self.gaussian_formula_label.setVisible(False)
        else:
            self.kernel_grid.setEnabled(True)
            self.kernel_grid.setToolTip("")
            self.kernel_preset_dropdown.set_value(DEFAULT_KERNEL_PRESET)
            self.kernel_preset_dropdown.combobox.setEnabled(False)
            self.gaussian_formula_label.setVisible(False)
    
    def set_profile(self, profile_name: str) -> None:
        if profile_name == "Shift Left":
            self._apply_shift_left_profile()
            self.kernel_preset_dropdown.set_value(DEFAULT_KERNEL_PRESET)
            self.kernel_preset_dropdown.combobox.setEnabled(False)
        elif profile_name == "Shift Right":
            self._apply_shift_right_profile()
            self.kernel_preset_dropdown.set_value(DEFAULT_KERNEL_PRESET)
            self.kernel_preset_dropdown.combobox.setEnabled(False)
        elif profile_name == DEFAULT_KERNEL_PRESET:
            self.kernel_preset_dropdown.combobox.setEnabled(True)
    
    def _apply_shift_left_profile(self) -> None:
        size = self._kernel_model.get_grid_size()
        middle_row = size // 2
        left_col = 0
        
        self._kernel_model.set_all_values(0.0)
        self._kernel_model.set_cell(middle_row, left_col, 1.0)
    
    def _apply_shift_right_profile(self) -> None:
        size = self._kernel_model.get_grid_size()
        middle_row = size // 2
        right_col = size - 1
        
        self._kernel_model.set_all_values(0.0)
        self._kernel_model.set_cell(middle_row, right_col, 1.0)
    
    def set_sigma(self, sigma: float) -> None:
        self._sigma = sigma
        self._apply_gaussian_kernel()
    
    def set_normalize(self, normalize: bool) -> None:
        self._normalize = normalize
        self._apply_gaussian_kernel()
    
    def _render_gaussian_formula(self) -> None:
        formula = r'$G_\sigma = \frac{1}{2\pi\sigma^2} e^{- \, \frac{(x^2+y^2)}{2\sigma^2}}$'
        pixmap = self._latex_to_pixmap(formula)
        self.gaussian_formula_label.setPixmap(pixmap)
    
    def _latex_to_pixmap(self, latex_str: str) -> QPixmap:
        fig = Figure(figsize=(2, 1), facecolor='white')
        canvas = FigureCanvasAgg(fig)
        ax = fig.add_subplot(111)
        ax.axis('off')
        
        ax.text(0.5, 0.5, latex_str, 
                horizontalalignment='center',
                verticalalignment='center',
                fontsize=12,
                transform=ax.transAxes)
        
        canvas.draw()
        
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', pad_inches=0, facecolor='white')
        buf.seek(0)
        
        plt.close(fig)
        
        img = QImage()
        img.loadFromData(buf.read())
        
        return QPixmap.fromImage(img)
    
    def _apply_gaussian_kernel(self) -> None:
        import math
        
        size = self._kernel_model.get_grid_size()
        center = size // 2
        sigma_squared = self._sigma * self._sigma
        coefficient = 1.0 / (2.0 * math.pi * sigma_squared)
        
        kernel_sum = 0.0
        temp_values = []
        
        for row in range(size):
            row_values = []
            for col in range(size):
                x = col - center
                y = row - center
                exponent = -(x * x + y * y) / (2.0 * sigma_squared)
                value = coefficient * math.exp(exponent)
                row_values.append(value)
                kernel_sum += value
            temp_values.append(row_values)
        
        for row in range(size):
            for col in range(size):
                value = temp_values[row][col]
                if self._normalize and kernel_sum > 0:
                    value = value / kernel_sum
                self._kernel_model.set_cell(row, col, value)