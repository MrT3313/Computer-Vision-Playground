from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QScrollArea, QWidget
from PySide6.QtCore import Qt
from core import ApplicationState
from core.mean_filter_calculator import MeanFilterCalculator
from core.custom_filter_calculator import CustomFilterCalculator
from core.gaussian_filter_calculator import GaussianFilterCalculator
from .calculation_table_widget import CalculationTableWidget
from .formula_display_widget import FormulaDisplayWidget


class FilterCalculationsWidget(QFrame):
    def __init__(self, input_model, kernel_model, coordinator, output_model):
        super().__init__()
        # Store reference to the input image grid model
        self._input_model = input_model
        # Store reference to the kernel grid model
        self._kernel_model = kernel_model
        # Store reference to the application coordinator for position tracking
        self._coordinator = coordinator
        # Store reference to the output image grid model for writing results
        self._output_model = output_model
        # Store the current filter selection (e.g., "Mean", "Custom")
        self._filter_selection = "Mean"
        # Store the filter category (e.g., "Linear", "Non-Linear")
        self._filter_category = "Linear"
        # Store the filter type (e.g., "Cross-Correlation", "Convolution")
        self._filter_type = "Cross-Correlation"
        # Store the constant multiplier value for kernel weights
        self._constant = 1.0
        
        # Create the calculator that performs the convolution computation
        self._calculator = MeanFilterCalculator(input_model, kernel_model, coordinator)
        
        self._setup_ui()
    
    def _setup_ui(self):
        # Configure the frame's visual appearance with a box border
        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(2)  # Set border thickness to 2 pixels
        self.setMinimumHeight(150)  # Ensure minimum height of 150 pixels
        
        # Create the main vertical layout that will contain all child widgets
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)  # Remove padding around edges
        main_layout.setSpacing(0)  # Remove spacing between child widgets
        
        # Create the title bar frame at the top of the panel
        title_bar = QFrame()
        title_bar.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border-bottom: 1px solid rgba(0, 0, 0, 0.3);")
        title_bar.setFixedHeight(30)  # Fixed height of 30 pixels for title bar
        
        # Create layout for the title bar to hold the title label
        title_layout = QVBoxLayout(title_bar)
        title_layout.setContentsMargins(5, 0, 5, 0)  # Add 5px padding on left and right
        
        # Create the title label
        title_label = QLabel("4. Filter Calculations")
        title_label.setStyleSheet("font-size: 12px; font-weight: bold; background: transparent; border: none;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)  # Align text to the left and vertically centered
        
        # Add the title label to the title bar layout
        title_layout.addWidget(title_label)
        
        # Create the content area widget that will hold all filter calculation components
        self._content_area = QWidget()
        content_layout = QVBoxLayout(self._content_area)
        content_layout.setContentsMargins(10, 10, 10, 10)  # Add 10px padding on all sides
        content_layout.setSpacing(10)  # Add 10px spacing between widgets
        
        # Create placeholder label shown when no calculations are active
        self._placeholder_label = QLabel("Click 'Start' to begin calculations")
        self._placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Create widget to display the mathematical formula for the current filter
        self._formula_widget = FormulaDisplayWidget()
        
        # Create scroll area to contain the calculation table (allows horizontal scrolling)
        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(False)  # Table manages its own size
        self._scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)  # Show horizontal scrollbar when needed
        self._scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # Never show vertical scrollbar
        self._scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)  # Remove scroll area border
        self._scroll_area.setMinimumHeight(200)  # Set minimum height for table area
        self._scroll_area.setMaximumHeight(200)  # Set maximum height to prevent vertical expansion
        
        # Create the calculation table widget that displays step-by-step computations
        self._table_widget = CalculationTableWidget()
        self._scroll_area.setWidget(self._table_widget)
        # Override resize event to keep table width synchronized with scroll area
        self._scroll_area.resizeEvent = self._on_scroll_area_resize
        
        # Add all widgets to the content layout
        content_layout.addWidget(self._formula_widget, 0)  # Stretch factor 0 = fixed height
        content_layout.addWidget(self._placeholder_label)
        content_layout.addWidget(self._scroll_area, 1)  # Stretch factor 1 = expandable
        
        # Create label to display the final calculation result
        self._result_label = QLabel()
        self._result_label.setStyleSheet("color: white; font-size: 13px; font-weight: bold; padding: 10px;")
        self._result_label.setWordWrap(True)  # Allow text to wrap to multiple lines
        content_layout.addWidget(self._result_label, 0)  # Stretch factor 0 = fixed height
        
        # Add both the title bar and content area to the main layout
        main_layout.addWidget(title_bar)  # Title bar at the top
        main_layout.addWidget(self._content_area, 1)  # Content area below with stretch factor 1
        
        # Show placeholder by default (before navigation starts)
        self._show_placeholder()
    
    def _on_scroll_area_resize(self, event):
        # Handle scroll area resize to ensure table uses full available width
        QScrollArea.resizeEvent(self._scroll_area, event)
        # Get the viewport width (visible area width)
        viewport_width = self._scroll_area.viewport().width()
        # Resize table to match viewport width while maintaining its calculated height
        self._table_widget.resize(viewport_width, self._table_widget.height())
    
    def _show_placeholder(self):
        # Show the placeholder message and hide calculation content (but keep formula visible)
        self._placeholder_label.setVisible(True)
        self._formula_widget.setVisible(True)
        self._scroll_area.setVisible(False)
        self._result_label.setVisible(False)
    
    def _show_content(self):
        # Show the calculation content and hide the placeholder message
        self._placeholder_label.setVisible(False)
        self._formula_widget.setVisible(True)
        self._scroll_area.setVisible(True)
        self._result_label.setVisible(True)
    
    def set_filter(self, filter_name: str) -> None:
        # Update the filter selection and refresh the display
        self._filter_selection = filter_name
        # Update the formula display to show the new filter's equation
        self._formula_widget.set_filter(filter_name)
        # Create appropriate calculator based on filter selection
        if filter_name == "Mean":
            self._calculator = MeanFilterCalculator(self._input_model, self._kernel_model, self._coordinator)
        elif filter_name == "Gaussian":
            self._calculator = GaussianFilterCalculator(self._input_model, self._kernel_model, self._coordinator)
        elif filter_name == "Custom":
            self._calculator = CustomFilterCalculator(self._input_model, self._kernel_model, self._coordinator)
        # Recalculate and update the display with the new filter
        self._update_display()
    
    def set_category(self, category: str) -> None:
        # Update the filter category and refresh the display
        self._filter_category = category
        self._update_display()
    
    def set_type(self, filter_type: str) -> None:
        # Update the filter type and refresh the display
        self._filter_type = filter_type
        # Update the formula display to show the correct formula for the filter type
        self._formula_widget.set_filter_type(filter_type)
        self._update_display()
    
    def set_constant(self, constant: float) -> None:
        # Update the constant multiplier value and refresh the display
        self._constant = constant
        # Recalculate and update the display with the new constant
        self._update_display()
    
    def on_state_changed(self, state) -> None:
        # Handle application state changes
        if state == ApplicationState.INITIAL:
            # Show placeholder when returning to initial state
            self._show_placeholder()
        elif state == ApplicationState.NAVIGATING:
            # Show content and perform calculations when entering navigation state
            self._show_content()
            self._update_display()
    
    def update_calculation(self, row: int, col: int) -> None:
        # Update calculations when the kernel position changes during navigation
        if self._coordinator.get_state() == ApplicationState.NAVIGATING:
            self._update_display()
    
    def on_kernel_changed(self, size: int, grid_data: list) -> None:
        # Update calculations when the kernel data or size changes
        if self._coordinator.get_state() == ApplicationState.NAVIGATING:
            self._update_display()
    
    def _update_display(self):
        # Perform calculation and update all display components
        # Only update if in NAVIGATING state
        if self._coordinator.get_state() != ApplicationState.NAVIGATING:
            return
        
        # Perform the calculation for the current kernel position
        if self._filter_selection == "Mean":
            result = self._calculator.calculate(self._constant)
        elif self._filter_selection == "Gaussian":
            result = self._calculator.calculate(self._constant)
        elif self._filter_selection == "Custom":
            result = self._calculator.calculate(self._constant, self._filter_type)
        else:
            return
        
        # Update the calculation table with step-by-step computation details
        self._table_widget.set_calculations(result['calculations'])
        
        # Build text for displaying the sum of all weighted pixel values
        calculations = result['calculations']
        sum_parts = " + ".join([f"{c['bounded_result']:.2f}" for c in calculations])
        sum_text = f"Sum: {sum_parts} = {result['total_sum']:.2f}"
        
        # Build result text based on filter type
        if self._filter_selection == "Mean":
            kernel_size = self._kernel_model.get_grid_size()
            k = kernel_size // 2
            denominator = (2 * k + 1) ** 2
            mean_text = f"Mean: 1/(2k+1)² × {result['total_sum']:.2f} = 1/{denominator} × {result['total_sum']:.2f} = {result['output']:.2f}"
            result_text = f"Result: {result['output']:.2f}"
            full_text = f"{sum_text}\n\n{mean_text}\n\n{result_text}"
        elif self._filter_selection == "Gaussian":
            result_text = f"Result: {result['output']:.2f}"
            full_text = f"{sum_text}\n\n{result_text}"
        elif self._filter_selection == "Custom":
            # For Custom filter, output is just the sum
            result_text = f"Result: {result['output']:.2f}"
            full_text = f"{sum_text}\n\n{result_text}"
        else:
            full_text = sum_text
        
        self._result_label.setText(full_text)
        
        # Write the calculated output value to the output image model
        output_cell = result['output_cell']
        # Round and clamp the output value to valid pixel range [0, 255]
        output_value = max(0, min(255, round(result['output'])))
        self._output_model.set_cell(output_cell[0], output_cell[1], output_value)