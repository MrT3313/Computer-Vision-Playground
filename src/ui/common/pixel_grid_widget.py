from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen, QColor


class PixelGridWidget(QWidget):
    def __init__(self, model):
        super().__init__()

        self._model = model
        self._highlighted_cells = []
        self._highlight_color = QColor(100, 150, 255)
        self._highlight_border_width = 3
        self._bordered_cell = None
        self._border_color = QColor(255, 140, 0)
        self._border_width = 3

        self._model.grid_changed.connect(self._on_grid_changed)
        
        self.setMinimumSize(100, 100)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(255, 255, 255))
        self.setPalette(palette)
    
    def _on_grid_changed(self, size: int, grid_data: list[list[int]]) -> None:
        self.update()
    
    def set_highlighted_cells(self, cells: list[tuple[int, int]], color: QColor = None) -> None:
        self._highlighted_cells = cells
        if color:
            self._highlight_color = color
        self.update()
    
    def set_bordered_cell(self, cell: tuple[int, int] | None, color: QColor = None, width: int = None) -> None:
        self._bordered_cell = cell
        if color:
            self._border_color = color
        if width:
            self._border_width = width
        self.update()
    
    def clear_highlights(self) -> None:
        self._highlighted_cells = []
        self._bordered_cell = None
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
        
        for row in range(grid_size):
            for col in range(grid_size):
                x = offset_x + col * cell_size
                y = offset_y + row * cell_size
                
                cell_value = grid_data[row][col]
                cell_color = QColor(cell_value, cell_value, cell_value)
                
                painter.fillRect(x, y, cell_size, cell_size, cell_color)
                
                painter.setPen(border_pen)
                painter.drawRect(x, y, cell_size, cell_size)
        
        for row, col in self._highlighted_cells:
            if 0 <= row < grid_size and 0 <= col < grid_size:
                x = offset_x + col * cell_size
                y = offset_y + row * cell_size
                
                highlight_pen = QPen(self._highlight_color)
                highlight_pen.setWidth(self._highlight_border_width)
                highlight_pen.setCosmetic(True)
                painter.setPen(highlight_pen)
                painter.drawRect(x, y, cell_size, cell_size)
        
        if self._bordered_cell is not None:
            row, col = self._bordered_cell
            if 0 <= row < grid_size and 0 <= col < grid_size:
                x = offset_x + col * cell_size
                y = offset_y + row * cell_size
                
                border_pen = QPen(self._border_color)
                border_pen.setWidth(self._border_width)
                border_pen.setCosmetic(True)
                painter.setPen(border_pen)
                painter.drawRect(x, y, cell_size, cell_size)
