from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QWidget
from PySide6.QtCore import Qt
from ui.common import PixelGridWidget

class InputImageWidget(QFrame):
    def __init__(self, model, coordinator=None):
        super().__init__()
        self._model = model
        self._coordinator = coordinator
        self._pixel_grid = None
        self._setup_ui()
        
        if self._coordinator:
            self._coordinator.position_changed.connect(self._on_position_changed)
            self._coordinator.state_changed.connect(self._on_state_changed)
            self._update_initial_display()
    
    def _setup_ui(self):
        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(2)
        self.setMinimumSize(200, 200)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        title_bar = QFrame()
        title_bar.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border-bottom: 1px solid rgba(0, 0, 0, 0.3);")
        title_bar.setFixedHeight(30)
        
        title_layout = QVBoxLayout(title_bar)
        title_layout.setContentsMargins(5, 0, 5, 0)
        
        title_label = QLabel("1. Input Image")
        title_label.setStyleSheet("font-size: 12px; font-weight: bold; background: transparent; border: none;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        title_layout.addWidget(title_label)
        
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(10)
        
        self._pixel_grid = PixelGridWidget(self._model, editable=True)
        content_layout.addWidget(self._pixel_grid)
        
        main_layout.addWidget(title_bar)
        main_layout.addWidget(content_area, 1)
    
    def _on_position_changed(self, row: int, col: int) -> None:
        if self._coordinator and self._pixel_grid:
            affected_cells = self._coordinator.get_affected_cells()
            self._pixel_grid.set_highlighted_cells(affected_cells)
    
    def _on_state_changed(self, state) -> None:
        if self._pixel_grid:
            if state.value == "initial":
                if self._coordinator:
                    affected_cells = self._coordinator.get_affected_cells()
                    self._pixel_grid.set_highlighted_cells(affected_cells)
            else:
                pass
    
    def _update_initial_display(self) -> None:
        if self._coordinator and self._pixel_grid:
            affected_cells = self._coordinator.get_affected_cells()
            self._pixel_grid.set_highlighted_cells(affected_cells)
    
    def set_edit_mode(self, mode: str) -> None:
        if self._pixel_grid:
            self._pixel_grid.set_edit_mode(mode)