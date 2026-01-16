from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen, QColor, QMouseEvent
from .number_input_modal import show_number_input_dialog


class PixelGridWidget(QWidget):
    def __init__(self, model, editable=False):
        super().__init__()

        # Store reference to the pixel grid data model
        self._model = model
        # List of cell coordinates (row, col) to highlight with colored borders
        self._highlighted_cells = []
        # Color used for highlighting cells (default: light blue)
        self._highlight_color = QColor(100, 150, 255)
        # Border width in pixels for highlighted cells
        self._highlight_border_width = 3
        # Single cell to draw a special border around (used for output cell indicator)
        self._bordered_cell = None
        # Color used for the bordered cell (default: orange)
        self._border_color = QColor(255, 140, 0)
        # Border width in pixels for the bordered cell
        self._border_width = 3
        # Whether the grid allows user editing via mouse interaction
        self._editable = editable
        # Edit mode: "Toggle" (flip between 0/255) or "Custom" (enter specific value)
        self._edit_mode = "Toggle"
        # Track whether user is currently dragging mouse for continuous editing
        self._is_dragging = False
        # Track the last cell toggled during drag to avoid re-toggling same cell
        self._last_toggled_cell = None
        # Whether to show the pixel values in the grid
        self._show_pixel_values = True
        # Whether to show the pixel colors in the grid
        self._show_colors = True

        # Connect to model's signal to update display when grid data changes
        self._model.grid_changed.connect(self._on_grid_changed)
        
        # Enable mouse tracking to receive mouse move events even without button pressed
        self.setMouseTracking(True)
        # Set minimum widget size to ensure visibility
        self.setMinimumSize(100, 100)
    
    def _on_grid_changed(self, size: int, grid_data: list[list[int]]) -> None:
        # Trigger a repaint when the grid data changes
        self.update()
    
    def set_highlighted_cells(self, cells: list[tuple[int, int]], color: QColor = None) -> None:
        # Set which cells to highlight (e.g., cells under the convolution kernel)
        self._highlighted_cells = cells
        # Optionally update the highlight color
        if color:
            self._highlight_color = color
        # Trigger a repaint to show the new highlights
        self.update()
    
    def set_bordered_cell(self, cell: tuple[int, int] | None, color: QColor = None, width: int = None) -> None:
        # Set a single cell to draw a special border around (e.g., current output cell)
        self._bordered_cell = cell
        # Optionally update the border color
        if color:
            self._border_color = color
        # Optionally update the border width
        if width:
            self._border_width = width
        # Trigger a repaint to show the new border
        self.update()
    
    def clear_highlights(self) -> None:
        # Remove all cell highlights and borders
        self._highlighted_cells = []
        self._bordered_cell = None
        # Trigger a repaint to clear the visual indicators
        self.update()
    
    def set_edit_mode(self, mode: str) -> None:
        # Change the editing mode ("Toggle" or "Custom")
        self._edit_mode = mode
    
    def set_show_pixel_values(self, show: bool) -> None:
        self._show_pixel_values = show
        self.update()
    
    def set_show_colors(self, show: bool) -> None:
        self._show_colors = show
        self.update()
    
    def _get_cell_from_position(self, x: int, y: int) -> tuple[int, int] | None:
        # Convert mouse pixel coordinates to grid cell coordinates (row, col)
        grid_size = self._model.get_grid_size()
        if grid_size == 0:
            return None
        
        # Early return if coordinates are negative
        if x < 0 or y < 0:
            return None
        
        # Get current widget dimensions
        widget_width = self.width()
        widget_height = self.height()
        
        # Calculate cell size based on the smaller dimension to maintain square cells
        min_dimension = min(widget_width, widget_height)
        cell_size = int(min_dimension / grid_size)
        
        # Calculate offsets to account for centered grid
        offset_x = int((widget_width - (cell_size * grid_size)) / 2)
        offset_y = int((widget_height - (cell_size * grid_size)) / 2)
        
        # Adjust coordinates relative to grid origin
        adjusted_x = x - offset_x
        adjusted_y = y - offset_y
        
        # Early return if adjusted coordinates are outside grid area
        if adjusted_x < 0 or adjusted_y < 0:
            return None
        
        # Calculate which cell was clicked
        col = int(adjusted_x / cell_size)
        row = int(adjusted_y / cell_size)
        
        # Verify the cell is within valid grid bounds
        if 0 <= row < grid_size and 0 <= col < grid_size:
            return (row, col)
        
        return None
    
    def mousePressEvent(self, event: QMouseEvent):
        # Handle mouse click events for editing cells
        # Early return if grid is not editable
        if not self._editable:
            return
        
        # Convert click position to cell coordinates
        cell = self._get_cell_from_position(event.pos().x(), event.pos().y())
        if cell is None:
            return
        
        # Get the clicked cell's current value
        row, col = cell
        current_value = self._model.get_grid_data()[row][col]
        
        if self._edit_mode == "Toggle":
            # In Toggle mode: start drag operation and flip cell value between 0 and 255
            self._is_dragging = True
            self._last_toggled_cell = (row, col)
            new_value = 0 if current_value != 0 else 255
            self._model.set_cell(row, col, new_value)
        elif self._edit_mode == "Custom":
            # In Custom mode: show dialog to enter specific value
            new_value, ok = show_number_input_dialog(
                self,
                "Edit Pixel Value",
                f"Enter value for cell ({row}, {col}):",
                current_value,
                0.0,  # Minimum value
                255.0,  # Maximum value
                0  # Number of decimal places
            )
            
            # If user confirmed the dialog, update the cell value
            if ok:
                self._model.set_cell(row, col, int(new_value))
    
    def mouseMoveEvent(self, event: QMouseEvent):
        # Handle mouse drag events for continuous editing in Toggle mode
        # Early return if not editable, not dragging, or not in Toggle mode
        if not self._editable or not self._is_dragging or self._edit_mode != "Toggle":
            return
        
        # Verify left mouse button is still pressed
        if not (event.buttons() & Qt.MouseButton.LeftButton):
            return
        
        # Convert current mouse position to cell coordinates
        cell = self._get_cell_from_position(event.pos().x(), event.pos().y())
        if cell is None:
            return
        
        row, col = cell
        
        # Only toggle if we've moved to a different cell (avoid re-toggling same cell)
        if self._last_toggled_cell != (row, col):
            self._last_toggled_cell = (row, col)
            current_value = self._model.get_grid_data()[row][col]
            new_value = 0 if current_value != 0 else 255
            self._model.set_cell(row, col, new_value)
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        # End drag operation when mouse button is released
        self._is_dragging = False
        self._last_toggled_cell = None
    
    def paintEvent(self, event):
        # Create painter object for drawing the grid
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False) # Disable antialiasing for sharp pixel edges
        
        # Retrieve current grid data and size from the model
        grid_data = self._model.get_grid_data()
        grid_size = self._model.get_grid_size()
        
        # Early return if grid size is invalid to avoid division by zero
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
        
        # Draw all cells with their values as grayscale colors
        for row in range(grid_size):
            for col in range(grid_size):
                # Calculate pixel position for current cell
                x = offset_x + col * cell_size
                y = offset_y + row * cell_size
                
                # Get cell value (0-255) and create grayscale color
                cell_value = grid_data[row][col]
                
                if self._show_colors:
                    cell_color = QColor(cell_value, cell_value, cell_value)
                else:
                    cell_color = QColor(255, 255, 255)
                
                # Fill the cell with its color
                painter.fillRect(x, y, cell_size, cell_size, cell_color)
                
                # Draw the cell border
                painter.setPen(border_pen)
                painter.drawRect(x, y, cell_size, cell_size)
                
                if self._show_pixel_values:
                    if self._show_colors:
                        text_color = QColor(0, 0, 0) if cell_value > 127 else QColor(255, 255, 255)
                    else:
                        text_color = QColor(0, 0, 0)
                    painter.setPen(text_color)
                    
                    font = painter.font()
                    font_size = max(6, int(cell_size * 0.3))
                    font.setPixelSize(font_size)
                    painter.setFont(font)
                    
                    from PySide6.QtCore import QRect
                    text_rect = QRect(x, y, cell_size, cell_size)
                    painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, str(cell_value))
        
        # Draw highlighted cell borders (e.g., for cells under the kernel)
        for row, col in self._highlighted_cells:
            # Verify cell is within valid grid bounds
            if 0 <= row < grid_size and 0 <= col < grid_size:
                # Calculate pixel position for the highlighted cell
                x = offset_x + col * cell_size
                y = offset_y + row * cell_size
                
                # Configure pen for highlight border
                highlight_pen = QPen(self._highlight_color)
                highlight_pen.setWidth(self._highlight_border_width)
                highlight_pen.setCosmetic(True)
                painter.setPen(highlight_pen)
                # Draw the highlight border over the cell
                painter.drawRect(x, y, cell_size, cell_size)
        
        # Draw special border around the bordered cell (e.g., current output cell)
        if self._bordered_cell is not None:
            row, col = self._bordered_cell
            # Verify cell is within valid grid bounds
            if 0 <= row < grid_size and 0 <= col < grid_size:
                # Calculate pixel position for the bordered cell
                x = offset_x + col * cell_size
                y = offset_y + row * cell_size
                
                # Configure pen for special border
                border_pen = QPen(self._border_color)
                border_pen.setWidth(self._border_width)
                border_pen.setCosmetic(True)
                painter.setPen(border_pen)
                # Draw the special border over the cell
                painter.drawRect(x, y, cell_size, cell_size)