from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtCore import Qt, QRect, QSize
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QMouseEvent
from consts import DEFAULT_KERNEL_CELL_SIZE
from ui.common import show_number_input_dialog


class KernelGridWidget(QWidget):
    def __init__(self, model):
        super().__init__()
        
        # Store reference to the kernel data model
        self._model = model
        # Connect to model's signal to update display when kernel data changes
        self._model.grid_changed.connect(self._on_grid_changed)
        
        # Set fixed size policy so widget doesn't resize beyond calculated dimensions
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        # Configure white background for the widget
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(255, 255, 255))
        self.setPalette(palette)
    
    def _on_grid_changed(self, size: int, grid_data: list[list[float]]) -> None:
        # Recalculate widget size based on new grid size
        grid_size = self._model.get_grid_size()
        widget_size = grid_size * DEFAULT_KERNEL_CELL_SIZE
        self.setFixedSize(widget_size, widget_size)
        # Trigger a repaint to display the updated grid
        self.update()
    
    def sizeHint(self) -> QSize:
        # Calculate and return the preferred size based on grid size and cell size
        grid_size = self._model.get_grid_size()
        size = grid_size * DEFAULT_KERNEL_CELL_SIZE
        return QSize(size, size)
    
    def minimumSizeHint(self) -> QSize:
        # Minimum size is the same as the preferred size for fixed-size widget
        return self.sizeHint()
    
    def mousePressEvent(self, event: QMouseEvent):
        # Early return if widget is disabled
        if not self.isEnabled():
            return
        
        # Get current grid size
        grid_size = self._model.get_grid_size()
        if grid_size == 0:
            return
        
        # Get click coordinates relative to widget
        click_x = event.pos().x()
        click_y = event.pos().y()
        
        # Early return if click is outside valid area
        if click_x < 0 or click_y < 0:
            return
        
        # Calculate which cell was clicked based on click position
        col = int(click_x / DEFAULT_KERNEL_CELL_SIZE)
        row = int(click_y / DEFAULT_KERNEL_CELL_SIZE)
        
        # Verify the clicked cell is within valid grid bounds
        if 0 <= row < grid_size and 0 <= col < grid_size:
            # Get the current value of the clicked cell
            current_value = self._model.get_value(row, col)
            # Show input dialog to allow user to edit the kernel value
            new_value, ok = show_number_input_dialog(
                self,
                "Edit Kernel Value",
                f"Enter value for cell ({row}, {col}):",
                current_value,
                -1000.0,
                1000.0,
                2
            )
            
            # If user confirmed the dialog, update the cell value in the model
            if ok:
                self._model.set_cell(row, col, new_value)
    
    def paintEvent(self, event):
        # Create painter object for drawing the kernel grid
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False) # Disable antialiasing for sharp edges
        
        # Retrieve current kernel data and size from the model
        grid_data = self._model.get_grid_data()
        grid_size = self._model.get_grid_size()
        
        # Early return if grid size is invalid
        if grid_size == 0:
            return
        
        # Configure pen for drawing cell borders
        border_color = QColor(150, 150, 150)
        border_pen = QPen(border_color)
        border_pen.setWidth(1) # Set border line width to 1 pixel
        border_pen.setCosmetic(True) # Ensure border width remains constant regardless of transformations
        
        # Configure colors for cell background and text
        cell_bg_color = QColor(240, 240, 240)
        text_color = QColor(50, 50, 50)
        text_pen = QPen(text_color)
        
        # Set font for displaying kernel values
        font = QFont("Arial", 10)
        painter.setFont(font)
        
        # Iterate through each cell in the kernel grid
        for row in range(grid_size):
            for col in range(grid_size):
                # Calculate pixel position for current cell
                x = col * DEFAULT_KERNEL_CELL_SIZE
                y = row * DEFAULT_KERNEL_CELL_SIZE
                
                # Fill the cell with background color
                painter.fillRect(x, y, DEFAULT_KERNEL_CELL_SIZE, DEFAULT_KERNEL_CELL_SIZE, cell_bg_color)
                
                # Draw the cell border
                painter.setPen(border_pen)
                painter.drawRect(x, y, DEFAULT_KERNEL_CELL_SIZE, DEFAULT_KERNEL_CELL_SIZE)
                
                # Get cell value and format for display
                cell_value = grid_data[row][col]
                # Format value to 2 decimal places, display "0" for zero values
                value_text = f"{cell_value:.2f}" if cell_value != 0 else "0"
                
                # Draw the kernel value text centered in the cell
                painter.setPen(text_pen)
                painter.drawText(
                    QRect(x, y, DEFAULT_KERNEL_CELL_SIZE, DEFAULT_KERNEL_CELL_SIZE),
                    Qt.AlignmentFlag.AlignCenter,
                    value_text
                )