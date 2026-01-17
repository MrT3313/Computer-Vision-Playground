from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QPushButton, QHBoxLayout, QCheckBox
from PySide6.QtCore import Signal
from consts import DEFAULT_GRID_SIZE, MIN_GRID_SIZE, MAX_GRID_SIZE
from ui.common.number_input import NumberInputWidget
from ui.common.dropdown import DropdownWidget


class ControlPanelWidget(QWidget):
    # Signal emitted when the grid size value changes, passes the new grid size as an integer
    grid_size_changed = Signal(int)
    # Signal emitted when the input mode changes, passes the mode as a string
    input_mode_changed = Signal(str)
    # Signal emitted when the show pixel values checkbox state changes, passes the new state as a boolean
    show_pixel_values_changed = Signal(bool)
    # Signal emitted when the show colors checkbox state changes, passes the new state as a boolean
    show_colors_changed = Signal(bool)
    # Signal emitted when the filter category changes, passes the category as a string
    category_changed = Signal(str)
    # Signal emitted when the filter type changes, passes the type as a string
    type_changed = Signal(str)
    # Signal emitted when the filter selection changes, passes the filter as a string
    filter_changed = Signal(str)
    
    def __init__(self, coordinator=None):
        super().__init__()
        # Store reference to the application coordinator for navigation control
        self._coordinator = coordinator
        self._setup_ui()
        
        # Connect to coordinator signals if coordinator is provided
        if self._coordinator:
            # Update button visibility when application state changes
            self._coordinator.state_changed.connect(self._on_state_changed)
            # Update button enabled/disabled states when position changes
            self._coordinator.position_changed.connect(self._on_position_changed)
    
    def _setup_ui(self):
        # Create the main vertical layout for the control panel
        layout = QVBoxLayout(self)
        
        # Create group box for grid configuration controls
        grid_group = QGroupBox("Grid Configuration")
        grid_layout = QVBoxLayout()
        
        # Create number input widget for grid size control
        self.grid_size_input = NumberInputWidget(
            label="Grid Size:",
            default_value=DEFAULT_GRID_SIZE,
            min_value=MIN_GRID_SIZE,
            max_value=MAX_GRID_SIZE
        )
        # Emit signal when grid size value changes
        self.grid_size_input.value_changed.connect(self.grid_size_changed.emit)
        grid_layout.addWidget(self.grid_size_input)
        
        # Create checkbox for showing pixel values
        self.show_pixel_values_checkbox = QCheckBox("Show Pixel Values")
        self.show_pixel_values_checkbox.setChecked(True)
        self.show_pixel_values_checkbox.stateChanged.connect(self._on_show_pixel_values_changed)
        grid_layout.addWidget(self.show_pixel_values_checkbox)
        
        # Create checkbox for showing colors
        self.show_colors_checkbox = QCheckBox("Show Colors")
        self.show_colors_checkbox.setChecked(True)
        self.show_colors_checkbox.stateChanged.connect(self._on_show_colors_changed)
        grid_layout.addWidget(self.show_colors_checkbox)
        
        # Set the layout for the grid configuration group box
        grid_group.setLayout(grid_layout)
        
        # Add the grid configuration group to the main layout
        layout.addWidget(grid_group)
        
        # Create group box for input image configuration controls
        input_image_group = QGroupBox("Input Image Configuration")
        input_image_layout = QVBoxLayout()
        
        # Create dropdown widget for selecting input mode (Toggle or Custom)
        self.input_mode_dropdown = DropdownWidget(
            label="Mode:",
            options=["Toggle", "Custom"],
            default_option="Toggle"
        )
        # Emit signal when input mode selection changes
        self.input_mode_dropdown.value_changed.connect(self.input_mode_changed.emit)
        input_image_layout.addWidget(self.input_mode_dropdown)
        
        # Set the layout for the input image configuration group box
        input_image_group.setLayout(input_image_layout)
        
        # Add the input image configuration group to the main layout
        layout.addWidget(input_image_group)
        
        # Create group box for filter configuration controls
        filter_group = QGroupBox("Filter Configuration")
        filter_layout = QVBoxLayout()
        
        # Create dropdown widget for selecting filter category
        self.category_dropdown = DropdownWidget(
            label="Category:",
            options=["Linear", "Non-Linear"],
            default_option="Linear"
        )
        self.category_dropdown.value_changed.connect(self._on_category_changed)
        filter_layout.addWidget(self.category_dropdown)
        
        # Create dropdown widget for selecting filter type
        self.type_dropdown = DropdownWidget(
            label="Type:",
            options=["Cross-Correlation", "Convolution"],
            default_option="Cross-Correlation"
        )
        self.type_dropdown.value_changed.connect(self._on_type_changed)
        filter_layout.addWidget(self.type_dropdown)
        
        # Create dropdown widget for selecting specific filter
        self.filter_dropdown = DropdownWidget(
            label="Filter Selection:",
            options=["Mean", "Custom"],
            default_option="Mean"
        )
        self.filter_dropdown.value_changed.connect(self._on_filter_changed)
        filter_layout.addWidget(self.filter_dropdown)
        
        # Set the layout for the filter configuration group box
        filter_group.setLayout(filter_layout)
        
        # Add the filter configuration group to the main layout
        layout.addWidget(filter_group)
        
        # Create group box for navigation controls
        nav_group = QGroupBox("Navigation")
        nav_layout = QVBoxLayout()
        
        # Create Start button to begin navigation
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self._on_start_clicked)
        nav_layout.addWidget(self.start_button)
        
        # Create horizontal layout for Reset, Previous, and Next buttons
        nav_buttons_layout = QHBoxLayout()
        
        # Create Reset button to return to initial state
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self._on_reset_clicked)
        nav_buttons_layout.addWidget(self.reset_button)
        
        # Create Previous button to navigate backwards
        self.previous_button = QPushButton("Previous")
        self.previous_button.clicked.connect(self._on_previous_clicked)
        nav_buttons_layout.addWidget(self.previous_button)
        
        # Create Next button to navigate forwards
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self._on_next_clicked)
        nav_buttons_layout.addWidget(self.next_button)
        
        # Add the navigation buttons layout to the navigation group layout
        nav_layout.addLayout(nav_buttons_layout)
        nav_group.setLayout(nav_layout)
        
        # Add the navigation group to the main layout
        layout.addWidget(nav_group)
        
        # Set initial button visibility based on application state
        self._update_button_visibility()
        
        # Set initial Type dropdown state based on default filter selection (Mean)
        self.type_dropdown.combobox.setEnabled(False)
        
        # Add stretchable space at the bottom to push controls to the top
        layout.addStretch()
    
    def _on_start_clicked(self) -> None:
        # Start navigation when Start button is clicked
        if self._coordinator:
            self._coordinator.start()
    
    def _on_reset_clicked(self) -> None:
        # Reset to initial state when Reset button is clicked
        if self._coordinator:
            self._coordinator.reset()
    
    def _on_previous_clicked(self) -> None:
        # Navigate to previous position when Previous button is clicked
        if self._coordinator:
            self._coordinator.previous()
    
    def _on_next_clicked(self) -> None:
        # Navigate to next position when Next button is clicked
        if self._coordinator:
            self._coordinator.next()
    
    def _on_show_pixel_values_changed(self, state: int) -> None:
        # Show or hide the pixel values in the pixel grid
        is_checked = state == 2
        if not is_checked and not self.show_colors_checkbox.isChecked():
            self.show_colors_checkbox.setChecked(True)
        self.show_pixel_values_changed.emit(is_checked)
    
    def _on_show_colors_changed(self, state: int) -> None:
        # Show or hide the colors in the pixel grid
        is_checked = state == 2
        if not is_checked and not self.show_pixel_values_checkbox.isChecked():
            self.show_pixel_values_checkbox.setChecked(True)
        self.show_colors_changed.emit(is_checked)
    
    def _on_category_changed(self, category: str) -> None:
        self.category_changed.emit(category)
        
        if category == "Non-Linear":
            self.type_dropdown.combobox.setEnabled(False)
            self.filter_dropdown.combobox.clear()
            self.filter_dropdown.combobox.addItems(["Median"])
            self.filter_dropdown.combobox.setCurrentText("Median")
        else:
            self.type_dropdown.combobox.setEnabled(True)
            self.filter_dropdown.combobox.clear()
            self.filter_dropdown.combobox.addItems(["Mean", "Custom"])
            self.filter_dropdown.combobox.setCurrentText("Mean")
    
    def _on_type_changed(self, type_value: str) -> None:
        self.type_changed.emit(type_value)
    
    def _on_filter_changed(self, filter_value: str) -> None:
        self.filter_changed.emit(filter_value)
        
        current_category = self.category_dropdown.combobox.currentText()
        
        if current_category == "Non-Linear":
            self.type_dropdown.combobox.setEnabled(False)
        elif filter_value == "Mean":
            self.type_dropdown.combobox.setEnabled(False)
        else:
            self.type_dropdown.combobox.setEnabled(True)
    
    def _on_state_changed(self, state) -> None:
        # Update UI when application state changes
        self._update_button_visibility()  # Show/hide buttons based on state
        self._update_button_states()  # Enable/disable buttons based on navigation availability
    
    def _on_position_changed(self, row: int, col: int) -> None:
        # Update button enabled/disabled states when position changes during navigation
        self._update_button_states()
    
    def _update_button_visibility(self) -> None:
        # Show/hide navigation buttons based on current application state
        if not self._coordinator:
            return
        
        from core import ApplicationState
        # Check if currently in INITIAL state
        is_initial = self._coordinator.get_state() == ApplicationState.INITIAL
        
        # In INITIAL state: show Start button, hide navigation buttons
        # In NAVIGATING state: hide Start button, show navigation buttons
        self.start_button.setVisible(is_initial)
        self.reset_button.setVisible(not is_initial)
        self.previous_button.setVisible(not is_initial)
        self.next_button.setVisible(not is_initial)
    
    def _update_button_states(self) -> None:
        # Enable/disable Previous and Next buttons based on navigation boundaries
        if not self._coordinator:
            return
        
        # Disable Previous button if at the start position
        self.previous_button.setEnabled(self._coordinator.can_go_previous())
        # Disable Next button if at the end position
        self.next_button.setEnabled(self._coordinator.can_go_next())
