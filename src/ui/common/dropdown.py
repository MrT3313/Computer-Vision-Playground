from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox
from PySide6.QtCore import Signal


class DropdownWidget(QWidget):
    # Signal emitted when the selected dropdown option changes, passes the new option as a string
    value_changed = Signal(str)
    
    def __init__(
        self,
        label: str,
        options: list[str],
        default_option: str | None = None
    ):
        super().__init__()
        self._setup_ui(label, options, default_option)
    
    def _setup_ui(
        self,
        label: str,
        options: list[str],
        default_option: str | None
    ):
        # Create horizontal layout for label and dropdown
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0) # Remove padding around edges
        
        # Add label to identify the dropdown
        layout.addWidget(QLabel(label))
        
        # Create combobox (dropdown) widget
        self.combobox = QComboBox()
        # Add all available options to the dropdown
        self.combobox.addItems(options)
        
        # Set the default selected option if provided and valid
        if default_option and default_option in options:
            self.combobox.setCurrentText(default_option)
        
        # Emit signal when the selected option changes
        self.combobox.currentTextChanged.connect(self.value_changed.emit)
        # Add combobox to the layout
        layout.addWidget(self.combobox)
    
    def value(self) -> str:
        # Return the currently selected option text
        return self.combobox.currentText()
    
    def set_value(self, value: str) -> None:
        # Set the currently selected option to the specified value
        self.combobox.setCurrentText(value)