from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QPushButton, QHBoxLayout, QCheckBox, QGridLayout, QFrame
from PySide6.QtCore import Signal
from .playback_controller import PlaybackController
from consts import (
    DEFAULT_GRID_SIZE, MIN_GRID_SIZE, MAX_GRID_SIZE,
    DEFAULT_INPUT_MODE, INPUT_MODES,
    DEFAULT_FILTER_PROFILE, FILTER_PROFILES,
    DEFAULT_FILTER_CATEGORY, FILTER_CATEGORIES,
    DEFAULT_FILTER_TYPE, FILTER_TYPES,
    DEFAULT_FILTER_SELECTION, FILTER_SELECTIONS_LINEAR, FILTER_SELECTIONS_NONLINEAR,
    DEFAULT_NONLINEAR_FILTER,
    PROFILE_FILTER_TYPE, PROFILE_FILTER_SELECTION,
    DEFAULT_SIGMA, MIN_SIGMA, MAX_SIGMA, SIGMA_STEP, SIGMA_DECIMALS
)
from ui.common.number_input import NumberInputWidget
from ui.common.dropdown import DropdownWidget
from ui.common.title_bar_widget import TitleBarWidget


class ControlPanelWidget(QFrame):
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
    # Signal emitted when the filter profile changes, passes the profile as a string
    profile_changed = Signal(str)
    # Signal emitted when the sigma value changes, passes the sigma as a float
    sigma_changed = Signal(float)
    # Signal emitted when the normalize checkbox state changes, passes the new state as a boolean
    normalize_changed = Signal(bool)
    
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
        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(2)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        title_bar = TitleBarWidget("5. Control Panel")
        layout.addWidget(title_bar)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(10)
        
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
        
        self.show_pixel_values_checkbox = QCheckBox("Show Pixel Values")
        self.show_pixel_values_checkbox.setChecked(True)
        self.show_pixel_values_checkbox.stateChanged.connect(self._on_show_pixel_values_changed)
        grid_layout.addWidget(self.show_pixel_values_checkbox)
        
        self.show_colors_checkbox = QCheckBox("Show Colors")
        self.show_colors_checkbox.setChecked(True)
        self.show_colors_checkbox.stateChanged.connect(self._on_show_colors_changed)
        grid_layout.addWidget(self.show_colors_checkbox)
        
        grid_group.setLayout(grid_layout)
        content_layout.addWidget(grid_group)
        
        input_image_group = QGroupBox("Input Image Configuration")
        input_image_layout = QVBoxLayout()
        
        self.input_mode_dropdown = DropdownWidget(
            label="Mode:",
            options=INPUT_MODES,
            default_option=DEFAULT_INPUT_MODE
        )
        self.input_mode_dropdown.value_changed.connect(self.input_mode_changed.emit)
        input_image_layout.addWidget(self.input_mode_dropdown)
        
        input_image_group.setLayout(input_image_layout)
        content_layout.addWidget(input_image_group)
        
        filter_group = QGroupBox("Filter Configuration")
        filter_layout = QVBoxLayout()
        
        self.profile_dropdown = DropdownWidget(
            label="Filter Profile:",
            options=FILTER_PROFILES,
            default_option=DEFAULT_FILTER_PROFILE
        )
        self.profile_dropdown.value_changed.connect(self._on_profile_changed)
        filter_layout.addWidget(self.profile_dropdown)
        
        self.category_dropdown = DropdownWidget(
            label="Category:",
            options=FILTER_CATEGORIES,
            default_option=DEFAULT_FILTER_CATEGORY
        )
        self.category_dropdown.value_changed.connect(self._on_category_changed)
        filter_layout.addWidget(self.category_dropdown)
        
        self.type_dropdown = DropdownWidget(
            label="Type:",
            options=FILTER_TYPES,
            default_option=DEFAULT_FILTER_TYPE
        )
        self.type_dropdown.value_changed.connect(self._on_type_changed)
        filter_layout.addWidget(self.type_dropdown)
        
        self.filter_dropdown = DropdownWidget(
            label="Filter Selection:",
            options=FILTER_SELECTIONS_LINEAR,
            default_option=DEFAULT_FILTER_SELECTION
        )
        self.filter_dropdown.value_changed.connect(self._on_filter_changed)
        filter_layout.addWidget(self.filter_dropdown)
        
        self.sigma_input = NumberInputWidget(
            label="Sigma (σ):",
            default_value=DEFAULT_SIGMA,
            min_value=MIN_SIGMA,
            max_value=MAX_SIGMA,
            step=SIGMA_STEP,
            decimals=SIGMA_DECIMALS
        )
        self.sigma_input.value_changed.connect(self._on_sigma_changed)
        self.sigma_input.setVisible(False)
        filter_layout.addWidget(self.sigma_input)
        
        self.normalize_checkbox = QCheckBox("Normalize Kernel")
        self.normalize_checkbox.setChecked(True)
        self.normalize_checkbox.stateChanged.connect(self._on_normalize_changed)
        self.normalize_checkbox.setVisible(False)
        filter_layout.addWidget(self.normalize_checkbox)
        
        filter_group.setLayout(filter_layout)
        content_layout.addWidget(filter_group)
        
        nav_group = QGroupBox("Navigation")
        nav_layout = QVBoxLayout()
        
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self._on_start_clicked)
        nav_layout.addWidget(self.start_button)
        
        self.play_button_initial = QPushButton("Play")
        self.play_button_initial.clicked.connect(self._on_play_clicked)
        nav_layout.addWidget(self.play_button_initial)
        
        nav_buttons_layout = QGridLayout()
        
        self.previous_button = QPushButton("Previous")
        self.previous_button.clicked.connect(self._on_previous_clicked)
        nav_buttons_layout.addWidget(self.previous_button, 0, 0)
        
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self._on_next_clicked)
        nav_buttons_layout.addWidget(self.next_button, 0, 1)
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self._on_reset_clicked)
        nav_buttons_layout.addWidget(self.reset_button, 1, 0)
        
        self.play_button_navigating = QPushButton("Play")
        self.play_button_navigating.clicked.connect(self._on_play_clicked)
        nav_buttons_layout.addWidget(self.play_button_navigating, 1, 1)
        
        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self._on_pause_clicked)
        nav_buttons_layout.addWidget(self.pause_button, 1, 1)
        self.pause_button.setVisible(False)
        
        nav_layout.addLayout(nav_buttons_layout)
        
        self.speed_input = NumberInputWidget(
            label="Speed:",
            default_value=0.5,
            min_value=0.1,
            max_value=10.0,
            step=0.1,
            decimals=1
        )
        self.speed_input.setVisible(False)
        self.speed_input.value_changed.connect(self._on_speed_changed)
        nav_layout.addWidget(self.speed_input)
        
        self._playback_controller = PlaybackController(self._coordinator, self.speed_input)
        self._playback_controller.playback_state_changed.connect(self._on_playback_state_changed)
        nav_group.setLayout(nav_layout)
        
        content_layout.addWidget(nav_group)
        
        self._update_button_visibility()
        self._update_play_pause_buttons()
        
        self.type_dropdown.combobox.setEnabled(False)
        
        content_layout.addStretch()
        
        layout.addWidget(content_widget, 1)
    
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
    
    def _on_play_clicked(self) -> None:
        self._playback_controller.start()
    
    def _on_pause_clicked(self) -> None:
        self._playback_controller.stop()
        self._update_button_states()
    
    def _on_playback_state_changed(self, is_playing: bool) -> None:
        self._update_play_pause_buttons()
        if not is_playing:
            self._update_button_states()
    
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
    
    def _on_profile_changed(self, profile: str) -> None:
        self.profile_changed.emit(profile)
        
        if profile != DEFAULT_FILTER_PROFILE:
            self.category_dropdown.combobox.setEnabled(False)
            self.filter_dropdown.combobox.setEnabled(False)
            
            self.category_dropdown.set_value(DEFAULT_FILTER_CATEGORY)
            self.type_dropdown.set_value(PROFILE_FILTER_TYPE)
            self.filter_dropdown.set_value(PROFILE_FILTER_SELECTION)
            
            self.type_dropdown.combobox.setEnabled(False)
        else:
            self.category_dropdown.set_value(DEFAULT_FILTER_CATEGORY)
            self.type_dropdown.set_value(DEFAULT_FILTER_TYPE)
            self.filter_dropdown.set_value(DEFAULT_FILTER_SELECTION)
            
            self.category_dropdown.combobox.setEnabled(True)
            self.filter_dropdown.combobox.setEnabled(True)
            
            self.type_dropdown.combobox.setEnabled(False)
    
    def _on_category_changed(self, category: str) -> None:
        self.category_changed.emit(category)
        
        current_profile = self.profile_dropdown.combobox.currentText()
        if current_profile != DEFAULT_FILTER_PROFILE:
            return
        
        if category == "Non-Linear":
            self.type_dropdown.combobox.setEnabled(False)
            self.filter_dropdown.combobox.clear()
            self.filter_dropdown.combobox.addItems(FILTER_SELECTIONS_NONLINEAR)
            self.filter_dropdown.combobox.setCurrentText(DEFAULT_NONLINEAR_FILTER)
        else:
            self.type_dropdown.combobox.setEnabled(True)
            self.filter_dropdown.combobox.clear()
            self.filter_dropdown.combobox.addItems(FILTER_SELECTIONS_LINEAR)
            self.filter_dropdown.combobox.setCurrentText(DEFAULT_FILTER_SELECTION)
    
    def _on_type_changed(self, type_value: str) -> None:
        self.type_changed.emit(type_value)
    
    def _on_filter_changed(self, filter_value: str) -> None:
        self.filter_changed.emit(filter_value)
        
        current_profile = self.profile_dropdown.combobox.currentText()
        if current_profile != DEFAULT_FILTER_PROFILE:
            return
        
        current_category = self.category_dropdown.combobox.currentText()
        
        if current_category == "Non-Linear":
            self.type_dropdown.combobox.setEnabled(False)
            self.sigma_input.setVisible(False)
            self.normalize_checkbox.setVisible(False)
        elif filter_value == DEFAULT_FILTER_SELECTION:
            self.type_dropdown.combobox.setEnabled(False)
            self.sigma_input.setVisible(False)
            self.normalize_checkbox.setVisible(False)
        elif filter_value == "Gaussian":
            self.type_dropdown.combobox.setEnabled(False)
            self.sigma_input.setVisible(True)
            self.normalize_checkbox.setVisible(True)
        else:
            self.type_dropdown.combobox.setEnabled(True)
            self.sigma_input.setVisible(False)
            self.normalize_checkbox.setVisible(False)
    
    def _on_sigma_changed(self, sigma: float) -> None:
        self.sigma_changed.emit(sigma)
    
    def _on_normalize_changed(self, state: int) -> None:
        is_checked = state == 2
        self.normalize_changed.emit(is_checked)
    
    def _on_speed_changed(self, speed: float) -> None:
        self._playback_controller.update_speed()
    
    def _on_state_changed(self, state) -> None:
        if self._playback_controller.is_playing():
            self._playback_controller.stop()
        self._update_button_visibility()
        self._update_button_states()
        self._update_play_pause_buttons()
    
    def _on_position_changed(self, row: int, col: int) -> None:
        self._update_button_states()
        if self._playback_controller.is_playing() and self._coordinator and not self._coordinator.can_go_next():
            self._playback_controller.stop()
            self._update_play_pause_buttons()
            self._update_button_states()
    
    def _update_button_visibility(self) -> None:
        # Show/hide navigation buttons based on current application state
        if not self._coordinator:
            return
        
        from core import ApplicationState
        # Check if currently in INITIAL state
        is_initial = self._coordinator.get_state() == ApplicationState.INITIAL
        
        # In INITIAL state: show Start button and play button below it, hide navigation buttons
        # In NAVIGATING state: hide Start button and play button below it, show navigation buttons
        self.start_button.setVisible(is_initial)
        self.play_button_initial.setVisible(is_initial)
        self.reset_button.setVisible(not is_initial)
        self.previous_button.setVisible(not is_initial)
        self.next_button.setVisible(not is_initial)
        # Hide play/pause buttons from grid layout in INITIAL state
        if is_initial:
            self.play_button_navigating.setVisible(False)
            self.pause_button.setVisible(False)
    
    def _update_play_pause_buttons(self) -> None:
        if not self._coordinator:
            return
        
        from core import ApplicationState
        if self._coordinator.get_state() != ApplicationState.NAVIGATING:
            self.speed_input.setVisible(False)
            return
        
        is_playing = self._playback_controller.is_playing()
        # Show pause button when playing, show play button when not playing
        self.pause_button.setVisible(is_playing)
        self.play_button_navigating.setVisible(not is_playing)
        
        # Show speed input when playing
        self.speed_input.setVisible(is_playing)
        
        # Disable Previous and Next buttons when playing
        self.previous_button.setEnabled(not is_playing)
        self.next_button.setEnabled(not is_playing)
        
        # Set tooltips for disabled state
        if is_playing:
            self.previous_button.setToolTip("Previous is disabled while auto-progression is active")
            self.next_button.setToolTip("Next is disabled while auto-progression is active")
        else:
            self.previous_button.setToolTip("")
            self.next_button.setToolTip("")
    
    def _update_button_states(self) -> None:
        if not self._coordinator:
            return
        
        from core import ApplicationState
        is_initial = self._coordinator.get_state() == ApplicationState.INITIAL
        
        is_playing = self._playback_controller.is_playing()
        if is_playing:
            self.previous_button.setEnabled(False)
            self.next_button.setEnabled(False)
            return
        
        # In INITIAL state, play button should always be enabled (can start)
        if is_initial:
            self.play_button_initial.setEnabled(True)
        else:
            # In NAVIGATING state, disable Previous button if at the start position
            can_go_previous = self._coordinator.can_go_previous()
            self.previous_button.setEnabled(can_go_previous)
            
            # Disable Next button if at the end position
            can_go_next = self._coordinator.can_go_next()
            self.next_button.setEnabled(can_go_next)
            
            # Disable play button if at the end (no next position available)
            self.play_button_navigating.setEnabled(can_go_next)
