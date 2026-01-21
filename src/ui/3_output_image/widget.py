from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from ui.common import PixelGridWidget, TitleBarWidget

class OutputImageWidget(QFrame):
    def __init__(self, model, coordinator=None):
        super().__init__()
        # Store reference to the output pixel grid data model
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
            # Set initial bordered cell based on starting position
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
        
        title_bar = TitleBarWidget("3. Output Image: G(i,j)")
        
        # Create the content area widget that will hold the pixel grid
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(10, 10, 10, 10) # Add 10px padding on all sides
        content_layout.setSpacing(10) # Add 10px spacing between widgets
        
        # Create the read-only pixel grid widget for displaying the output image
        self._pixel_grid = PixelGridWidget(self._model, editable=False)
        content_layout.addWidget(self._pixel_grid)
        
        # Add both the title bar and content area to the main layout
        main_layout.addWidget(title_bar) # Title bar at the top
        main_layout.addWidget(content_area, 1) # Content area below with stretch factor 1
    
    def _on_position_changed(self, row: int, col: int) -> None:
        # Update bordered cell when the kernel position changes during navigation
        if self._coordinator and self._pixel_grid:
            # Get the current output cell (center of kernel) position
            output_cell = self._coordinator.get_output_cell()
            # Draw a border around this cell to show where output is being written
            self._pixel_grid.set_bordered_cell(output_cell)
    
    def _on_state_changed(self, state) -> None:
        # Update display when the application state changes
        if self._pixel_grid:
            # If returning to initial state, clear the output grid and show the initial output position
            if state.value == "initial":
                self._model.clear_grid()
                if self._coordinator:
                    output_cell = self._coordinator.get_output_cell()
                    self._pixel_grid.set_bordered_cell(output_cell)
            else:
                # For other states, maintain current display
                pass
    
    def _update_initial_display(self) -> None:
        # Set the initial bordered cell when the widget is first created
        if self._coordinator and self._pixel_grid:
            # Get the starting output cell position
            output_cell = self._coordinator.get_output_cell()
            # Draw a border around this cell in the display
            self._pixel_grid.set_bordered_cell(output_cell)
    
    def set_show_pixel_values(self, show: bool) -> None:
        # Show or hide the pixel values in the pixel grid
        if self._pixel_grid:
            self._pixel_grid.set_show_pixel_values(show)
    
    def set_show_colors(self, show: bool) -> None:
        # Show or hide the colors in the pixel grid
        if self._pixel_grid:
            self._pixel_grid.set_show_colors(show)