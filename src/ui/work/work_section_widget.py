from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QSizePolicy, QScrollArea
from PySide6.QtCore import Qt

from src.core.filter_calculator import ConvolutionResult, CrossCorrelationResult, MedianFilterResult


class WorkSectionWidget(QWidget):
    
    def __init__(self, parent=None, debug = False):
        super().__init__(parent)
        self.debug = debug
        self.grid_labels = []
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.content_widget = QWidget()
        self.content_widget.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        content_layout = QVBoxLayout(self.content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        content_layout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMinimumSize)
        
        self.grid_container = QWidget()
        self.grid_container.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setSpacing(2)
        self.grid_layout.setContentsMargins(10, 10, 10, 0)
        self.grid_layout.setSizeConstraint(QGridLayout.SizeConstraint.SetMinimumSize)
        content_layout.addWidget(self.grid_container)
        
        self.summary_label = QLabel("")
        self.summary_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.summary_label.setWordWrap(False)
        self.summary_label.setStyleSheet("padding: 10px 10px 0 10px; font-size: 12px;")
        content_layout.addWidget(self.summary_label)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.content_widget)
        self.scroll_area.setWidgetResizable(False)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        
        layout.addWidget(self.scroll_area)
        
        self.no_data_label = QLabel("No calculation to display")
        self.no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_data_label.setStyleSheet("padding: 20px; color: gray;")
        layout.addWidget(self.no_data_label)
        
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        
        if self.debug:
            self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
            self.setObjectName("WorkSectionContent")
            self.setStyleSheet("#WorkSectionContent { border: 2px solid red; background-color: transparent; }")
    
    def clear(self):
        self._clear_grid()
        self.summary_label.setText("")
        self.no_data_label.show()
        self.scroll_area.hide()
        self.scroll_area.setMinimumHeight(0)
        self.scroll_area.setMaximumHeight(16777215)
        self.summary_label.hide()
        self.updateGeometry()
    
    def _clear_grid(self):
        for label in self.grid_labels:
            label.deleteLater()
        self.grid_labels.clear()
        
        for col in range(100):
            self.grid_layout.setColumnMinimumWidth(col, 0)
            self.grid_layout.setColumnStretch(col, 0)
        
        self.grid_layout.invalidate()
    
    def _prepare_display(self):
        self._clear_grid()
        self.no_data_label.hide()
        self.scroll_area.show()
        self.summary_label.show()
        self._update_scroll_area_height()
    
    def _update_scroll_area_height(self):
        for col in range(self.grid_layout.columnCount()):
            self.grid_layout.setColumnMinimumWidth(col, 0)
            self.grid_layout.setColumnStretch(col, 0)
        
        self.grid_container.setMinimumSize(0, 0)
        self.grid_container.setMaximumSize(16777215, 16777215)
        self.content_widget.setMinimumSize(0, 0)
        self.content_widget.setMaximumSize(16777215, 16777215)
        
        self.grid_layout.invalidate()
        self.grid_layout.activate()
        
        self.grid_container.adjustSize()
        self.content_widget.adjustSize()
        
        grid_size = self.grid_container.size()
        self.grid_container.setFixedSize(grid_size)
        
        content_size = self.content_widget.size()
        self.content_widget.setFixedSize(content_size)
        
        self.scroll_area.setMinimumHeight(content_size.height() + 25)
        self.scroll_area.setMaximumHeight(content_size.height() + 25)
        self.updateGeometry()
    
    def _add_header_label(self, text: str, row: int):
        header = QLabel(text)
        header.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        header.setStyleSheet("font-weight: bold; padding-right: 10px;")
        self.grid_layout.addWidget(header, row, 0)
        self.grid_labels.append(header)
        return header
    
    def _add_data_column(self, idx: int, coord: tuple, value: int, extra_data: dict = None):
        index_label = QLabel(str(idx))
        index_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        index_label.setStyleSheet("font-weight: bold; padding: 5px 8px; color: #666;")
        self.grid_layout.addWidget(index_label, 0, idx + 1)
        self.grid_labels.append(index_label)
        
        coord_label = QLabel(f"({coord[0]},{coord[1]})")
        coord_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        coord_label.setStyleSheet("padding: 5px 8px;")
        self.grid_layout.addWidget(coord_label, 1, idx + 1)
        self.grid_labels.append(coord_label)
        
        value_label = QLabel(str(value))
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_label.setStyleSheet("padding: 5px 8px;")
        self.grid_layout.addWidget(value_label, 2, idx + 1)
        self.grid_labels.append(value_label)
        
        if extra_data:
            for row_num, data_value in extra_data.items():
                data_label = QLabel(data_value)
                data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                data_label.setStyleSheet("padding: 5px 8px;")
                self.grid_layout.addWidget(data_label, row_num, idx + 1)
                self.grid_labels.append(data_label)
    
    def update_convolution_calculation(self, result: ConvolutionResult):
        if result is None:
            self.clear()
            return
        
        self._prepare_display()
        
        self._add_header_label("Coordinates:", 1)
        self._add_header_label("Values:", 2)
        self._add_header_label("Kernel Adjusted Calculations:", 3)
        self._add_header_label("Kernel Adjusted Values:", 4)
        
        flattened_kernel = [val for row in result.flipped_kernel for val in row]
        is_mean = all(k == 1.0 for k in flattened_kernel)
        constant = result.constant
        adjusted_values = [v * k * constant for v, k in zip(result.values, flattened_kernel)]
        calculations = [f"({v}×{k:.2f})×{constant:.2f}" for v, k in zip(result.values, flattened_kernel)]
        
        if is_mean:
            for idx, (coord, value, calc, adj_val) in enumerate(zip(result.coordinates, result.values, calculations, adjusted_values)):
                self._add_data_column(idx, coord, value, {3: calc, 4: f"{adj_val:.2f}"})
            self._set_mean_filter_summary_with_adjusted(adjusted_values, len(result.values), result.result)
        else:
            self._add_header_label("Kernel (flipped):", 5)
            for idx, (coord, value, calc, adj_val, kernel_val) in enumerate(zip(result.coordinates, result.values, calculations, adjusted_values, flattened_kernel)):
                self._add_data_column(idx, coord, value, {3: calc, 4: f"{adj_val:.2f}", 5: f"{kernel_val:.2f}"})
            self._set_linear_filter_summary(result.values, flattened_kernel, result.result, "Convolution")
        
        self._update_scroll_area_height()
    
    def update_cross_correlation_calculation(self, result: CrossCorrelationResult):
        if result is None:
            self.clear()
            return
        
        self._prepare_display()
        
        self._add_header_label("Coordinates:", 1)
        self._add_header_label("Values:", 2)
        self._add_header_label("Kernel Adjusted Calculations:", 3)
        self._add_header_label("Kernel Adjusted Values:", 4)
        
        flattened_kernel = [val for row in result.kernel_values for val in row]
        is_mean = all(k == 1.0 for k in flattened_kernel)
        constant = result.constant
        adjusted_values = [v * k * constant for v, k in zip(result.values, flattened_kernel)]
        calculations = [f"({v}×{k:.2f})×{constant:.2f}" for v, k in zip(result.values, flattened_kernel)]
        
        if is_mean:
            for idx, (coord, value, calc, adj_val) in enumerate(zip(result.coordinates, result.values, calculations, adjusted_values)):
                self._add_data_column(idx, coord, value, {3: calc, 4: f"{adj_val:.2f}"})
            self._set_mean_filter_summary_with_adjusted(adjusted_values, len(result.values), result.result)
        else:
            self._add_header_label("Kernel:", 5)
            for idx, (coord, value, calc, adj_val, kernel_val) in enumerate(zip(result.coordinates, result.values, calculations, adjusted_values, flattened_kernel)):
                self._add_data_column(idx, coord, value, {3: calc, 4: f"{adj_val:.2f}", 5: f"{kernel_val:.2f}"})
            self._set_linear_filter_summary(result.values, flattened_kernel, result.result, "Cross-Correlation")
        
        self._update_scroll_area_height()
    
    def update_median_calculation(self, result: MedianFilterResult):
        if result is None:
            self.clear()
            return
        
        self._prepare_display()
        
        self._add_header_label("Coordinates:", 1)
        self._add_header_label("Values:", 2)
        self._add_header_label("Kernel Adjusted Calculations:", 3)
        self._add_header_label("Kernel Adjusted Values:", 4)
        
        constant = result.constant
        adjusted_values = [constant if v == result.median else 0.0 for v in result.values]
        calculations = [f"{v}×{constant:.2f}" if v == result.median else "0" for v in result.values]
        
        for idx, (coord, value, calc, adj_val) in enumerate(zip(result.coordinates, result.values, calculations, adjusted_values)):
            self._add_data_column(idx, coord, value, {3: calc, 4: f"{adj_val:.2f}"})
        
        sorted_str = ", ".join([str(v) for v in result.sorted_values])
        median_idx = len(result.sorted_values) // 2
        
        summary_text = f"""<div style='line-height: 1.8;'>
<b>Median Filter:</b><br/>
<b>Sorted values:</b> [{sorted_str}]<br/>
<b>Median:</b> values[{median_idx}] = {result.median:.2f}<br/>
<b>Result:</b> {result.median:.2f} × {constant:.2f} = {result.result:.2f}
</div>"""
        
        self.summary_label.setText(summary_text)
        self._update_scroll_area_height()
    
    def _set_mean_filter_summary_with_adjusted(self, adjusted_values: list, count: int, final_result: float):
        adjusted_str = " + ".join([f"{v:.2f}" for v in adjusted_values])
        total = sum(adjusted_values)
        mean = total / count
        
        summary_text = f"""<div style='line-height: 1.8;'>
<b>Sum:</b> {adjusted_str} = {total:.2f}<br/>
<b>Mean:</b> {total:.2f} / {count} = {mean:.2f}<br/>
<b>Result:</b> {mean:.2f}
</div>"""
        
        self.summary_label.setText(summary_text)
    
    def _set_linear_filter_summary(self, values: list, kernel: list, final_result: float, operation_name: str):
        constant = final_result / sum([v * k for v, k in zip(values, kernel)]) if sum([v * k for v, k in zip(values, kernel)]) != 0 else 1.0
        adjusted_values = [v * k * constant for v, k in zip(values, kernel)]
        adjusted_str = " + ".join([f"{av:.2f}" for av in adjusted_values])
        result_sum = sum(adjusted_values)
        
        summary_text = f"""<div style='line-height: 1.8;'>
<b>Sum:</b> {adjusted_str} = {result_sum:.2f}<br/>
<b>Result:</b> {result_sum:.2f}
</div>"""
        
        self.summary_label.setText(summary_text)
