from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QScrollArea, QWidget
from PySide6.QtCore import Qt
from core import ApplicationState
from core.mean_filter_calculator import MeanFilterCalculator
from .calculation_table_widget import CalculationTableWidget


class FilterCalculationsWidget(QFrame):
    def __init__(self, input_model, kernel_model, coordinator):
        super().__init__()
        self._input_model = input_model
        self._kernel_model = kernel_model
        self._coordinator = coordinator
        self._filter_type = "Mean"
        self._constant = 1.0
        
        self._calculator = MeanFilterCalculator(input_model, kernel_model, coordinator)
        
        self._setup_ui()
    
    def _setup_ui(self):
        # Configure the frame's visual appearance with a box border
        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(2)
        self.setMinimumHeight(150)
        
        # Create the main vertical layout that will contain all child widgets
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create the title bar frame at the top of the panel
        title_bar = QFrame()
        title_bar.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border-bottom: 1px solid rgba(0, 0, 0, 0.3);")
        title_bar.setFixedHeight(30)
        
        # Create layout for the title bar to hold the title label
        title_layout = QVBoxLayout(title_bar)
        title_layout.setContentsMargins(5, 0, 5, 0)
        
        # Create the title label
        title_label = QLabel("4. Filter Calculations")
        title_label.setStyleSheet("font-size: 12px; font-weight: bold; background: transparent; border: none;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        # Add the title label to the title bar layout
        title_layout.addWidget(title_label)
        
        # Create the content area widget that will hold all filter calculation controls
        self._content_area = QWidget()
        content_layout = QVBoxLayout(self._content_area)
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(10)
        
        self._placeholder_label = QLabel("Click 'Start' to begin calculations")
        self._placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(False)
        self._scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self._scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        self._scroll_area.setMinimumHeight(170)
        self._scroll_area.setMaximumHeight(170)
        
        self._table_widget = CalculationTableWidget()
        self._scroll_area.setWidget(self._table_widget)
        
        content_layout.addWidget(self._placeholder_label)
        content_layout.addWidget(self._scroll_area, 0)
        
        self._result_label = QLabel()
        self._result_label.setStyleSheet("color: white; font-size: 13px; font-weight: bold; padding: 10px;")
        self._result_label.setWordWrap(True)
        content_layout.addWidget(self._result_label, 0)
        
        main_layout.addWidget(title_bar)
        main_layout.addWidget(self._content_area, 1)
        
        self._show_placeholder()
    
    def _show_placeholder(self):
        self._placeholder_label.setVisible(True)
        self._scroll_area.setVisible(False)
        self._result_label.setVisible(False)
    
    def _show_content(self):
        self._placeholder_label.setVisible(False)
        self._scroll_area.setVisible(True)
        self._result_label.setVisible(True)
    
    def set_filter(self, filter_name: str) -> None:
        self._filter_type = filter_name
        self._update_display()
    
    def set_constant(self, constant: float) -> None:
        self._constant = constant
        self._update_display()
    
    def on_state_changed(self, state) -> None:
        if state == ApplicationState.INITIAL:
            self._show_placeholder()
        elif state == ApplicationState.NAVIGATING:
            self._show_content()
            self._update_display()
    
    def update_calculation(self, row: int, col: int) -> None:
        if self._coordinator.get_state() == ApplicationState.NAVIGATING:
            self._update_display()
    
    def on_kernel_changed(self, size: int, grid_data: list) -> None:
        if self._coordinator.get_state() == ApplicationState.NAVIGATING:
            self._update_display()
    
    def _update_display(self):
        if self._coordinator.get_state() != ApplicationState.NAVIGATING:
            return
        
        result = self._calculator.calculate(self._constant)
        
        self._table_widget.set_calculations(result['calculations'])
        
        calculations = result['calculations']
        sum_parts = " + ".join([f"{c['result']:.2f}" for c in calculations])
        sum_text = f"Sum: {sum_parts} = {result['total_sum']:.2f}"
        mean_text = f"Mean: {result['total_sum']:.2f} / {result['kernel_area']} = {result['output']:.2f}"
        result_text = f"Result: {result['output']:.2f}"
        
        full_text = f"{sum_text}\n\n{mean_text}\n\n{result_text}"
        self._result_label.setText(full_text)
