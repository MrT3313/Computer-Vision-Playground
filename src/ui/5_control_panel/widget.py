from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QPushButton, QHBoxLayout
from PySide6.QtCore import Signal
from consts import DEFAULT_GRID_SIZE, MIN_GRID_SIZE, MAX_GRID_SIZE
from ui.common.number_input import NumberInputWidget


class ControlPanelWidget(QWidget):
    grid_size_changed = Signal(int)
    
    def __init__(self, coordinator=None):
        super().__init__()
        self._coordinator = coordinator
        self._setup_ui()
        
        if self._coordinator:
            self._coordinator.state_changed.connect(self._on_state_changed)
            self._coordinator.position_changed.connect(self._on_position_changed)
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        grid_group = QGroupBox("Grid Configuration")
        grid_layout = QVBoxLayout()
        
        self.grid_size_input = NumberInputWidget(
            label="Grid Size:",
            default_value=DEFAULT_GRID_SIZE,
            min_value=MIN_GRID_SIZE,
            max_value=MAX_GRID_SIZE
        )
        self.grid_size_input.value_changed.connect(self.grid_size_changed.emit)
        grid_layout.addWidget(self.grid_size_input)
        
        grid_group.setLayout(grid_layout)
        
        layout.addWidget(grid_group)
        
        nav_group = QGroupBox("Navigation")
        nav_layout = QVBoxLayout()
        
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self._on_start_clicked)
        nav_layout.addWidget(self.start_button)
        
        nav_buttons_layout = QHBoxLayout()
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self._on_reset_clicked)
        nav_buttons_layout.addWidget(self.reset_button)
        
        self.previous_button = QPushButton("Previous")
        self.previous_button.clicked.connect(self._on_previous_clicked)
        nav_buttons_layout.addWidget(self.previous_button)
        
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self._on_next_clicked)
        nav_buttons_layout.addWidget(self.next_button)
        
        nav_layout.addLayout(nav_buttons_layout)
        nav_group.setLayout(nav_layout)
        
        layout.addWidget(nav_group)
        
        self._update_button_visibility()
        
        layout.addStretch()
    
    def _on_start_clicked(self) -> None:
        if self._coordinator:
            self._coordinator.start()
    
    def _on_reset_clicked(self) -> None:
        if self._coordinator:
            self._coordinator.reset()
    
    def _on_previous_clicked(self) -> None:
        if self._coordinator:
            self._coordinator.previous()
    
    def _on_next_clicked(self) -> None:
        if self._coordinator:
            self._coordinator.next()
    
    def _on_state_changed(self, state) -> None:
        self._update_button_visibility()
        self._update_button_states()
    
    def _on_position_changed(self, row: int, col: int) -> None:
        self._update_button_states()
    
    def _update_button_visibility(self) -> None:
        if not self._coordinator:
            return
        
        from core import ApplicationState
        is_initial = self._coordinator.get_state() == ApplicationState.INITIAL
        
        self.start_button.setVisible(is_initial)
        self.reset_button.setVisible(not is_initial)
        self.previous_button.setVisible(not is_initial)
        self.next_button.setVisible(not is_initial)
    
    def _update_button_states(self) -> None:
        if not self._coordinator:
            return
        
        self.previous_button.setEnabled(self._coordinator.can_go_previous())
        self.next_button.setEnabled(self._coordinator.can_go_next())
