from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QWidget
from PySide6.QtCore import Qt
from ui.common import PixelGridWidget

class InputImageWidget(QFrame):
    def __init__(self, model, coordinator=None):
        super().__init__()
        # Store reference to the pixel grid data model
        self._model = model
        # Store reference to the application coordinator for position tracking
        self._coordinator = coordinator
        # Initialize pixel grid widget reference
        self._pixel_grid = None
        self._setup_ui()
        
        # Connect to coordinator signals if coordinator is provided
        if self._coordinator:
            # Update display when position changes during navigation
            self._coordinator.position_changed.connect(self._on_position_changed)
            # Update display when application state changes
            self._coordinator.state_changed.connect(self._on_state_changed)
            # Set initial highlighted cells based on starting position
            self._update_initial_display()
    
    def _setup_ui(self):
        # Configure the frame's visual appearance with a box border
        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(2) # Set border thickness to 2 pixels
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
        
        # Create the content area widget that will hold the pixel grid
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(10, 10, 10, 10) # Add 10px padding on all sides
        content_layout.setSpacing(10) # Add 10px spacing between widgets
        
        # Create the editable pixel grid widget for displaying and editing the input image
        self._pixel_grid = PixelGridWidget(self._model, editable=True)
        content_layout.addWidget(self._pixel_grid)
        
        # Add both the title bar and content area to the main layout
        main_layout.addWidget(title_bar) # Title bar at the top
        main_layout.addWidget(content_area, 1) # Content area below with stretch factor 1
    
    def _on_position_changed(self, row: int, col: int) -> None:
        # Update highlighted cells when the kernel position changes during navigation
        if self._coordinator and self._pixel_grid:
            # Get all cells affected by the kernel at the current position
            affected_cells = self._coordinator.get_affected_cells()
            # Highlight these cells in the pixel grid display
            self._pixel_grid.set_highlighted_cells(affected_cells)
    
    def _on_state_changed(self, state) -> None:
        # Update display when the application state changes
        if self._pixel_grid:
            # If returning to initial state, show the initial kernel position
            if state.value == "initial":
                if self._coordinator:
                    affected_cells = self._coordinator.get_affected_cells()
                    self._pixel_grid.set_highlighted_cells(affected_cells)
            else:
                # For other states, maintain current display
                pass
    
    def _update_initial_display(self) -> None:
        # Set the initial highlighted cells when the widget is first created
        if self._coordinator and self._pixel_grid:
            # Get cells affected by kernel at starting position
            affected_cells = self._coordinator.get_affected_cells()
            # Highlight these cells in the display
            self._pixel_grid.set_highlighted_cells(affected_cells)
    
    def set_edit_mode(self, mode: str) -> None:
        # Change the pixel grid editing mode (e.g., "paint", "erase", "select")
        if self._pixel_grid:
            self._pixel_grid.set_edit_mode(mode)
    
    def set_show_pixel_values(self, show: bool) -> None:
        # Show or hide the pixel values in the pixel grid
        if self._pixel_grid:
            self._pixel_grid.set_show_pixel_values(show)
    
    def set_show_colors(self, show: bool) -> None:
        # Show or hide the colors in the pixel grid
        if self._pixel_grid:
            self._pixel_grid.set_show_colors(show)