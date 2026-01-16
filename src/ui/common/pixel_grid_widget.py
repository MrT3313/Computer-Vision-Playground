from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen, QColor


class PixelGridWidget(QWidget):
    def __init__(self, model):
        super().__init__()

        # Store reference to the data model that contains the grid state
        self._model = model

        # Connect to model's signal to update display when grid data changes
        self._model.grid_changed.connect(self._on_grid_changed)
        
        # Set minimum widget size to ensure visibility
        self.setMinimumSize(100, 100)

        # Configure white background for the widget
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(255, 255, 255))
        self.setPalette(palette)
    
    def _on_grid_changed(self, size: int, grid_data: list[list[int]]) -> None:
        # Force widget to repaint when grid data changes
        self.update()
    
    def paintEvent(self, event):
        # Create painter object for drawing the grid
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        
        # Retrieve current grid data and size from the model
        grid_data = self._model.get_grid_data()
        grid_size = self._model.get_grid_size()
        
        # If grid size is 0, return early to avoid division by zero
        if grid_size == 0:
            return
        
        # Get current widget dimensions
        widget_width = self.width()
        widget_height = self.height()
        
        # Calculate cell size based on the smaller dimension to maintain square cells
        min_dimension = min(widget_width, widget_height)
        cell_size = int(min_dimension / grid_size)
        
        # Calculate offsets to center the grid within the widget
        offset_x = int((widget_width - (cell_size * grid_size)) / 2)
        offset_y = int((widget_height - (cell_size * grid_size)) / 2)
        
        # Configure pen for drawing cell borders
        border_color = QColor(100, 100, 100)
        border_pen = QPen(border_color)
        border_pen.setWidth(1) # Set border line width to 1 pixel
        border_pen.setCosmetic(True) # Ensure border width remains constant regardless of transformations
        
        # Iterate through each cell in the grid
        for row in range(grid_size):
            for col in range(grid_size):
                # Calculate pixel position for current cell
                x = offset_x + col * cell_size
                y = offset_y + row * cell_size
                
                # Get cell value (0-255) and create grayscale color
                cell_value = grid_data[row][col]
                cell_color = QColor(cell_value, cell_value, cell_value)
                
                # Fill the cell with its color
                painter.fillRect(x, y, cell_size, cell_size, cell_color)
                
                # Draw the cell border
                painter.setPen(border_pen)
                painter.drawRect(x, y, cell_size, cell_size)
