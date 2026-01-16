from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox
from PySide6.QtCore import Signal


class DropdownWidget(QWidget):
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
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        layout.addWidget(QLabel(label))
        
        self.combobox = QComboBox()
        self.combobox.addItems(options)
        
        if default_option and default_option in options:
            self.combobox.setCurrentText(default_option)
        
        self.combobox.currentTextChanged.connect(self.value_changed.emit)
        layout.addWidget(self.combobox)
    
    def value(self) -> str:
        return self.combobox.currentText()
    
    def set_value(self, value: str) -> None:
        self.combobox.setCurrentText(value)
