from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSpinBox, QDoubleSpinBox
from PySide6.QtCore import Signal


class NumberInputWidget(QWidget):
    # Signal emitted when the spinbox value changes, passes the new value (int or float)
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
        # Create horizontal layout for label and spinbox
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0) # Remove padding around edges
        
        # Add label to identify the input field
        layout.addWidget(QLabel(label))
        
        # Determine whether to use integer or floating-point spinbox
        # Use float spinbox if default value is float, or if step/decimals are specified
        is_float = isinstance(default_value, float) or step is not None or decimals is not None
        
        if is_float:
            # Create double spinbox for floating-point values
            self.spinbox = QDoubleSpinBox()
            self.spinbox.setMinimum(float(min_value)) # Set minimum allowed value
            self.spinbox.setMaximum(float(max_value)) # Set maximum allowed value
            self.spinbox.setValue(float(default_value)) # Set initial default value
            if step is not None:
                self.spinbox.setSingleStep(step) # Set increment/decrement step size
            if decimals is not None:
                self.spinbox.setDecimals(decimals) # Set number of decimal places to display
        else:
            # Create integer spinbox for whole number values
            self.spinbox = QSpinBox()
            self.spinbox.setMinimum(int(min_value)) # Set minimum allowed value
            self.spinbox.setMaximum(int(max_value)) # Set maximum allowed value
            self.spinbox.setValue(int(default_value)) # Set initial default value
        
        # Connect spinbox value changes to emit the value_changed signal
        self.spinbox.valueChanged.connect(self.value_changed.emit)
        # Add spinbox to the layout
        layout.addWidget(self.spinbox)
    
    def value(self) -> int | float:
        # Return the current value of the spinbox
        return self.spinbox.value()
    
    def set_value(self, value: int | float) -> None:
        # Set a new value for the spinbox
        self.spinbox.setValue(value)