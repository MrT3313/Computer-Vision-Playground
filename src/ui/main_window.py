from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QScrollArea
from PySide6.QtCore import Qt
from core import ImageGridModel, KernelApplicationCoordinator
from consts import DEFAULT_GRID_SIZE, DEFAULT_KERNEL_SIZE

class MainWindow(QMainWindow):
    """
    Main application window for the Computer Vision Playground.
    This class creates the overall layout and organizes all UI components.
    """

    def __init__(self):
        """
        Initialize the main window with title, size, and UI setup.
        """

        super().__init__()

        # Set the window title displayed in the title bar
        self.setWindowTitle("Computer Vision Playground")
        # Set minimum window dimensions to ensure adequate space for all components
        self.setMinimumSize(1200, 800)
        
        # Create the input image model with default grid size
        self._input_model = ImageGridModel(DEFAULT_GRID_SIZE)
        # Create the output image model with default grid size
        self._output_model = ImageGridModel(DEFAULT_GRID_SIZE)
        # Create the coordinator to manage kernel position and navigation state
        self._coordinator = KernelApplicationCoordinator(DEFAULT_GRID_SIZE, DEFAULT_KERNEL_SIZE)
        
        # Set up the UI components and layout
        self._setup_ui()
    
    def _setup_ui(self):
        """
        Set up the main UI layout structure.
        Creates a horizontal layout with left side (main content) and right side (controls).
        """

        # Create the central widget that will contain all other widgets
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create horizontal layout for main content organization
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(10) # Add 10px spacing between left and right sides
        main_layout.setContentsMargins(10, 10, 10, 10) # Add 10px padding on all sides
        
        # Create the left side (image processing widgets) and right side (control panel)
        left_widget = self._create_left_side()
        right_widget = self._create_right_side()
        
        # Wrap left side in scroll area to handle vertical overflow when kernel grows
        left_scroll = QScrollArea()
        left_scroll.setWidget(left_widget)
        left_scroll.setWidgetResizable(True) # Allow scroll area to resize its content
        left_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff) # Never show horizontal scrollbar
        left_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded) # Show vertical scrollbar when needed
        left_scroll.setFrameShape(QScrollArea.Shape.NoFrame) # Remove scroll area border
        
        # Add widgets to layout with stretch factors (left: 1 = expandable, right: 0 = fixed width)
        main_layout.addWidget(left_scroll, 1)
        main_layout.addWidget(right_widget, 0)
    
    def _create_left_side(self) -> QWidget:
        """
        Create the left side of the UI containing image processing components.
        
        Layout structure:
        - Top row: Input Image | Kernel Config | Output Image
        - Bottom row: Filter Calculations
        
        Returns:
            QWidget: Container widget with all left-side components
        """

        # Import UI modules dynamically to handle numeric prefixes in filenames
        import importlib
        input_image_module = importlib.import_module('ui.1_input_image')
        kernel_config_module = importlib.import_module('ui.2_kernel_config')
        output_image_module = importlib.import_module('ui.3_output_image')
        filter_calculations_module = importlib.import_module('ui.4_filter_calculations')
        
        # Create instances of the imported widget classes
        InputImageWidget = input_image_module.InputImageWidget
        KernelConfigWidget = kernel_config_module.KernelConfigWidget
        OutputImageWidget = output_image_module.OutputImageWidget
        FilterCalculationsWidget = filter_calculations_module.FilterCalculationsWidget
        
        # Create container widget with vertical layout for top/bottom sections
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setSpacing(10) # Add 10px spacing between top row and calculations
        left_layout.setContentsMargins(0, 0, 0, 0) # Remove padding around edges
        
        # Create top row container with horizontal layout
        top_row = QWidget()
        top_layout = QHBoxLayout(top_row)
        top_layout.setSpacing(10) # Add 10px spacing between widgets
        top_layout.setContentsMargins(0, 0, 0, 0) # Remove padding around edges
        
        # Create input image widget with coordinator for position tracking
        self._input_image = InputImageWidget(self._input_model, self._coordinator)
        # Create kernel configuration widget
        self._kernel_config = KernelConfigWidget()
        # Create output image widget with coordinator for position tracking
        self._output_image = OutputImageWidget(self._output_model, self._coordinator)
        
        # Add widgets to top row with stretch factors (input: 1, kernel: 0, output: 1)
        top_layout.addWidget(self._input_image, 1)
        top_layout.addWidget(self._kernel_config, 0)
        top_layout.addWidget(self._output_image, 1)
        
        # Create filter calculations widget for detailed computation display
        filter_calculations = FilterCalculationsWidget()
        
        # Add top row and calculations to left layout (top: 1, calculations: 0 = fixed height)
        left_layout.addWidget(top_row, 1)
        left_layout.addWidget(filter_calculations, 0)
        
        return left_widget
    
    def _create_right_side(self) -> QWidget:
        """
        Create the right side of the UI containing the control panel.
        
        Returns:
            QWidget: Control panel widget with fixed width
        """

        # Import UI modules dynamically to handle numeric prefixes in filenames
        import importlib
        control_panel_module = importlib.import_module('ui.5_control_panel')
        
        # Create instance of the imported control panel class
        ControlPanelWidget = control_panel_module.ControlPanelWidget
        
        # Create control panel with coordinator for navigation control
        self._control_panel = ControlPanelWidget(self._coordinator)
        # Set fixed width to prevent control panel from expanding
        self._control_panel.setFixedWidth(300)
        
        # Connect grid size changes to update all models and coordinator
        self._control_panel.grid_size_changed.connect(self._input_model.set_grid_size)
        self._control_panel.grid_size_changed.connect(self._output_model.set_grid_size)
        self._control_panel.grid_size_changed.connect(self._coordinator.set_grid_size)
        
        # Connect input mode changes to update input image editing behavior
        self._control_panel.input_mode_changed.connect(self._input_image.set_edit_mode)
        
        # Connect show pixel values changes to update input and output image pixel values
        self._control_panel.show_pixel_values_changed.connect(self._input_image.set_show_pixel_values)
        self._control_panel.show_pixel_values_changed.connect(self._output_image.set_show_pixel_values)
        
        # Connect show colors changes to update input and output image colors
        self._control_panel.show_colors_changed.connect(self._input_image.set_show_colors)
        self._control_panel.show_colors_changed.connect(self._output_image.set_show_colors)
        
        self._kernel_config.kernel_size_input.value_changed.connect(self._coordinator.set_kernel_size)
        
        return self._control_panel