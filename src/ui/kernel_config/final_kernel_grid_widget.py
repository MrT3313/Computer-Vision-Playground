from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QPen, QColor, QFont

from src.core.filter_config import KernelConfig
from src.consts.defaults import DEFAULT_KERNEL_GRID_CELL_SIZE


class FinalKernelGridWidget(QWidget):
    def __init__(self, kernel_config: KernelConfig, constant: float = 1.0, parent=None):
        super().__init__(parent)
        self.kernel_config = kernel_config
        self.constant = constant
        self.cell_size = DEFAULT_KERNEL_GRID_CELL_SIZE
        
        self.offset_x = 0
        self.offset_y = 0
        
        self.update_size()

    def update_size(self):
        size = self.kernel_config.size
        widget_size = size * self.cell_size + 1
        self.setMinimumSize(widget_size, widget_size)
        self.setMaximumSize(widget_size, widget_size)

    def set_constant(self, constant: float):
        self.constant = constant
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        self.offset_x = (self.width() - (self.kernel_config.size * self.cell_size)) // 2
        self.offset_y = (self.height() - (self.kernel_config.size * self.cell_size)) // 2

        for row in range(self.kernel_config.size):
            for col in range(self.kernel_config.size):
                x = col * self.cell_size + self.offset_x
                y = row * self.cell_size + self.offset_y
                
                cell_color = QColor(240, 240, 240)
                
                painter.fillRect(x, y, self.cell_size, self.cell_size, cell_color)
                painter.setPen(QPen(QColor(150, 150, 150), 1))
                painter.drawRect(x, y, self.cell_size, self.cell_size)
                
                value = self.kernel_config.get_value(row, col)
                final_value = value * self.constant
                painter.setPen(QPen(QColor(50, 50, 50), 1))
                font = QFont("Arial", 10)
                painter.setFont(font)
                
                value_text = f"{final_value:.2f}" if final_value != 0 else "0"
                
                painter.drawText(
                    QRect(x, y, self.cell_size, self.cell_size),
                    Qt.AlignmentFlag.AlignCenter,
                    value_text
                )
