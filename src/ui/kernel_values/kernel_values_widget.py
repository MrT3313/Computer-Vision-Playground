from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Signal

from src.core.kernel_config import KernelConfig
from src.ui.control_panel.kernel_grid_widget import KernelGridWidget


class KernelValuesWidget(QWidget):
    value_changed = Signal()
    
    def __init__(self, kernel_config: KernelConfig, parent=None):
        super().__init__(parent)
        self.kernel_config = kernel_config
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        layout.addStretch()
        
        self.kernel_grid = KernelGridWidget(self.kernel_config)
        self.kernel_grid.value_changed.connect(self.value_changed.emit)
        layout.addWidget(self.kernel_grid)
        
        layout.addStretch()
    
    def update_kernel_grid(self):
        self.kernel_grid.update_size()
        self.kernel_grid.update()
    
    def update_kernel_values_state(self, category: str, filter_selection: str):
        if category == "Linear" and filter_selection == "Custom":
            self.kernel_grid.setEnabled(True)
            self.label.setText("Kernel Values:")
            self.label.setStyleSheet("")
        else:
            self.kernel_grid.setEnabled(False)
            if filter_selection == "Mean":
                self.label.setText("Kernel Values: (auto-generated for Mean)")
            elif filter_selection == "Median":
                self.label.setText("Kernel Values: (not used for Median)")
            self.label.setStyleSheet("color: gray;")
