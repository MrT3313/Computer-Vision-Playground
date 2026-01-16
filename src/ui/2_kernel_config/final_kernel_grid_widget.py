from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtCore import Qt, QRect, QSize
from PySide6.QtGui import QPainter, QPen, QColor, QFont
from consts import DEFAULT_KERNEL_CELL_SIZE


class FinalKernelGridWidget(QWidget):
    def __init__(self, model, constant: float = 1.0):
        super().__init__()
        
        self._model = model
        self._constant = constant
        
        self._model.grid_changed.connect(self._on_grid_changed)
        
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(255, 255, 255))
        self.setPalette(palette)
    
    def set_constant(self, constant: float) -> None:
        self._constant = constant
        self.update()
    
    def _on_grid_changed(self, size: int, grid_data: list[list[float]]) -> None:
        grid_size = self._model.get_grid_size()
        widget_size = grid_size * DEFAULT_KERNEL_CELL_SIZE
        self.setFixedSize(widget_size, widget_size)
        self.update()
    
    def sizeHint(self) -> QSize:
        grid_size = self._model.get_grid_size()
        size = grid_size * DEFAULT_KERNEL_CELL_SIZE
        return QSize(size, size)
    
    def minimumSizeHint(self) -> QSize:
        return self.sizeHint()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        
        grid_data = self._model.get_grid_data()
        grid_size = self._model.get_grid_size()
        
        if grid_size == 0:
            return
        
        border_color = QColor(150, 150, 150)
        border_pen = QPen(border_color)
        border_pen.setWidth(1)
        border_pen.setCosmetic(True)
        
        cell_bg_color = QColor(240, 240, 240)
        text_color = QColor(50, 50, 50)
        text_pen = QPen(text_color)
        
        font = QFont("Arial", 10)
        painter.setFont(font)
        
        for row in range(grid_size):
            for col in range(grid_size):
                x = col * DEFAULT_KERNEL_CELL_SIZE
                y = row * DEFAULT_KERNEL_CELL_SIZE
                
                painter.fillRect(x, y, DEFAULT_KERNEL_CELL_SIZE, DEFAULT_KERNEL_CELL_SIZE, cell_bg_color)
                
                painter.setPen(border_pen)
                painter.drawRect(x, y, DEFAULT_KERNEL_CELL_SIZE, DEFAULT_KERNEL_CELL_SIZE)
                
                kernel_value = grid_data[row][col]
                final_value = kernel_value * self._constant
                value_text = f"{final_value:.2f}" if final_value != 0 else "0"
                
                painter.setPen(text_pen)
                painter.drawText(
                    QRect(x, y, DEFAULT_KERNEL_CELL_SIZE, DEFAULT_KERNEL_CELL_SIZE),
                    Qt.AlignmentFlag.AlignCenter,
                    value_text
                )
