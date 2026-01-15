from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QGridLayout, QLabel, QGroupBox, QScrollArea
)

from src.core.image_data import ImageData
from src.core.kernel_config import KernelConfig, KernelPosition
from src.core.filter_calculator import FilterCalculator
from src.ui.raw_input_image.raw_input_image_widget import RawInputImageWidget
from src.ui.kernel_values.kernel_values_widget import KernelValuesWidget
from src.ui.computed_pixel_values.computed_pixel_values_widget import ComputedPixelValuesWidget
from src.ui.control_panel.control_panel_widget import ControlPanel
from src.ui.work.work_section_widget import WorkSectionWidget


class MainWindow(QMainWindow):
    """
    Main application window for the Computer Vision Playground.
    
    Provides an interactive environment for learning convolution operations:
    1. Input image - draw black/white pixels with numeric values
    2. Computed values - see filter output values
    3. Control panel - configure kernel and navigate positions
    4. Work section - see step-by-step filter calculations
    
    The window coordinates all widgets and handles the convolution workflow.
    """
    
    def __init__(self, width = 10, height = 10):
        super().__init__()
        self.setWindowTitle("Computer Vision Playground")
        
        # CONFIGURATION #######################################################
        #######################################################################
        self.image_data = ImageData(width=width, height=height)
        
        self.output_data = ImageData(width=width, height=height)
        self.output_data.pixels = [[None for _ in range(width)] for _ in range(height)]
        
        self.kernel_config = KernelConfig(size=3)
        self.kernel_position = KernelPosition()
        
        # Initialize kernel with 1's for default Mean filter
        for r in range(self.kernel_config.size):
            for c in range(self.kernel_config.size):
                self.kernel_config.set_value(r, c, 1.0)

        # Filter configuration
        self.filter_calculator = FilterCalculator()
        
        # SETUP ###############################################################
        #######################################################################
        self.setup_ui()
        self.connect_signals()
        self.update_kernel_position()
        
    # SETUP METHODS ###########################################################
    ###########################################################################
    def setup_ui(self):
        """
        Create and arrange all UI components in the main window.
        
        Layout structure:
        - Left side: 3-column grid with input/kernel/computed (top row), work section (bottom)
        - Right side: Control panel
        """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Grid layout for the main visualization area (left side)
        grid_layout = QGridLayout()
        
        input_group = QGroupBox("Raw Input Image")
        input_layout = QVBoxLayout()
        input_scroll = QScrollArea()
        input_scroll.setWidgetResizable(False)
        self.input_grid = RawInputImageWidget(self.image_data)
        input_scroll.setWidget(self.input_grid)
        input_layout.addWidget(input_scroll)
        input_group.setLayout(input_layout)
        grid_layout.addWidget(input_group, 0, 0)
        
        kernel_group = QGroupBox("Kernel Values")
        kernel_layout = QVBoxLayout()
        self.kernel_values = KernelValuesWidget(self.kernel_config)
        kernel_layout.addWidget(self.kernel_values)
        kernel_group.setLayout(kernel_layout)
        grid_layout.addWidget(kernel_group, 0, 1)
        
        computed_group = QGroupBox("Computed Pixel Values")
        computed_layout = QVBoxLayout()
        computed_scroll = QScrollArea()
        computed_scroll.setWidgetResizable(False)
        self.computed_grid = ComputedPixelValuesWidget(self.output_data)
        computed_scroll.setWidget(self.computed_grid)
        computed_layout.addWidget(computed_scroll)
        computed_group.setLayout(computed_layout)
        grid_layout.addWidget(computed_group, 0, 2)
        
        work_group = QGroupBox("Work")
        work_layout = QVBoxLayout()
        work_layout.setContentsMargins(0, 0, 0, 0)
        work_layout.setSpacing(0)
        self.work_section = WorkSectionWidget()
        work_layout.addWidget(self.work_section)
        work_group.setLayout(work_layout)
        work_group.setMaximumHeight(250)
        grid_layout.addWidget(work_group, 1, 0, 1, 3)
        
        grid_layout.setRowStretch(0, 1)
        grid_layout.setRowStretch(1, 0)
        
        control_group = QGroupBox("Control Panel")
        control_group.setMaximumWidth(300)
        control_layout = QVBoxLayout()
        self.control_panel = ControlPanel(self.kernel_config)
        control_layout.addWidget(self.control_panel)
        control_group.setLayout(control_layout)
        
        main_layout.addLayout(grid_layout, 2)
        main_layout.addWidget(control_group, 1)
        
    def connect_signals(self):
        self.input_grid.pixel_clicked.connect(self.on_input_changed)
        self.control_panel.grid_size_changed.connect(self.on_grid_size_changed)
        self.control_panel.show_colors_changed.connect(self.on_show_colors_changed)
        self.control_panel.kernel_size_changed.connect(self.on_kernel_size_changed)
        self.control_panel.category_changed.connect(self.on_category_changed)
        self.control_panel.operation_type_changed.connect(self.on_operation_type_changed)
        self.control_panel.filter_selection_changed.connect(self.on_filter_selection_changed)
        self.control_panel.constant_changed.connect(self.on_constant_changed)
        self.kernel_values.value_changed.connect(self.on_kernel_value_changed)
        self.control_panel.raw_image_mode_changed.connect(self.on_raw_image_mode_changed)
        self.control_panel.previous_position.connect(self.on_previous_position)
        self.control_panel.next_position.connect(self.on_next_position)
        self.control_panel.reset_position.connect(self.on_reset_position)
    
    def update_kernel_position(self):
        total = self.kernel_position.calculate_total_positions(
            self.image_data.width,
            self.image_data.height,
            self.kernel_config.size
        )
        
        if total > 0:
            self.kernel_position.set_position(0, self.image_data.width, self.kernel_config.size)
            self.control_panel.enable_navigation(True)
        else:
            self.control_panel.enable_navigation(False)
            
        self.update_highlights()
    
    # SIGNAL HANDLERS #########################################################
    ###########################################################################
    def on_input_changed(self, row: int, col: int):
        pass
        
    def on_grid_size_changed(self, size: int):
        self.image_data.resize(size, size)
        
        self.output_data.resize(size, size)
        self.output_data.pixels = [[None for _ in range(size)] for _ in range(size)]
        
        self.input_grid.set_image_data(self.image_data)
        self.computed_grid.set_image_data(self.output_data)
        
        self.update_kernel_position()
    
    def on_show_colors_changed(self, show_colors: bool):
        self.input_grid.set_show_colors(show_colors)
        self.computed_grid.set_show_colors(show_colors)
        
    def on_kernel_size_changed(self, size: int):
        self.kernel_config.resize(size)
        
        if self.kernel_config.filter_selection == "Mean":
            for r in range(self.kernel_config.size):
                for c in range(self.kernel_config.size):
                    self.kernel_config.set_value(r, c, 1.0)
        
        self.kernel_values.update_kernel_grid()
        self.update_kernel_position()
        
    def on_category_changed(self, category: str):
        self.kernel_config.category = category
        self.output_data.pixels = [[None] * self.output_data.width for _ in range(self.output_data.height)]
        self.computed_grid.update()
        self.update_highlights()
    
    def on_operation_type_changed(self, operation_type: str):
        self.kernel_config.operation_type = operation_type
        self.update_highlights()
    
    def on_filter_selection_changed(self, filter_selection: str):
        self.kernel_config.filter_selection = filter_selection
        
        if filter_selection == "Mean":
            for r in range(self.kernel_config.size):
                for c in range(self.kernel_config.size):
                    self.kernel_config.set_value(r, c, 1.0)
        elif filter_selection == "Custom":
            for r in range(self.kernel_config.size):
                for c in range(self.kernel_config.size):
                    self.kernel_config.set_value(r, c, 0.0)
        
        self.kernel_values.update_kernel_values_state(
            self.kernel_config.category,
            self.kernel_config.filter_selection
        )
        self.kernel_values.update_kernel_grid()
        self.update_highlights()
    
    def on_constant_changed(self, constant: float):
        self.kernel_config.constant = constant
        self.update_highlights()
    
    def on_kernel_value_changed(self):
        pass
    
    def on_raw_image_mode_changed(self, mode: str):
        self.input_grid.set_mode(mode)
        
    def on_previous_position(self):
        if self.kernel_position.current_index > 0:
            self.kernel_position.set_position(
                self.kernel_position.current_index - 1,
                self.image_data.width,
                self.kernel_config.size
            )
            self.update_highlights()
            
    def on_next_position(self):
        if self.kernel_position.current_index < self.kernel_position.total_positions - 1:
            self.kernel_position.set_position(
                self.kernel_position.current_index + 1,
                self.image_data.width,
                self.kernel_config.size
            )
            self.update_highlights()
            
    def on_reset_position(self):
        self.output_data.pixels = [[None for _ in range(self.output_data.width)] for _ in range(self.output_data.height)]
        
        self.work_section.clear()
        
        self.computed_grid.update()
        
        self.kernel_position.set_position(
            0,
            self.image_data.width,
            self.kernel_config.size
        )
        self.update_highlights()
        
    # FILTER CALCULATION ######################################################
    ###########################################################################
    def calculate_and_update(self):
        if self.kernel_config.category == "Linear":
            if self.kernel_config.operation_type == "Convolution":
                result = self.filter_calculator.calculate_convolution(
                    self.image_data,
                    self.kernel_position,
                    self.kernel_config
                )
                if result:
                    self.work_section.update_convolution_calculation(result)
                    self.output_data.set_pixel(result.center_row, result.center_col, int(result.result))
            else:
                result = self.filter_calculator.calculate_cross_correlation(
                    self.image_data,
                    self.kernel_position,
                    self.kernel_config
                )
                if result:
                    self.work_section.update_cross_correlation_calculation(result)
                    self.output_data.set_pixel(result.center_row, result.center_col, int(result.result))
        else:
            result = self.filter_calculator.calculate_median_filter(
                self.image_data,
                self.kernel_position,
                self.kernel_config.size,
                self.kernel_config.constant
            )
            if result:
                self.work_section.update_median_calculation(result)
                self.output_data.set_pixel(result.center_row, result.center_col, int(result.result))
        
        self.computed_grid.update()
    
    def update_highlights(self):
        if self.kernel_position.total_positions > 0:
            self.input_grid.set_kernel_highlight(
                self.kernel_position.row,
                self.kernel_position.col,
                self.kernel_config.size
            )
            
            center_row = self.kernel_position.row + self.kernel_config.size // 2
            center_col = self.kernel_position.col + self.kernel_config.size // 2
            
            self.computed_grid.set_output_highlight(
                center_row,
                center_col
            )
            
            self.control_panel.update_position_label(
                self.kernel_position.current_index,
                self.kernel_position.total_positions
            )
            
            self.calculate_and_update()
        else:
            self.input_grid.clear_kernel_highlight()
            self.computed_grid.clear_output_highlight()
            self.control_panel.update_position_label(0, 0)
            self.work_section.clear()
