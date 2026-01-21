from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.main_window import MainWindow


class MainWindowSignalConnector:
    def __init__(self, main_window: 'MainWindow'):
        self._main_window = main_window
    
    def connect_all_signals(self) -> None:
        self._connect_input_mode_signals()
        self._connect_display_signals()
        self._connect_kernel_signals()
        self._connect_filter_signals()
        self._connect_calculation_signals()
        self._connect_config_change_signals()
        self._connect_image_upload_signals()
        self._initialize_kernel_config()
    
    def _connect_input_mode_signals(self) -> None:
        self._main_window._control_panel.input_mode_changed.connect(
            self._main_window._input_image.set_edit_mode
        )
    
    def _connect_display_signals(self) -> None:
        self._main_window._control_panel.show_pixel_values_changed.connect(
            self._main_window._input_image.set_show_pixel_values
        )
        self._main_window._control_panel.show_pixel_values_changed.connect(
            self._main_window._output_image.set_show_pixel_values
        )
        self._main_window._control_panel.show_colors_changed.connect(
            self._main_window._input_image.set_show_colors
        )
        self._main_window._control_panel.show_colors_changed.connect(
            self._main_window._output_image.set_show_colors
        )
    
    def _connect_kernel_signals(self) -> None:
        self._main_window._kernel_config.kernel_size_input.value_changed.connect(
            self._main_window._coordinator.set_kernel_size
        )
    
    def _connect_filter_signals(self) -> None:
        self._main_window._control_panel.filter_changed.connect(
            self._main_window._kernel_config.set_filter
        )
        self._main_window._control_panel.filter_changed.connect(
            self._main_window._filter_calculations.set_filter
        )
        self._main_window._control_panel.sigma_changed.connect(
            self._main_window._kernel_config.set_sigma
        )
        self._main_window._control_panel.normalize_changed.connect(
            self._main_window._kernel_config.set_normalize
        )
        self._main_window._control_panel.profile_changed.connect(
            self._main_window._kernel_config.set_profile
        )
        self._main_window._control_panel.category_changed.connect(
            self._main_window._filter_calculations.set_category
        )
        self._main_window._control_panel.type_changed.connect(
            self._main_window._filter_calculations.set_type
        )
        self._main_window._control_panel.type_changed.connect(
            self._main_window._kernel_config.final_kernel_grid.set_filter_type
        )
        self._main_window._control_panel.type_changed.connect(
            self._main_window._filter_calculations._formula_widget.set_filter_type
        )
    
    def _connect_calculation_signals(self) -> None:
        self._main_window._coordinator.state_changed.connect(
            self._main_window._filter_calculations.on_state_changed
        )
        self._main_window._coordinator.position_changed.connect(
            self._main_window._filter_calculations.update_calculation
        )
        self._main_window._kernel_config._kernel_model.grid_changed.connect(
            self._main_window._filter_calculations.on_kernel_changed
        )
        self._main_window._kernel_config.constant_input.value_changed.connect(
            self._main_window._filter_calculations.set_constant
        )
    
    def _connect_config_change_signals(self) -> None:
        self._main_window._input_model.grid_changed.connect(
            self._main_window._on_config_changed
        )
        self._main_window._kernel_config.kernel_size_input.value_changed.connect(
            self._main_window._on_config_changed
        )
        self._main_window._kernel_config._kernel_model.grid_changed.connect(
            self._main_window._on_config_changed
        )
        self._main_window._kernel_config.constant_input.value_changed.connect(
            self._main_window._on_config_changed
        )
        self._main_window._control_panel.category_changed.connect(
            self._main_window._on_config_changed
        )
        self._main_window._control_panel.type_changed.connect(
            self._main_window._on_config_changed
        )
        self._main_window._control_panel.filter_changed.connect(
            self._main_window._on_config_changed
        )
        self._main_window._control_panel.profile_changed.connect(
            self._main_window._on_config_changed
        )
        self._main_window._control_panel.sigma_changed.connect(
            self._main_window._on_config_changed
        )
        self._main_window._control_panel.normalize_changed.connect(
            self._main_window._on_config_changed
        )
    
    def _connect_image_upload_signals(self) -> None:
        def update_models_from_image(new_size: int) -> None:
            self._main_window._output_model.set_grid_size(new_size)
            self._main_window._coordinator.set_grid_size(new_size)
        
        self._main_window._input_image.grid_size_detected.connect(update_models_from_image)
    
    def _initialize_kernel_config(self) -> None:
        current_filter = self._main_window._control_panel.filter_dropdown.combobox.currentText()
        self._main_window._kernel_config.set_filter(current_filter)
