from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QFontMetrics


class CalculationTableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._calculations = []
        self._label_width = 0
        self._cell_widths = []
        self._cell_height = 30
        self._row_count = 6
        self.setMinimumHeight(self._row_count * self._cell_height)
    
    def set_calculations(self, calculations: list) -> None:
        self._calculations = calculations
        if self._calculations:
            self._calculate_dimensions()
            total_width = self._label_width + sum(self._cell_widths)
            height = self._row_count * self._cell_height
            self.setMinimumWidth(total_width)
            self.setFixedHeight(height)
        self.update()
        self.updateGeometry()
    
    def _calculate_dimensions(self):
        font = QFont("Arial", 11)
        bold_font = QFont("Arial", 11)
        bold_font.setBold(True)
        
        row_labels = [
            "",
            "Coordinates:",
            "Values:",
            "Kernel Adjusted Calculations:",
            "Kernel Adjusted Values:",
            "Bounded Values:"
        ]
        
        bold_metrics = QFontMetrics(bold_font)
        
        max_label_width = 0
        for label in row_labels:
            label_width = bold_metrics.horizontalAdvance(label + "  ")
            max_label_width = max(max_label_width, label_width)
        
        self._label_width = max_label_width + 20
        
        metrics = QFontMetrics(font)
        self._cell_widths = []
        
        for calc in self._calculations:
            max_width = 0
            
            texts = [
                str(calc['index']),
                f"({calc['coordinate'][0]},{calc['coordinate'][1]})",
                str(calc['input_value']),
                f"({calc['input_value']}×{calc['final_kernel_value']:.2f})",
                f"{calc['result']:.2f}",
                f"{calc['bounded_result']:.2f}"
            ]
            
            for text in texts:
                text_width = metrics.horizontalAdvance(text)
                max_width = max(max_width, text_width)
            
            self._cell_widths.append(max_width + 30)
    
    def sizeHint(self) -> QSize:
        if not self._calculations:
            return QSize(400, self._row_count * self._cell_height)
        
        total_width = self._label_width + sum(self._cell_widths)
        height = self._row_count * self._cell_height
        return QSize(total_width, height)
    
    def minimumSizeHint(self) -> QSize:
        return self.sizeHint()
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        
        if not self._calculations:
            painter.setPen(QColor(200, 200, 200))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "No calculations to display")
            return
        
        label_text_color = QColor(255, 255, 255)
        data_text_color = QColor(255, 255, 255)
        header_text_color = QColor(150, 150, 150)
        
        font = QFont("Arial", 11)
        bold_font = QFont("Arial", 11)
        bold_font.setBold(True)
        
        num_cols = len(self._calculations)
        
        row_labels = [
            "",
            "Coordinates:",
            "Values:",
            "Kernel Adjusted Calculations:",
            "Kernel Adjusted Values:",
            "Bounded Values:"
        ]
        
        min_total_width = self._label_width + sum(self._cell_widths)
        available_width = self.width()
        extra_space = max(0, available_width - min_total_width)
        extra_per_cell = extra_space / num_cols if num_cols > 0 else 0
        
        actual_cell_widths = [w + extra_per_cell for w in self._cell_widths]
        
        for row_idx in range(self._row_count):
            y = row_idx * self._cell_height
            
            painter.setFont(bold_font)
            painter.setPen(QPen(label_text_color))
            painter.drawText(0, y, self._label_width - 10, self._cell_height,
                           Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                           row_labels[row_idx])
        
        x_offset = self._label_width
        for col_idx, calc in enumerate(self._calculations):
            cell_width = actual_cell_widths[col_idx]
            
            for row_idx in range(self._row_count):
                y = row_idx * self._cell_height
                
                painter.setFont(font)
                
                if row_idx == 0:
                    painter.setPen(QPen(header_text_color))
                else:
                    painter.setPen(QPen(data_text_color))
                
                if row_idx == 0:
                    text = str(calc['index'])
                elif row_idx == 1:
                    text = f"({calc['coordinate'][0]},{calc['coordinate'][1]})"
                elif row_idx == 2:
                    text = str(calc['input_value'])
                elif row_idx == 3:
                    text = f"({calc['input_value']}×{calc['final_kernel_value']:.2f})"
                elif row_idx == 4:
                    text = f"{calc['result']:.2f}"
                else:
                    text = f"{calc['bounded_result']:.2f}"
                
                painter.drawText(x_offset, y, cell_width, self._cell_height,
                               Qt.AlignmentFlag.AlignCenter, text)
            
            x_offset += cell_width
