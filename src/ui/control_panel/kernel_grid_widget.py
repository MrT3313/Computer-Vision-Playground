from PySide6.QtWidgets import QWidget, QLineEdit
from PySide6.QtCore import Qt, Signal, QRect
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QMouseEvent

from src.core.kernel_config import KernelConfig
from src.consts.defaults import DEFAULT_KERNEL_GRID_CELL_SIZE


class KernelGridWidget(QWidget):
    """
    Interactive grid widget for viewing and editing kernel values.
    
    Displays kernel coefficients in a grid where each cell shows a numeric value.
    Users can click cells to edit values. Used for custom filter configurations.
    
    Signals:
        value_changed: Emitted when any kernel value is modified
    """
    value_changed = Signal()
    
    def __init__(self, kernel_config: KernelConfig, parent=None):
        """
        Initialize the kernel grid widget.
        
        Args:
            kernel_config: Kernel configuration to display and edit
            parent: Optional parent widget
        """
        super().__init__(parent)
        self.kernel_config = kernel_config
        self.cell_size = DEFAULT_KERNEL_GRID_CELL_SIZE
        self.editing_cell = None
        self.line_edit = None  # QLineEdit widget for in-place editing
        
        self.update_size()
        self.setMouseTracking(True)  # Enable mouse tracking for hover effects

    def update_size(self):
        """
        Update widget dimensions based on kernel size.
        Sets both minimum and maximum to the same value for a fixed-size widget.
        """
        size = self.kernel_config.size
        # Calculate total widget size: (cells * cell_size) + 1 for border
        widget_size = size * self.cell_size + 1
        self.setMinimumSize(widget_size, widget_size)
        self.setMaximumSize(widget_size, widget_size)

    def get_cell_at_position(self, x: float, y: float) -> tuple[int, int]:
        """
        Convert mouse coordinates to grid cell indices.
        
        Args:
            x: Mouse x coordinate
            y: Mouse y coordinate
            
        Returns:
            (row, col) tuple of the cell at that position
        """
        col = int(x) // self.cell_size
        row = int(y) // self.cell_size
        return row, col

    def mousePressEvent(self, event: QMouseEvent):
        """
        Handle mouse clicks to start editing a cell.
        
        Args:
            event: Mouse event containing position and button info
        """
        if event.button() == Qt.MouseButton.LeftButton:
            row, col = self.get_cell_at_position(event.position().x(), event.position().y())
            # Check if click is within valid grid bounds
            if 0 <= row < self.kernel_config.size and 0 <= col < self.kernel_config.size:
                self.start_editing(row, col)

    def start_editing(self, row: int, col: int):
        """
        Start in-place editing of a cell value.
        Creates a QLineEdit overlay on the clicked cell.
        
        Args:
            row: Row index of cell to edit
            col: Column index of cell to edit
        """
        # Finish any existing edit first
        if self.line_edit:
            self.finish_editing()
        
        self.editing_cell = (row, col)
        current_value = self.kernel_config.get_value(row, col)
        
        # Calculate position for the line edit
        x = col * self.cell_size
        y = row * self.cell_size
        
        # Create line edit widget positioned over the cell
        self.line_edit = QLineEdit(self)
        self.line_edit.setGeometry(x + 2, y + 2, self.cell_size - 4, self.cell_size - 4)
        self.line_edit.setText(str(current_value))
        self.line_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.line_edit.setFont(QFont("Arial", 10))
        self.line_edit.selectAll()  # Select text for easy replacement
        self.line_edit.setFocus()
        # Connect signals to finish editing
        self.line_edit.returnPressed.connect(self.finish_editing)  # Enter key
        self.line_edit.editingFinished.connect(self.finish_editing)  # Focus loss
        self.line_edit.show()

    def finish_editing(self):
        """
        Complete editing and save the new value to the kernel config.
        Validates input as a float before saving.
        """
        if not self.line_edit or not self.editing_cell:
            return
        
        text = self.line_edit.text().strip()
        row, col = self.editing_cell
        
        # Try to parse as float, ignore if invalid
        try:
            value = float(text)
            self.kernel_config.set_value(row, col, value)
            self.value_changed.emit()  # Notify listeners of the change
        except ValueError:
            # Invalid input, just ignore and revert
            pass
        
        # Clean up the line edit widget
        self.line_edit.deleteLater()
        self.line_edit = None
        self.editing_cell = None
        self.update()  # Redraw with updated value

    def paintEvent(self, event):
        """
        Render the kernel grid with all cell values.
        
        Each cell shows:
        - White background (yellow if being edited)
        - Gray border
        - Kernel value centered as text (hidden if being edited)
        
        Args:
            event: Paint event (unused)
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw each cell in the kernel grid
        for row in range(self.kernel_config.size):
            for col in range(self.kernel_config.size):
                x = col * self.cell_size
                y = row * self.cell_size
                
                is_editing = self.editing_cell == (row, col)
                
                # Highlight cell being edited with yellow background
                if is_editing:
                    cell_color = QColor(255, 255, 200)  # Light yellow
                else:
                    cell_color = QColor(255, 255, 255)  # White
                
                # Fill cell background
                painter.fillRect(x, y, self.cell_size, self.cell_size, cell_color)
                # Draw cell border
                painter.setPen(QPen(QColor(150, 150, 150), 1))
                painter.drawRect(x, y, self.cell_size, self.cell_size)
                
                # Draw value text (skip if editing, since line edit shows it)
                if not is_editing:
                    value = self.kernel_config.get_value(row, col)
                    painter.setPen(QPen(QColor(50, 50, 50), 1))
                    font = QFont("Arial", 10)
                    painter.setFont(font)
                    
                    # Format: show 2 decimal places, or "0" for zero values
                    value_text = f"{value:.2f}" if value != 0 else "0"
                    
                    # Draw centered text
                    painter.drawText(
                        QRect(x, y, self.cell_size, self.cell_size),
                        Qt.AlignmentFlag.AlignCenter,
                        value_text
                    )
