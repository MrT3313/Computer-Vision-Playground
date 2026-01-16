from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
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
        # Configure the frame's visual appearance with a box border
        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(2) # Set border thickness to 2 pixels
        self.setStyleSheet("background-color: grey;") # Set background color
        self.setMinimumSize(200, 200) # Ensure minimum size of 200x200 pixels
        
        # Create the main vertical layout that will contain all child widgets
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0) # Remove padding around edges
        main_layout.setSpacing(0) # Remove spacing between child widgets
        
        # Create the title bar frame at the top of the panel
        title_bar = QFrame()
        title_bar.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border-bottom: 1px solid rgba(0, 0, 0, 0.3);")
        title_bar.setFixedHeight(30) # Fixed height of 30 pixels for title bar
        
        # Create layout for the title bar to hold the title label
        title_layout = QVBoxLayout(title_bar)
        title_layout.setContentsMargins(5, 0, 5, 0) # Add 5px padding on left and right
        
        # Create the title label
        title_label = QLabel("1. Input Image")
        title_label.setStyleSheet("font-size: 12px; font-weight: bold; background: transparent; border: none;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter) # Align text to the left and vertically centered
        
        # Add the title label to the title bar layout
        title_layout.addWidget(title_label)
        
        self._pixel_grid = PixelGridWidget(self._model)
        
        main_layout.addWidget(title_bar)
        main_layout.addWidget(self._pixel_grid, 1)
    
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
