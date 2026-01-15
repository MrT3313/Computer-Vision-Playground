from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, QRect
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QMouseEvent

from src.core.image_data import ImageData


class PixelGridWidget(QWidget):
    pixel_clicked = Signal(int, int)
    
    def __init__(
        self,
        image_data: ImageData,
        editable: bool = True,
        show_values: bool = False,
        parent=None
    ):
        super().__init__(parent)
        self.image_data = image_data
        self.editable = editable
        self.show_values = show_values
        
        self.cell_size = 30
        self.kernel_highlight_row = -1
        self.kernel_highlight_col = -1
        self.kernel_size = 3
        self.output_highlight_row = -1
        self.output_highlight_col = -1
        
        self.is_drawing = False
        self.last_drawn_cell = (-1, -1)
        
        self.setMinimumSize(
            self.image_data.width * self.cell_size + 1,
            self.image_data.height * self.cell_size + 1
        )

    def set_image_data(self, image_data: ImageData):
        self.image_data = image_data
        self.setMinimumSize(
            self.image_data.width * self.cell_size + 1,
            self.image_data.height * self.cell_size + 1
        )
        self.update()

    def set_kernel_highlight(self, row: int, col: int, kernel_size: int):
        self.kernel_highlight_row = row
        self.kernel_highlight_col = col
        self.kernel_size = kernel_size
        self.update()

    def clear_kernel_highlight(self):
        self.kernel_highlight_row = -1
        self.kernel_highlight_col = -1
        self.update()

    def set_output_highlight(self, row: int, col: int):
        self.output_highlight_row = row
        self.output_highlight_col = col
        self.update()

    def clear_output_highlight(self):
        self.output_highlight_row = -1
        self.output_highlight_col = -1
        self.update()

    def get_cell_at_position(self, x: int, y: int) -> tuple[int, int]:
        col = x // self.cell_size
        row = y // self.cell_size
        return row, col

    def mousePressEvent(self, event: QMouseEvent):
        if not self.editable:
            return
        
        if event.button() == Qt.MouseButton.LeftButton:
            row, col = self.get_cell_at_position(event.position().x(), event.position().y())
            if 0 <= row < self.image_data.height and 0 <= col < self.image_data.width:
                self.is_drawing = True
                self.last_drawn_cell = (row, col)
                self.image_data.toggle_pixel(row, col)
                self.pixel_clicked.emit(row, col)
                self.update()

    def mouseMoveEvent(self, event: QMouseEvent):
        if not self.editable or not self.is_drawing:
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

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        for row in range(self.image_data.height):
            for col in range(self.image_data.width):
                x = col * self.cell_size
                y = row * self.cell_size
                
                pixel_value = self.image_data.get_pixel(row, col)
                cell_color = QColor(pixel_value, pixel_value, pixel_value)
                painter.fillRect(x, y, self.cell_size, self.cell_size, cell_color)
                
                in_kernel = (
                    self.kernel_highlight_row >= 0 and
                    self.kernel_highlight_col >= 0 and
                    self.kernel_highlight_row <= row < self.kernel_highlight_row + self.kernel_size and
                    self.kernel_highlight_col <= col < self.kernel_highlight_col + self.kernel_size
                )
                
                is_output_cell = (
                    self.output_highlight_row >= 0 and
                    self.output_highlight_col >= 0 and
                    row == self.output_highlight_row and 
                    col == self.output_highlight_col
                )
                
                if in_kernel:
                    painter.setPen(QPen(QColor(0, 150, 255), 3))
                elif is_output_cell:
                    painter.setPen(QPen(QColor(255, 100, 0), 3))
                else:
                    painter.setPen(QPen(QColor(200, 200, 200), 1))
                
                painter.drawRect(x, y, self.cell_size, self.cell_size)
                
                if self.show_values:
                    painter.setPen(QPen(QColor(255, 0, 0) if pixel_value == 0 else QColor(100, 100, 100), 1))
                    font = QFont("Arial", 8)
                    painter.setFont(font)
                    painter.drawText(
                        QRect(x, y, self.cell_size, self.cell_size),
                        Qt.AlignmentFlag.AlignCenter,
                        str(pixel_value)
                    )

        if self.kernel_highlight_row >= 0 and self.kernel_highlight_col >= 0:
            x = self.kernel_highlight_col * self.cell_size
            y = self.kernel_highlight_row * self.cell_size
            width = self.kernel_size * self.cell_size
            height = self.kernel_size * self.cell_size
            
            painter.setPen(QPen(QColor(0, 150, 255), 4))
            painter.drawRect(x, y, width, height)
