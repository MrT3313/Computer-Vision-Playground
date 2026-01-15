from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QGridLayout, QLabel, QGroupBox, QScrollArea
)
from PySide6.QtCore import Qt

from src.core.image_data import ImageData
from src.core.kernel_config import KernelConfig, KernelPosition
from src.core.filter_calculator import FilterCalculator
from src.ui.pixel_grid_widget import PixelGridWidget
from src.ui.control_panel import ControlPanel
from src.ui.work_section_widget import WorkSectionWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Computer Vision Playground")
        
        self.image_data = ImageData(width=10, height=10)
        self.output_data = ImageData(width=10, height=10)
        self.output_data.pixels = [[None for _ in range(10)] for _ in range(10)]
        
        self.kernel_config = KernelConfig(size=3)
        self.kernel_position = KernelPosition()
        self.filter_calculator = FilterCalculator()
        
        self.setup_ui()
        self.connect_signals()
        self.update_kernel_position()
        
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        grid_layout = QGridLayout()
        
        input_group = QGroupBox("1. Raw Input Image")
        input_layout = QVBoxLayout()
        input_scroll = QScrollArea()
        input_scroll.setWidgetResizable(False)
        self.input_grid = PixelGridWidget(
            self.image_data,
            editable=True,
            show_values=False
        )
        input_scroll.setWidget(self.input_grid)
        input_layout.addWidget(input_scroll)
        input_group.setLayout(input_layout)
        grid_layout.addWidget(input_group, 0, 0)
        
        values_group = QGroupBox("2. Raw Image Pixel Values")
        values_layout = QVBoxLayout()
        values_scroll = QScrollArea()
        values_scroll.setWidgetResizable(False)
        self.values_grid = PixelGridWidget(
            self.image_data,
            editable=False,
            show_values=True
        )
        values_scroll.setWidget(self.values_grid)
        values_layout.addWidget(values_scroll)
        values_group.setLayout(values_layout)
        grid_layout.addWidget(values_group, 0, 1)
        
        work_group = QGroupBox("Work - Mean Filter Calculation")
        work_layout = QVBoxLayout()
        work_layout.setContentsMargins(0, 0, 0, 0)
        work_layout.setSpacing(0)
        self.work_section = WorkSectionWidget()
        work_layout.addWidget(self.work_section)
        work_group.setLayout(work_layout)
        work_group.setMaximumHeight(250)
        grid_layout.addWidget(work_group, 1, 0, 1, 2)
        
        computed_group = QGroupBox("4. Computed Pixel Values")
        computed_layout = QVBoxLayout()
        computed_scroll = QScrollArea()
        computed_scroll.setWidgetResizable(False)
        self.computed_grid = PixelGridWidget(
            self.output_data,
            editable=False,
            show_values=True
        )
        computed_scroll.setWidget(self.computed_grid)
        computed_layout.addWidget(computed_scroll)
        computed_group.setLayout(computed_layout)
        grid_layout.addWidget(computed_group, 2, 0)
        
        output_group = QGroupBox("5. Output Image")
        output_layout = QVBoxLayout()
        output_scroll = QScrollArea()
        output_scroll.setWidgetResizable(False)
        self.output_grid = PixelGridWidget(
            self.output_data,
            editable=False,
            show_values=False
        )
        output_scroll.setWidget(self.output_grid)
        output_layout.addWidget(output_scroll)
        output_group.setLayout(output_layout)
        grid_layout.addWidget(output_group, 2, 1)
        
        grid_layout.setRowStretch(0, 1)
        grid_layout.setRowStretch(1, 0)
        grid_layout.setRowStretch(2, 1)
        
        control_group = QGroupBox("3. Control Panel")
        control_layout = QVBoxLayout()
        self.control_panel = ControlPanel(self.kernel_config)
        control_layout.addWidget(self.control_panel)
        control_group.setLayout(control_layout)
        
        main_layout.addLayout(grid_layout, 2)
        main_layout.addWidget(control_group, 1)
        
    def connect_signals(self):
        self.input_grid.pixel_clicked.connect(self.on_input_changed)
        self.control_panel.grid_size_changed.connect(self.on_grid_size_changed)
        self.control_panel.kernel_size_changed.connect(self.on_kernel_size_changed)
        self.control_panel.filter_type_changed.connect(self.on_filter_type_changed)
        self.control_panel.kernel_value_changed.connect(self.on_kernel_value_changed)
        self.control_panel.previous_position.connect(self.on_previous_position)
        self.control_panel.next_position.connect(self.on_next_position)
        self.control_panel.reset_position.connect(self.on_reset_position)
    
    def on_input_changed(self, row: int, col: int):
        self.values_grid.update()
        
    def on_grid_size_changed(self, size: int):
        self.image_data.resize(size, size)
        self.output_data.resize(size, size)
        self.output_data.pixels = [[None for _ in range(size)] for _ in range(size)]
        
        self.input_grid.set_image_data(self.image_data)
        self.values_grid.set_image_data(self.image_data)
        self.computed_grid.set_image_data(self.output_data)
        self.output_grid.set_image_data(self.output_data)
        
        self.update_kernel_position()
        
    def on_kernel_size_changed(self, size: int):
        self.kernel_config.resize(size)
        self.control_panel.update_kernel_grid()
        self.update_kernel_position()
        
    def on_filter_type_changed(self, filter_type: str):
        self.kernel_config.filter_type = filter_type
        self.work_section.set_filter_type(filter_type)
        self.control_panel.update_kernel_values_state(filter_type)
    
    def on_kernel_value_changed(self):
        pass
        
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
        self.output_grid.update()
        
        self.kernel_position.set_position(
            0,
            self.image_data.width,
            self.kernel_config.size
        )
        self.update_highlights()
        
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
        
    def calculate_and_update(self):
        if self.kernel_config.filter_type == "Mean":
            result = self.filter_calculator.calculate_mean_filter(
                self.image_data,
                self.kernel_position,
                self.kernel_config.size
            )
            
            if result:
                self.work_section.update_mean_calculation(result)
                
                self.output_data.set_pixel(
                    result.center_row,
                    result.center_col,
                    int(result.mean)
                )
                
                self.computed_grid.update()
                self.output_grid.update()
    
    def update_highlights(self):
        if self.kernel_position.total_positions > 0:
            self.input_grid.set_kernel_highlight(
                self.kernel_position.row,
                self.kernel_position.col,
                self.kernel_config.size
            )
            
            self.values_grid.set_kernel_highlight(
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
            
            self.output_grid.clear_output_highlight()
            
            self.control_panel.update_position_label(
                self.kernel_position.current_index,
                self.kernel_position.total_positions
            )
            
            self.calculate_and_update()
        else:
            self.input_grid.clear_kernel_highlight()
            self.values_grid.clear_kernel_highlight()
            self.computed_grid.clear_output_highlight()
            self.output_grid.clear_output_highlight()
            self.control_panel.update_position_label(0, 0)
            self.work_section.clear()
