from PySide6.QtWidgets import QWidget, QInputDialog
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QMouseEvent


class KernelGridWidget(QWidget):
    def __init__(self, model):
        super().__init__()
        
        self._model = model
        self._model.grid_changed.connect(self._on_grid_changed)
        
        self.setMinimumSize(100, 100)
        
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(255, 255, 255))
        self.setPalette(palette)
    
    def _on_grid_changed(self, size: int, grid_data: list[list[float]]) -> None:
        self.update()
    
    def mousePressEvent(self, event: QMouseEvent):
        if not self.isEnabled():
            return
        
        grid_size = self._model.get_grid_size()
        if grid_size == 0:
            return
        
        widget_width = self.width()
        widget_height = self.height()
        min_dimension = min(widget_width, widget_height)
        cell_size = int(min_dimension / grid_size)
        
        offset_x = int((widget_width - (cell_size * grid_size)) / 2)
        offset_y = int((widget_height - (cell_size * grid_size)) / 2)
        
        click_x = event.pos().x() - offset_x
        click_y = event.pos().y() - offset_y
        
        if click_x < 0 or click_y < 0:
            return
        
        col = int(click_x / cell_size)
        row = int(click_y / cell_size)
        
        if 0 <= row < grid_size and 0 <= col < grid_size:
            current_value = self._model.get_value(row, col)
            new_value, ok = QInputDialog.getDouble(
                self,
                "Edit Kernel Value",
                f"Enter value for cell ({row}, {col}):",
                current_value,
                -1000.0,
                1000.0,
                2
            )
            
            if ok:
                self._model.set_cell(row, col, new_value)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        
        grid_data = self._model.get_grid_data()
        grid_size = self._model.get_grid_size()
        
        if grid_size == 0:
            return
        
        widget_width = self.width()
        widget_height = self.height()
        
        min_dimension = min(widget_width, widget_height)
        cell_size = int(min_dimension / grid_size)
        
        offset_x = int((widget_width - (cell_size * grid_size)) / 2)
        offset_y = int((widget_height - (cell_size * grid_size)) / 2)
        
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
                x = offset_x + col * cell_size
                y = offset_y + row * cell_size
                
                painter.fillRect(x, y, cell_size, cell_size, cell_bg_color)
                
                painter.setPen(border_pen)
                painter.drawRect(x, y, cell_size, cell_size)
                
                cell_value = grid_data[row][col]
                value_text = f"{cell_value:.2f}" if cell_value != 0 else "0"
                
                painter.setPen(text_pen)
                painter.drawText(
                    QRect(x, y, cell_size, cell_size),
                    Qt.AlignmentFlag.AlignCenter,
                    value_text
                )
