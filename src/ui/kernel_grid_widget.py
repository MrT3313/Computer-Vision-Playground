from PySide6.QtWidgets import QWidget, QLineEdit
from PySide6.QtCore import Qt, Signal, QRect
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QMouseEvent

from src.core.kernel_config import KernelConfig


class KernelGridWidget(QWidget):
    value_changed = Signal()
    
    def __init__(self, kernel_config: KernelConfig, parent=None):
        super().__init__(parent)
        self.kernel_config = kernel_config
        self.cell_size = 45
        self.editing_cell = None
        self.line_edit = None
        
        self.update_size()
        self.setMouseTracking(True)

    def update_size(self):
        size = self.kernel_config.size
        self.setMinimumSize(
            size * self.cell_size + 1,
            size * self.cell_size + 1
        )
        self.setMaximumSize(
            size * self.cell_size + 1,
            size * self.cell_size + 1
        )

    def get_cell_at_position(self, x: float, y: float) -> tuple[int, int]:
        col = int(x) // self.cell_size
        row = int(y) // self.cell_size
        return row, col

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            row, col = self.get_cell_at_position(event.position().x(), event.position().y())
            if 0 <= row < self.kernel_config.size and 0 <= col < self.kernel_config.size:
                self.start_editing(row, col)

    def start_editing(self, row: int, col: int):
        if self.line_edit:
            self.finish_editing()
        
        self.editing_cell = (row, col)
        current_value = self.kernel_config.get_value(row, col)
        
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
        
        text = self.line_edit.text().strip()
        row, col = self.editing_cell
        
        try:
            value = float(text)
            self.kernel_config.set_value(row, col, value)
            self.value_changed.emit()
        except ValueError:
            pass
        
        self.line_edit.deleteLater()
        self.line_edit = None
        self.editing_cell = None
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        for row in range(self.kernel_config.size):
            for col in range(self.kernel_config.size):
                x = col * self.cell_size
                y = row * self.cell_size
                
                is_editing = self.editing_cell == (row, col)
                
                if is_editing:
                    cell_color = QColor(255, 255, 200)
                else:
                    cell_color = QColor(255, 255, 255)
                
                painter.fillRect(x, y, self.cell_size, self.cell_size, cell_color)
                painter.setPen(QPen(QColor(150, 150, 150), 1))
                painter.drawRect(x, y, self.cell_size, self.cell_size)
                
                if not is_editing:
                    value = self.kernel_config.get_value(row, col)
                    painter.setPen(QPen(QColor(50, 50, 50), 1))
                    font = QFont("Arial", 10)
                    painter.setFont(font)
                    
                    value_text = f"{value:.2f}" if value != 0 else "0"
                    
                    painter.drawText(
                        QRect(x, y, self.cell_size, self.cell_size),
                        Qt.AlignmentFlag.AlignCenter,
                        value_text
                    )
