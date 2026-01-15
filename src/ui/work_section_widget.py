from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QScrollArea, QFrame
from PySide6.QtCore import Qt

from src.core.filter_calculator import MeanFilterResult


class WorkSectionWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_filter = "Mean"
        self.grid_labels = []
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # self.title_label = QLabel("Mean Filter Calculation")
        # self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.title_label.setStyleSheet("font-weight: bold; font-size: 14px; padding: 0px 0px 0px 0px;")
        # self.content_layout.addWidget(self.title_label)
        
        self.grid_container = QWidget()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setSpacing(2)
        self.grid_layout.setContentsMargins(10, 10, 10, 0)
        self.content_layout.addWidget(self.grid_container)
        
        self.summary_label = QLabel("")
        self.summary_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.summary_label.setWordWrap(True)
        self.summary_label.setStyleSheet("padding: 10px 10px 10px 10px; font-size: 12px;")
        self.content_layout.addWidget(self.summary_label)
        
        self.no_data_label = QLabel("No calculation to display")
        self.no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_data_label.setStyleSheet("padding: 20px; color: gray;")
        self.content_layout.addWidget(self.no_data_label)
        
        scroll_area.setWidget(self.content_widget)
        layout.addWidget(scroll_area)
    
    def set_filter_type(self, filter_type: str):
        self.current_filter = filter_type
    
    def clear(self):
        self._clear_grid()
        self.summary_label.setText("")
        self.no_data_label.show()
        self.grid_container.hide()
        self.summary_label.hide()
    
    def _clear_grid(self):
        for label in self.grid_labels:
            label.deleteLater()
        self.grid_labels.clear()
    
    def update_mean_calculation(self, result: MeanFilterResult):
        if result is None:
            self.clear()
            return
        
        self._clear_grid()
        
        self.no_data_label.hide()
        self.grid_container.show()
        self.summary_label.show()
        
        coord_header = QLabel("Coordinates:")
        coord_header.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        coord_header.setStyleSheet("font-weight: bold; padding-right: 10px;")
        self.grid_layout.addWidget(coord_header, 1, 0)
        self.grid_labels.append(coord_header)
        
        value_header = QLabel("Values:")
        value_header.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        value_header.setStyleSheet("font-weight: bold; padding-right: 10px;")
        self.grid_layout.addWidget(value_header, 2, 0)
        self.grid_labels.append(value_header)
        
        for idx, (coord, value) in enumerate(zip(result.coordinates, result.values)):
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
        
        self._update_summary(result)
    
    def _update_summary(self, result: MeanFilterResult):
        values_sum_str = " + ".join([str(v) for v in result.values])
        
        summary_text = f"""<div style='line-height: 1.8;'>
<b>Sum:</b> {values_sum_str} = {result.total}<br/>
<b>Mean:</b> {result.total} / {len(result.values)} = {result.mean:.2f}<br/>
</div>"""
        
        self.summary_label.setText(summary_text)
