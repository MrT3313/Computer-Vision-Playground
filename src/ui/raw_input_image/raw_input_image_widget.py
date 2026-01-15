from PySide6.QtCore import Qt, Signal, QRect
from PySide6.QtGui import QMouseEvent, QFont, QPainter, QPen, QColor
from PySide6.QtWidgets import QLineEdit

from src.core.image_data import ImageData
from src.ui.common.pixel_grid_base import PixelGridBase
from src.consts.defaults import DEFAULT_IMAGE_GRID_CELL_SIZE


class RawInputImageWidget(PixelGridBase):
    pixel_clicked = Signal(int, int)
    
    def __init__(self, image_data: ImageData, parent=None, cell_size: int = DEFAULT_IMAGE_GRID_CELL_SIZE):
        super().__init__(
            image_data=image_data,
            show_values=True,
            parent=parent,
            cell_size=cell_size
        )
        self.setMouseTracking(True)
        self.is_drawing = False
        self.last_drawn_cell = (-1, -1)
        self.mode = "Toggle"
        self.editing_cell = None
        self.line_edit = None

    def set_mode(self, mode: str):
        self.mode = mode
        if self.line_edit:
            self.finish_editing()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            row, col = self.get_cell_at_position(event.position().x(), event.position().y())
            if 0 <= row < self.image_data.height and 0 <= col < self.image_data.width:
                if self.mode == "Toggle":
                    self.is_drawing = True
                    self.last_drawn_cell = (row, col)
                    self.image_data.toggle_pixel(row, col)
                    self.pixel_clicked.emit(row, col)
                    self.update()
                else:
                    self.start_editing(row, col)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.mode == "Toggle" and self.is_drawing:
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
    
    def start_editing(self, row: int, col: int):
        if self.line_edit:
            self.finish_editing()
        
        self.editing_cell = (row, col)
        current_value = self.image_data.get_pixel(row, col)
        
        x = col * self.cell_size
        y = row * self.cell_size
        
        self.line_edit = QLineEdit(self)
        self.line_edit.setGeometry(x + 2, y + 2, self.cell_size - 4, self.cell_size - 4)
        self.line_edit.setText(str(current_value))
        self.line_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.line_edit.setFont(QFont("Arial", 10))
        self.line_edit.selectAll()
        self.line_edit.setFocus()
        self.line_edit.returnPressed.connect(self.finish_editing)
        self.line_edit.editingFinished.connect(self.finish_editing)
        self.line_edit.show()

    def finish_editing(self):
        if not self.line_edit or not self.editing_cell:
            return
        
        line_edit = self.line_edit
        text = line_edit.text().strip()
        row, col = self.editing_cell
        
        self.line_edit = None
        self.editing_cell = None
        
        try:
            value = float(text)
            value = max(0, min(255, value))
            self.image_data.set_pixel(row, col, int(value))
            self.pixel_clicked.emit(row, col)
        except ValueError:
            pass
        
        line_edit.hide()
        line_edit.deleteLater()
        self.update()
