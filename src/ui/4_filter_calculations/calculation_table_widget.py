from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QFontMetrics


class CalculationTableWidget(QWidget):
    def __init__(self):
        super().__init__()
        # Store the list of calculation data for each affected cell
        self._calculations = []
        # Width allocated for row labels on the left side
        self._label_width = 0
        # List storing the width of each column (one per affected cell)
        self._cell_widths = []
        # Height of each row in pixels
        self._cell_height = 30
        # Total number of rows in the table (header + 5 data rows)
        self._row_count = 6
        # Set minimum height based on number of rows
        self.setMinimumHeight(self._row_count * self._cell_height)
    
    def set_calculations(self, calculations: list) -> None:
        # Update the calculation data and recalculate widget dimensions
        self._calculations = calculations
        if self._calculations:
            # Calculate optimal column widths based on content
            self._calculate_dimensions()
            # Calculate total required width (labels + all columns)
            total_width = self._label_width + sum(self._cell_widths)
            # Calculate total required height (all rows)
            height = self._row_count * self._cell_height
            # Set minimum width to accommodate all content
            self.setMinimumWidth(total_width)
            # Set fixed height (table doesn't expand vertically)
            self.setFixedHeight(height)
        # Trigger repaint to display new data
        self.update()
        # Notify layout system that size requirements have changed
        self.updateGeometry()
    
    def _calculate_dimensions(self):
        # Create fonts for measuring text dimensions
        font = QFont("Arial", 11)
        bold_font = QFont("Arial", 11)
        bold_font.setBold(True)
        
        # Define the text labels for each row
        row_labels = [
            "",  # Header row (no label)
            "Coordinates:",
            "Values:",
            "Kernel Adjusted Calculations:",
            "Kernel Adjusted Values:",
            "Bounded Values:"
        ]
        
        # Create font metrics for measuring bold text
        bold_metrics = QFontMetrics(bold_font)
        
        # Find the maximum width needed for row labels
        max_label_width = 0
        for label in row_labels:
            # Add extra spacing after label text
            label_width = bold_metrics.horizontalAdvance(label + "  ")
            max_label_width = max(max_label_width, label_width)
        
        # Set label column width with additional padding
        self._label_width = max_label_width + 20
        
        # Create font metrics for measuring regular text
        metrics = QFontMetrics(font)
        self._cell_widths = []
        
        # Calculate optimal width for each data column
        for calc in self._calculations:
            max_width = 0
            
            # Collect all text that will appear in this column
            texts = [
                str(calc['index']),  # Row 0: Cell index
                f"({calc['coordinate'][0]},{calc['coordinate'][1]})",  # Row 1: Coordinates
                str(calc['input_value']),  # Row 2: Input pixel value
                f"({calc['input_value']}×{calc['final_kernel_value']:.2f})",  # Row 3: Calculation expression
                f"{calc['result']:.2f}",  # Row 4: Raw result
                f"{calc['bounded_result']:.2f}"  # Row 5: Bounded result
            ]
            
            # Find the widest text in this column
            for text in texts:
                text_width = metrics.horizontalAdvance(text)
                max_width = max(max_width, text_width)
            
            # Add padding to the column width
            self._cell_widths.append(max_width + 30)
    
    def sizeHint(self) -> QSize:
        # Return the preferred size for this widget
        if not self._calculations:
            # Default size when no data to display
            return QSize(400, self._row_count * self._cell_height)
        
        # Calculate size based on content
        total_width = self._label_width + sum(self._cell_widths)
        height = self._row_count * self._cell_height
        return QSize(total_width, height)
    
    def minimumSizeHint(self) -> QSize:
        # Minimum size is the same as preferred size
        return self.sizeHint()
    
    def resizeEvent(self, event):
        # Handle widget resize events
        super().resizeEvent(event)
        # Trigger repaint to adjust content layout
        self.update()
    
    def paintEvent(self, event):
        # Create painter object for drawing the table
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)  # Disable antialiasing for sharp edges
        
        # Display message if no calculation data available
        if not self._calculations:
            painter.setPen(QColor(200, 200, 200))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "No calculations to display")
            return
        
        # Define colors for different text types
        label_text_color = QColor(255, 255, 255)  # White for row labels
        data_text_color = QColor(255, 255, 255)  # White for data values
        header_text_color = QColor(150, 150, 150)  # Gray for column headers
        
        # Create fonts for text rendering
        font = QFont("Arial", 11)
        bold_font = QFont("Arial", 11)
        bold_font.setBold(True)
        
        # Get number of data columns (one per affected cell)
        num_cols = len(self._calculations)
        
        # Define the text labels for each row
        row_labels = [
            "",  # Header row (no label)
            "Coordinates:",
            "Values:",
            "Kernel Adjusted Calculations:",
            "Kernel Adjusted Values:",
            "Bounded Values:"
        ]
        
        # Calculate column widths, distributing any extra space evenly
        min_total_width = self._label_width + sum(self._cell_widths)
        available_width = self.width()
        extra_space = max(0, available_width - min_total_width)
        extra_per_cell = extra_space / num_cols if num_cols > 0 else 0
        
        # Add extra space to each column proportionally
        actual_cell_widths = [w + extra_per_cell for w in self._cell_widths]
        
        # Draw row labels in the left column
        for row_idx in range(self._row_count):
            # Calculate vertical position for this row
            y = row_idx * self._cell_height
            
            # Use bold font for labels
            painter.setFont(bold_font)
            painter.setPen(QPen(label_text_color))
            # Draw label text right-aligned with padding
            painter.drawText(0, y, self._label_width - 10, self._cell_height,
                           Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                           row_labels[row_idx])
        
        # Draw data columns (one per affected cell)
        x_offset = self._label_width
        for col_idx, calc in enumerate(self._calculations):
            # Get the width for this column
            cell_width = actual_cell_widths[col_idx]
            
            # Draw all rows in this column
            for row_idx in range(self._row_count):
                # Calculate vertical position for this row
                y = row_idx * self._cell_height
                
                # Use regular font for data
                painter.setFont(font)
                
                # Use different color for header row vs data rows
                if row_idx == 0:
                    painter.setPen(QPen(header_text_color))
                else:
                    painter.setPen(QPen(data_text_color))
                
                # Select appropriate text based on row
                if row_idx == 0:
                    # Row 0: Cell index (header)
                    text = str(calc['index'])
                elif row_idx == 1:
                    # Row 1: Grid coordinates
                    text = f"({calc['coordinate'][0]},{calc['coordinate'][1]})"
                elif row_idx == 2:
                    # Row 2: Input pixel value
                    text = str(calc['input_value'])
                elif row_idx == 3:
                    # Row 3: Calculation expression (input × kernel weight)
                    text = f"({calc['input_value']}×{calc['final_kernel_value']:.2f})"
                elif row_idx == 4:
                    # Row 4: Raw calculation result
                    text = f"{calc['result']:.2f}"
                else:
                    # Row 5: Bounded result (clamped to [0, 255])
                    text = f"{calc['bounded_result']:.2f}"
                
                # Draw text centered in the cell
                painter.drawText(x_offset, y, cell_width, self._cell_height,
                               Qt.AlignmentFlag.AlignCenter, text)
            
            # Move to next column position
            x_offset += cell_width
