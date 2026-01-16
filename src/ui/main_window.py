from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt

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

        self.setWindowTitle("Computer Vision Playground")
        self.setMinimumSize(1200, 800)
        
        # Initialize and configure all UI components
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
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Create the left side (image processing widgets) and right side (control panel)
        left_widget = self._create_left_side()
        right_widget = self._create_right_side()
        
        # Add widgets to layout with stretch factors (left: 1, right: 0 = fixed width)
        main_layout.addWidget(left_widget, 1)
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
        left_layout.setSpacing(10) # space between widgets
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create top row container with horizontal layout
        top_row = QWidget()
        top_layout = QHBoxLayout(top_row)
        top_layout.setSpacing(10) # space between widgets
        top_layout.setContentsMargins(0, 0, 0, 0)
        
        # Instantiate the three main image processing widgets
        input_image = InputImageWidget()
        kernel_config = KernelConfigWidget()
        output_image = OutputImageWidget()
        
        # Fix kernel config width to prevent it from stretching
        kernel_config.setFixedWidth(150)
        
        # Add widgets to top row (input and output stretch, kernel config fixed)
        top_layout.addWidget(input_image, 1) # Stretch factor 1
        top_layout.addWidget(kernel_config, 0) # Stretch factor 0 (fixed)
        top_layout.addWidget(output_image, 1) # Stretch factor 1
        
        # Create filter calculations widget for detailed computation display
        filter_calculations = FilterCalculationsWidget()
        
        # Add top row and calculations to left layout with 60/40 split
        left_layout.addWidget(top_row, 60) # Top row gets 60% of vertical space
        left_layout.addWidget(filter_calculations, 40) # Calculations get 40% of vertical space
        
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
        
        # Create instance of the control panel widget
        ControlPanelWidget = control_panel_module.ControlPanelWidget
        
        # Create control panel widget with fixed width
        control_panel = ControlPanelWidget()
        control_panel.setFixedWidth(300) # Fixed width of 300 pixels
        
        return control_panel