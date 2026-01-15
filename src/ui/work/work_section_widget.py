from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QScrollArea, QFrame
from PySide6.QtCore import Qt

from src.core.filter_calculator import MeanFilterResult


class WorkSectionWidget(QWidget):
    """
    Widget that displays the step-by-step calculation details for filter operations.
    Shows coordinates, values, and mathematical operations in a visual grid format.
    """
    
    def __init__(self, parent=None):
        """
        Initialize the work section widget.
        
        Args:
            parent: Optional parent widget
        """
        super().__init__(parent)
        # Track which filter type is currently being displayed
        self.current_filter = "Mean"
        # Store references to all grid labels for cleanup when updating display
        self.grid_labels = []
        self.setup_ui()
    
    def setup_ui(self):
        """
        Set up the UI components for the work section.
        Creates a scrollable area containing a grid for calculation details and a summary section.
        """
        # Main layout for this widget with no margins
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create scroll area to handle content that might be larger than the visible area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Allow content to resize with the scroll area
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Container widget that will be placed inside the scroll area
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)  # Remove spacing between elements
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # Align content to top
        
        # Grid container holds the table showing coordinates and values
        self.grid_container = QWidget()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setSpacing(2)  # Small spacing between grid cells
        self.grid_layout.setContentsMargins(10, 10, 10, 0)  # Padding around the grid
        self.content_layout.addWidget(self.grid_container)
        
        # Summary label displays the mathematical calculation (sum, division, result)
        self.summary_label = QLabel("")
        self.summary_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.summary_label.setWordWrap(True)  # Allow text to wrap for long calculations
        self.summary_label.setStyleSheet("padding: 10px 10px 10px 10px; font-size: 12px;")
        self.content_layout.addWidget(self.summary_label)
        
        # Placeholder label shown when no calculation is available
        self.no_data_label = QLabel("No calculation to display")
        self.no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_data_label.setStyleSheet("padding: 20px; color: gray;")
        self.content_layout.addWidget(self.no_data_label)
        
        # Add the content widget to the scroll area and the scroll area to main layout
        scroll_area.setWidget(self.content_widget)
        layout.addWidget(scroll_area)
    
    def set_filter_type(self, filter_type: str):
        """
        Update the current filter type being displayed.
        
        Args:
            filter_type: Name of the filter (e.g., "Mean", "Gaussian", etc.)
        """
        self.current_filter = filter_type
    
    def clear(self):
        """
        Clear all calculation data and show the "no data" placeholder.
        Used when no pixel is selected or when switching contexts.
        """
        self._clear_grid()
        self.summary_label.setText("")
        # Show placeholder, hide actual content
        self.no_data_label.show()
        self.grid_container.hide()
        self.summary_label.hide()
    
    def _clear_grid(self):
        """
        Remove all labels from the grid layout.
        Properly deletes Qt widgets to prevent memory leaks.
        """
        for label in self.grid_labels:
            label.deleteLater()  # Schedule widget for deletion
        self.grid_labels.clear()  # Clear the reference list
    
    def update_mean_calculation(self, result: MeanFilterResult):
        """
        Display the mean filter calculation in a visual grid format.
        
        Creates a table showing:
        - Row 0: Index numbers (0, 1, 2, ...)
        - Row 1: Coordinates of each pixel used in the calculation
        - Row 2: Pixel values at those coordinates
        
        Then shows the sum and mean calculation below the grid.
        
        Args:
            result: MeanFilterResult containing coordinates, values, and calculated mean
        """
        # If no result provided, clear the display
        if result is None:
            self.clear()
            return
        
        # Remove any previous calculation from the grid
        self._clear_grid()
        
        # Hide placeholder and show the actual content
        self.no_data_label.hide()
        self.grid_container.show()
        self.summary_label.show()
        
        # Create "Coordinates:" label in the first column of row 1
        coord_header = QLabel("Coordinates:")
        coord_header.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        coord_header.setStyleSheet("font-weight: bold; padding-right: 10px;")
        self.grid_layout.addWidget(coord_header, 1, 0)  # Row 1, Column 0
        self.grid_labels.append(coord_header)
        
        # Create "Values:" label in the first column of row 2
        value_header = QLabel("Values:")
        value_header.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        value_header.setStyleSheet("font-weight: bold; padding-right: 10px;")
        self.grid_layout.addWidget(value_header, 2, 0)  # Row 2, Column 0
        self.grid_labels.append(value_header)
        
        # Loop through each coordinate-value pair and create column for it
        for idx, (coord, value) in enumerate(zip(result.coordinates, result.values)):
            # Row 0: Index number (0, 1, 2, ...)
            index_label = QLabel(str(idx))
            index_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            index_label.setStyleSheet("font-weight: bold; padding: 5px 8px; color: #666;")
            self.grid_layout.addWidget(index_label, 0, idx + 1)  # Row 0, Column idx+1
            self.grid_labels.append(index_label)
            
            # Row 1: Coordinate as (x,y)
            coord_label = QLabel(f"({coord[0]},{coord[1]})")
            coord_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            coord_label.setStyleSheet("padding: 5px 8px;")
            self.grid_layout.addWidget(coord_label, 1, idx + 1)  # Row 1, Column idx+1
            self.grid_labels.append(coord_label)
            
            # Row 2: Pixel value at that coordinate
            value_label = QLabel(str(value))
            value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            value_label.setStyleSheet("padding: 5px 8px;")
            self.grid_layout.addWidget(value_label, 2, idx + 1)  # Row 2, Column idx+1
            self.grid_labels.append(value_label)
        
        # Display the mathematical summary (sum and mean calculation)
        self._update_summary(result)
    
    def _update_summary(self, result: MeanFilterResult):
        """
        Create and display the mathematical summary of the mean filter calculation.
        
        Shows two lines:
        1. Sum: Lists all values added together and shows the total
        2. Mean: Shows total divided by count of values, displays result to 2 decimal places
        
        Args:
            result: MeanFilterResult containing the values and calculated results
        """
        # Create a string showing all values being added: "10 + 20 + 30"
        values_sum_str = " + ".join([str(v) for v in result.values])
        
        # Build HTML summary showing the step-by-step calculation
        summary_text = f"""<div style='line-height: 1.8;'>
<b>Sum:</b> {values_sum_str} = {result.total}<br/>
<b>Mean:</b> {result.total} / {len(result.values)} = {result.mean:.2f}<br/>
</div>"""
        
        # Display the summary in the label
        self.summary_label.setText(summary_text)
