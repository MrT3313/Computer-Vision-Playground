from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QMouseEvent

from src.core.image_data import ImageData
from src.ui.common.pixel_grid_base import PixelGridBase


class RawInputImageWidget(PixelGridBase):
    pixel_clicked = Signal(int, int)
    
    def __init__(self, image_data: ImageData, parent=None, cell_size: int = 20):
        super().__init__(
            image_data=image_data,
            show_values=False,
            parent=parent,
            cell_size=cell_size
        )
        self.setMouseTracking(True)
        self.is_drawing = False
        self.last_drawn_cell = (-1, -1)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            row, col = self.get_cell_at_position(event.position().x(), event.position().y())
            if 0 <= row < self.image_data.height and 0 <= col < self.image_data.width:
                self.is_drawing = True
                self.last_drawn_cell = (row, col)
                self.image_data.toggle_pixel(row, col)
                self.pixel_clicked.emit(row, col)
                self.update()

    def mouseMoveEvent(self, event: QMouseEvent):
        if not self.is_drawing:
            return
        
        row, col = self.get_cell_at_position(event.position().x(), event.position().y())
        if 0 <= row < self.image_data.height and 0 <= col < self.image_data.width:
            if (row, col) != self.last_drawn_cell:
                self.last_drawn_cell = (row, col)
                self.image_data.toggle_pixel(row, col)
                self.pixel_clicked.emit(row, col)
                self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_drawing = False
            self.last_drawn_cell = (-1, -1)
