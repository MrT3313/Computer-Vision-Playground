from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QPen, QColor, QFont

from src.core.image_data import ImageData
from src.consts.defaults import DEFAULT_IMAGE_GRID_CELL_SIZE


class PixelGridBase(QWidget):
    def __init__(
        self,
        image_data: ImageData,
        show_values: bool = False,
        show_colors: bool = True,
        parent=None,
        cell_size: int = DEFAULT_IMAGE_GRID_CELL_SIZE
    ):
        super().__init__(parent)
        self.image_data = image_data
        self.cell_size = cell_size
        self.show_values = show_values
        self.show_colors = show_colors
        
        self.setMinimumSize(
            self.image_data.width * self.cell_size + 1,
            self.image_data.height * self.cell_size + 1
        )
        
        self.kernel_highlight_row = -1
        self.kernel_highlight_col = -1
        self.kernel_size = 3
        
        self.output_highlight_row = -1
        self.output_highlight_col = -1
        
        self.offset_x = 0
        self.offset_y = 0

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
    
    def set_show_colors(self, show_colors: bool):
        self.show_colors = show_colors
        self.update()

    def set_show_values(self, show_values: bool):
        self.show_values = show_values
        self.update()

    def get_cell_at_position(self, x: float, y: float) -> tuple[int, int]:
        adjusted_x = x - self.offset_x
        adjusted_y = y - self.offset_y
        col = int(adjusted_x) // self.cell_size
        row = int(adjusted_y) // self.cell_size
        return row, col

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        self.offset_x = (self.width() - (self.image_data.width * self.cell_size)) // 2
        self.offset_y = (self.height() - (self.image_data.height * self.cell_size)) // 2

        for row in range(self.image_data.height):
            for col in range(self.image_data.width):
                x = col * self.cell_size + self.offset_x
                y = row * self.cell_size + self.offset_y
                
                pixel_value = self.image_data.get_pixel(row, col)
                
                if pixel_value is None:
                    cell_color = QColor(255, 255, 255)
                elif self.show_colors:
                    cell_color = QColor(pixel_value, pixel_value, pixel_value)
                else:
                    cell_color = QColor(255, 255, 255)
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
                
                if self.show_values and pixel_value is not None:
                    text_color = QColor(255, 0, 0) if pixel_value == 0 else QColor(100, 100, 100)
                    painter.setPen(QPen(text_color, 1))
                    font = QFont("Arial", 8)
                    painter.setFont(font)
                    painter.drawText(
                        QRect(x, y, self.cell_size, self.cell_size),
                        Qt.AlignmentFlag.AlignCenter,
                        str(pixel_value)
                    )

        if self.kernel_highlight_row >= 0 and self.kernel_highlight_col >= 0:
            x = self.kernel_highlight_col * self.cell_size + self.offset_x
            y = self.kernel_highlight_row * self.cell_size + self.offset_y
            width = self.kernel_size * self.cell_size
            height = self.kernel_size * self.cell_size
            
            painter.setPen(QPen(QColor(0, 150, 255), 4))
            painter.drawRect(x, y, width, height)
