from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QPushButton, QFileDialog, QMessageBox
from PySide6.QtCore import Qt, Signal
from ui.common import PixelGridWidget
from core.grid_image_processor import GridImageProcessor
from consts import MIN_GRID_SIZE, MAX_GRID_SIZE

class InputImageWidget(QFrame):
    grid_size_detected = Signal(int)
    
    def __init__(self, model, coordinator=None, control_panel=None):
        super().__init__()
        # Store reference to the pixel grid data model
        self._model = model
        # Store reference to the application coordinator for position tracking
        self._coordinator = coordinator
        # Store reference to control panel for direct updates
        self._control_panel = control_panel
        # Initialize pixel grid widget reference
        self._pixel_grid = None
        # Initialize image processor
        self._processor = GridImageProcessor()
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
        
        # Create horizontal layout for the title bar to hold the title label and upload button
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(5, 0, 5, 0) # Add 5px padding on left and right
        title_layout.setSpacing(5) # Add 5px spacing between widgets
        
        # Create the title label
        title_label = QLabel("1. Input Image: F(i,j)")
        title_label.setStyleSheet("font-size: 12px; font-weight: bold; background: transparent; border: none;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter) # Align text to the left and vertically centered
        
        # Add the title label to the title bar layout
        title_layout.addWidget(title_label)
        
        # Add stretch to push button to the right
        title_layout.addStretch()
        
        # Create the upload image button
        upload_button = QPushButton("Upload Image Grid")
        upload_button.setStyleSheet("font-size: 11px; padding: 2px 8px;")
        upload_button.clicked.connect(self._on_upload_clicked)
        title_layout.addWidget(upload_button)
        
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
    
    def _on_upload_clicked(self) -> None:
        # Handle the upload button click event to load a grid image
        
        # Open file dialog to let user select an image file
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Grid Image",  # Dialog title
            "",  # Starting directory (empty = default)
            "Image Files (*.png *.jpg *.jpeg *.bmp *.tiff)"  # File type filter
        )
        
        # Early return if user cancelled the dialog
        if not file_path:
            return
        
        # Process the selected image using the GridImageProcessor
        success, result, message = self._processor.process_image(file_path)
        
        # Show error if processing failed
        if not success:
            self.show_error(f"Unable to process image: {message}")
            return
        
        # Show error if result is None (should not happen if success is True, but checking for safety)
        if result is None:
            self.show_error(f"Unable to process image: {message}")
            return
        
        # Unpack the result tuple (grid size and grid data)
        grid_size, grid_data = result
        
        # Validate that detected grid size is within allowed range
        if grid_size < MIN_GRID_SIZE or grid_size > MAX_GRID_SIZE:
            self.show_error(f"Grid size {grid_size}x{grid_size} is outside valid range ({MIN_GRID_SIZE}-{MAX_GRID_SIZE})")
            return
        
        # Update the model with the detected grid size
        self._model.set_grid_size(grid_size)
        
        # Update the control panel grid size input to match detected size
        if self._control_panel:
            # Block signals to prevent triggering grid_size_changed signal while updating
            self._control_panel.grid_size_input.spinbox.blockSignals(True)
            try:
                # Set the spinbox value to the detected grid size
                self._control_panel.grid_size_input.set_value(grid_size)
            finally:
                # Always restore signal handling, even if an error occurs
                self._control_panel.grid_size_input.spinbox.blockSignals(False)
        
        # Emit signal to notify other components of the detected grid size
        self.grid_size_detected.emit(grid_size)
        
        # Populate the grid with extracted cell values
        for row_idx, row_data in enumerate(grid_data):
            for col_idx, cell_value in enumerate(row_data):
                # Set each cell value in the model
                self._model.set_cell(row_idx, col_idx, cell_value)
        
        # Show success message if there's any message to display
        if message:
            self._show_message("Success", message, QMessageBox.Icon.Information)
    
    def _show_message(self, title: str, message: str, icon: QMessageBox.Icon) -> None:
        # Display a message dialog with custom title, message, and icon
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)  # Set dialog title
        msg_box.setText(message)  # Set message text
        msg_box.setIcon(icon)  # Set icon (Information, Warning, Error, etc.)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)  # Add OK button
        msg_box.exec()  # Show dialog modally (blocks until user closes it)
    
    def show_error(self, message: str) -> None:
        # Convenience method to show an error dialog
        self._show_message("Error", message, QMessageBox.Icon.Warning)