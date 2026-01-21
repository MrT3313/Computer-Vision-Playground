from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtCore import Qt, QRect, QSize
from PySide6.QtGui import QPainter, QPen, QColor, QFont
from consts import DEFAULT_KERNEL_CELL_SIZE
from utils.kernel_utils import flip_kernel_180


class FinalKernelGridWidget(QWidget):
    def __init__(self, model, constant: float = 1.0):
        super().__init__()
        
        # Store reference to the kernel data model
        self._model = model
        # Store the constant multiplier to apply to kernel values
        self._constant = constant
        # Store the filter type to determine if kernel flipping is needed
        self._filter_type = "Cross-Correlation"
        
        # Connect to model's signal to update display when kernel data changes
        self._model.grid_changed.connect(self._on_grid_changed)
        
        # Set fixed size policy so widget doesn't resize beyond calculated dimensions
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        # Configure white background for the widget
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(255, 255, 255))
        self.setPalette(palette)
    
    def set_constant(self, constant: float) -> None:
        # Update the constant multiplier and trigger a repaint
        self._constant = constant
        self.update()
    
    def set_filter_type(self, filter_type: str) -> None:
        # Update the filter type and trigger a repaint
        self._filter_type = filter_type
        self.update()
    
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
        
        if self._filter_type == "Convolution":
            grid_data = flip_kernel_180(grid_data)
        
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
                
                # Calculate final kernel value by multiplying with constant
                kernel_value = grid_data[row][col]
                final_value = kernel_value * self._constant
                # Format value to 2 decimal places, display "0" for zero values
                value_text = f"{final_value:.2f}" if final_value != 0 else "0"
                
                # Draw the kernel value text centered in the cell
                painter.setPen(text_pen)
                painter.drawText(
                    QRect(x, y, DEFAULT_KERNEL_CELL_SIZE, DEFAULT_KERNEL_CELL_SIZE),
                    Qt.AlignmentFlag.AlignCenter,
                    value_text
                )