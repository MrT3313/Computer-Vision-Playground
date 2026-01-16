from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSpinBox, QDoubleSpinBox
from PySide6.QtCore import Signal


class NumberInputWidget(QWidget):
    value_changed = Signal(object)
    
    def __init__(
        self,
        label: str,
        default_value: int | float,
        min_value: int | float,
        max_value: int | float,
        step: float | None = None,
        decimals: int | None = None
    ):
        super().__init__()
        self._setup_ui(label, default_value, min_value, max_value, step, decimals)
    
    def _setup_ui(
        self,
        label: str,
        default_value: int | float,
        min_value: int | float,
        max_value: int | float,
        step: float | None,
        decimals: int | None
    ):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        layout.addWidget(QLabel(label))
        
        is_float = isinstance(default_value, float) or step is not None or decimals is not None
        
        if is_float:
            self.spinbox = QDoubleSpinBox()
            self.spinbox.setMinimum(float(min_value))
            self.spinbox.setMaximum(float(max_value))
            self.spinbox.setValue(float(default_value))
            if step is not None:
                self.spinbox.setSingleStep(step)
            if decimals is not None:
                self.spinbox.setDecimals(decimals)
        else:
            self.spinbox = QSpinBox()
            self.spinbox.setMinimum(int(min_value))
            self.spinbox.setMaximum(int(max_value))
            self.spinbox.setValue(int(default_value))
        
        self.spinbox.valueChanged.connect(self.value_changed.emit)
        layout.addWidget(self.spinbox)
    
    def value(self) -> int | float:
        return self.spinbox.value()
    
    def set_value(self, value: int | float) -> None:
        self.spinbox.setValue(value)
