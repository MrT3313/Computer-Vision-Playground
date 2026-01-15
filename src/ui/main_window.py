from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QGridLayout, QLabel, QGroupBox, QScrollArea
)
from PySide6.QtCore import Qt

from src.core.image_data import ImageData
from src.core.kernel_config import KernelConfig, KernelPosition
from src.core.filter_calculator import FilterCalculator
from src.ui.raw_input_image.raw_input_image_widget import RawInputImageWidget
from src.ui.raw_image_pixel_values.raw_image_pixel_values_widget import RawImagePixelValuesWidget
from src.ui.computed_pixel_values.computed_pixel_values_widget import ComputedPixelValuesWidget
from src.ui.output_image.output_image_widget import OutputImageWidget
from src.ui.control_panel.control_panel_widget import ControlPanel
from src.ui.work.work_section_widget import WorkSectionWidget


class MainWindow(QMainWindow):
    """
    Main application window for the Computer Vision Playground.
    
    Provides an interactive environment for learning convolution operations:
    1. Input image - draw black/white pixels
    2. Pixel values - see numeric values of input
    3. Control panel - configure kernel and navigate positions
    4. Work section - see step-by-step filter calculations
    5. Computed values - see filter output values
    6. Output image - see final filtered image
    
    The window coordinates all widgets and handles the convolution workflow.
    """
    
    def __init__(self, width = 10, height = 10):
        """Initialize the main window with data models and UI components."""
        super().__init__()
        self.setWindowTitle("Computer Vision Playground")
        
        # CONFIGURATION #######################################################
        #######################################################################
        # Input image (editable, starts white)
        self.image_data = ImageData(width=width, height=height)
        
        # Output image (computed values, starts as None)
        self.output_data = ImageData(width=width, height=height)
        self.output_data.pixels = [[None for _ in range(width)] for _ in range(height)]
        
        # Kernel configuration and position tracking
        self.kernel_config = KernelConfig(size=3)
        self.kernel_position = KernelPosition()

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
        - Left side: 2x2 grid with input/values (top row), work section (middle),
                     computed/output (bottom row)
        - Right side: Control panel
        """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Grid layout for the main visualization area (left side)
        grid_layout = QGridLayout()
        
        # === Section 1: Raw Input Image ===
        # Editable grid where user can draw black/white pixels
        input_group = QGroupBox("Raw Input Image")
        input_layout = QVBoxLayout()
        input_scroll = QScrollArea()
        input_scroll.setWidgetResizable(False)  # Fixed size, scrolls if needed
        self.input_grid = RawInputImageWidget(self.image_data)
        input_scroll.setWidget(self.input_grid)
        input_layout.addWidget(input_scroll)
        input_group.setLayout(input_layout)
        grid_layout.addWidget(input_group, 0, 0)  # Row 0, Column 0
        
        # === Section 2: Raw Image Pixel Values ===
        # Same as input but shows numeric values (0-255)
        values_group = QGroupBox("Raw Image Pixel Values")
        values_layout = QVBoxLayout()
        values_scroll = QScrollArea()
        values_scroll.setWidgetResizable(False)
        self.values_grid = RawImagePixelValuesWidget(self.image_data)
        values_scroll.setWidget(self.values_grid)
        values_layout.addWidget(values_scroll)
        values_group.setLayout(values_layout)
        grid_layout.addWidget(values_group, 0, 1)  # Row 0, Column 1
        
        # === Work Section: Mean Filter Calculation ===
        # Shows step-by-step calculation for current kernel position
        work_group = QGroupBox("Work")
        work_layout = QVBoxLayout()
        work_layout.setContentsMargins(0, 0, 0, 0)
        work_layout.setSpacing(0)
        self.work_section = WorkSectionWidget()
        work_layout.addWidget(self.work_section)
        work_group.setLayout(work_layout)
        work_group.setMaximumHeight(250)  # Limit height to prevent expansion
        # Spans both columns (row 1, columns 0-1)
        grid_layout.addWidget(work_group, 1, 0, 1, 2)
        
        # === Section 4: Computed Pixel Values ===
        # Shows the numeric results of filter calculations
        computed_group = QGroupBox("Computed Pixel Values")
        computed_layout = QVBoxLayout()
        computed_scroll = QScrollArea()
        computed_scroll.setWidgetResizable(False)
        self.computed_grid = ComputedPixelValuesWidget(self.output_data)
        computed_scroll.setWidget(self.computed_grid)
        computed_layout.addWidget(computed_scroll)
        computed_group.setLayout(computed_layout)
        grid_layout.addWidget(computed_group, 2, 0)  # Row 2, Column 0
        
        # === Section 5: Output Image ===
        # Shows the final filtered image as grayscale visualization
        output_group = QGroupBox("Output Image")
        output_layout = QVBoxLayout()
        output_scroll = QScrollArea()
        output_scroll.setWidgetResizable(False)
        self.output_grid = OutputImageWidget(self.output_data)
        output_scroll.setWidget(self.output_grid)
        output_layout.addWidget(output_scroll)
        output_group.setLayout(output_layout)
        grid_layout.addWidget(output_group, 2, 1)  # Row 2, Column 1
        
        # Set row stretching: top and bottom rows expand, middle (work) doesn't
        grid_layout.setRowStretch(0, 1)  # Input/values row stretches
        grid_layout.setRowStretch(1, 0)  # Work section fixed height
        grid_layout.setRowStretch(2, 1)  # Computed/output row stretches
        
        # === Section 3: Control Panel (right side) ===
        control_group = QGroupBox("Control Panel")
        control_layout = QVBoxLayout()
        self.control_panel = ControlPanel(self.kernel_config)
        control_layout.addWidget(self.control_panel)
        control_group.setLayout(control_layout)
        
        # Add grid layout and control panel to main horizontal layout
        main_layout.addLayout(grid_layout, 2)  # Grid takes 2/3 of width
        main_layout.addWidget(control_group, 1)  # Control takes 1/3 of width
        
    def connect_signals(self):
        """
        Connect all signals from UI components to their handler methods.
        Sets up the event flow between widgets and the main window.
        """
        self.input_grid.pixel_clicked.connect(self.on_input_changed)
        self.control_panel.grid_size_changed.connect(self.on_grid_size_changed)
        self.control_panel.kernel_size_changed.connect(self.on_kernel_size_changed)
        self.control_panel.filter_type_changed.connect(self.on_filter_type_changed)
        self.control_panel.kernel_value_changed.connect(self.on_kernel_value_changed)
        self.control_panel.previous_position.connect(self.on_previous_position)
        self.control_panel.next_position.connect(self.on_next_position)
        self.control_panel.reset_position.connect(self.on_reset_position)
    
    def update_kernel_position(self):
        """
        Recalculate total valid kernel positions and reset to first position.
        Called when grid size or kernel size changes.
        """
        # Calculate how many positions the kernel can occupy
        total = self.kernel_position.calculate_total_positions(
            self.image_data.width,
            self.image_data.height,
            self.kernel_config.size
        )
        
        # Enable/disable navigation based on whether kernel fits
        if total > 0:
            self.kernel_position.set_position(0, self.image_data.width, self.kernel_config.size)
            self.control_panel.enable_navigation(True)
        else:
            # Kernel is too large for the image
            self.control_panel.enable_navigation(False)
            
        self.update_highlights()
    
    # SIGNAL HANDLERS #########################################################
    ###########################################################################
    def on_input_changed(self, row: int, col: int):
        """
        Handle pixel clicks on the input image.
        Updates the values grid to show the new pixel value.
        
        Args:
            row: Row of clicked pixel
            col: Column of clicked pixel
        """
        self.values_grid.update()  # Redraw to show new value
        
    def on_grid_size_changed(self, size: int):
        """
        Handle grid size changes from the control panel.
        Resizes both input and output images and recalculates kernel positions.
        
        Args:
            size: New grid dimension (width and height)
        """
        # Resize input image (will reset to all white)
        self.image_data.resize(size, size)
        
        # Resize output image (will reset to all white, then set to None)
        self.output_data.resize(size, size)
        self.output_data.pixels = [[None for _ in range(size)] for _ in range(size)]
        
        # Update all grid widgets with new data
        self.input_grid.set_image_data(self.image_data)
        self.values_grid.set_image_data(self.image_data)
        self.computed_grid.set_image_data(self.output_data)
        self.output_grid.set_image_data(self.output_data)
        
        # Recalculate kernel positions for new grid size
        self.update_kernel_position()
        
    def on_kernel_size_changed(self, size: int):
        """
        Handle kernel size changes from the control panel.
        Updates kernel configuration and recalculates valid positions.
        
        Args:
            size: New kernel dimension (e.g., 3 for 3x3)
        """
        self.kernel_config.resize(size)
        self.control_panel.update_kernel_grid()  # Redraw kernel value grid
        self.update_kernel_position()  # Recalculate positions
        
    def on_filter_type_changed(self, filter_type: str):
        """
        Handle filter type changes from the control panel.
        
        Args:
            filter_type: Name of the selected filter (e.g., "Mean")
        """
        self.kernel_config.filter_type = filter_type
        self.work_section.set_filter_type(filter_type)
        self.control_panel.update_kernel_values_state(filter_type)
    
    def on_kernel_value_changed(self):
        """
        Handle changes to kernel values.
        Currently unused (reserved for custom filter types).
        """
        pass
        
    def on_previous_position(self):
        """
        Move kernel to the previous position.
        Decrements position index and updates all highlights and calculations.
        """
        if self.kernel_position.current_index > 0:
            self.kernel_position.set_position(
                self.kernel_position.current_index - 1,
                self.image_data.width,
                self.kernel_config.size
            )
            self.update_highlights()
            
    def on_next_position(self):
        """
        Move kernel to the next position.
        Increments position index and updates all highlights and calculations.
        """
        if self.kernel_position.current_index < self.kernel_position.total_positions - 1:
            self.kernel_position.set_position(
                self.kernel_position.current_index + 1,
                self.image_data.width,
                self.kernel_config.size
            )
            self.update_highlights()
            
    def on_reset_position(self):
        """
        Reset the output and return kernel to first position.
        Clears all computed values and the work section.
        """
        # Clear all output pixels (set to None)
        self.output_data.pixels = [[None for _ in range(self.output_data.width)] for _ in range(self.output_data.height)]
        
        # Clear the work section display
        self.work_section.clear()
        
        # Redraw output grids
        self.computed_grid.update()
        self.output_grid.update()
        
        # Return to first position
        self.kernel_position.set_position(
            0,
            self.image_data.width,
            self.kernel_config.size
        )
        self.update_highlights()
        
    # FILTER CALCULATION ######################################################
    ###########################################################################
    def calculate_and_update(self):
        """
        Perform filter calculation at current kernel position and update displays.
        Currently only supports mean filter.
        """
        if self.kernel_config.filter_type == "Mean":
            # Calculate mean filter for current position
            result = self.filter_calculator.calculate_mean_filter(
                self.image_data,
                self.kernel_position,
                self.kernel_config.size
            )
            
            if result:
                # Show calculation steps in work section
                self.work_section.update_mean_calculation(result)
                
                # Store calculated value in output image
                self.output_data.set_pixel(
                    result.center_row,
                    result.center_col,
                    int(result.mean)  # Round to integer for display
                )
                
                # Redraw output grids
                self.computed_grid.update()
                self.output_grid.update()
    
    def update_highlights(self):
        """
        Update all visual highlights and perform calculation for current position.
        
        Highlights:
        - Blue border around kernel area on input/values grids
        - Orange border on output pixel in computed grid
        - Position label in control panel
        
        Then triggers filter calculation and display update.
        """
        if self.kernel_position.total_positions > 0:
            # Highlight kernel area on input image grid
            self.input_grid.set_kernel_highlight(
                self.kernel_position.row,
                self.kernel_position.col,
                self.kernel_config.size
            )
            
            # Highlight kernel area on values grid
            self.values_grid.set_kernel_highlight(
                self.kernel_position.row,
                self.kernel_position.col,
                self.kernel_config.size
            )
            
            # Calculate center pixel position (where result goes)
            center_row = self.kernel_position.row + self.kernel_config.size // 2
            center_col = self.kernel_position.col + self.kernel_config.size // 2
            
            # Highlight output pixel in computed grid
            self.computed_grid.set_output_highlight(
                center_row,
                center_col
            )
            
            # No highlight on final output grid (just shows colors)
            self.output_grid.clear_output_highlight()
            
            # Update position counter in control panel
            self.control_panel.update_position_label(
                self.kernel_position.current_index,
                self.kernel_position.total_positions
            )
            
            # Perform calculation and update displays
            self.calculate_and_update()
        else:
            # No valid positions - clear all highlights
            self.input_grid.clear_kernel_highlight()
            self.values_grid.clear_kernel_highlight()
            self.computed_grid.clear_output_highlight()
            self.output_grid.clear_output_highlight()
            self.control_panel.update_position_label(0, 0)
            self.work_section.clear()
