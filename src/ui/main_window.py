from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Computer Vision Playground")
        self.setMinimumSize(1200, 800)
        
        self._setup_ui()
    
    # CONFIGURE UI ############################################################
    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        left_widget = self._create_left_side()
        right_widget = self._create_right_side()
        
        main_layout.addWidget(left_widget, 1)
        main_layout.addWidget(right_widget, 0)
    
    def _create_left_side(self) -> QWidget:
        import importlib
        
        input_image_module = importlib.import_module('ui.1_input_image')
        kernel_config_module = importlib.import_module('ui.2_kernel_config')
        output_image_module = importlib.import_module('ui.3_output_image')
        filter_calculations_module = importlib.import_module('ui.4_filter_calculations')
        
        InputImageWidget = input_image_module.InputImageWidget
        KernelConfigWidget = kernel_config_module.KernelConfigWidget
        OutputImageWidget = output_image_module.OutputImageWidget
        FilterCalculationsWidget = filter_calculations_module.FilterCalculationsWidget
        
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setSpacing(10)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        top_row = QWidget()
        top_layout = QHBoxLayout(top_row)
        top_layout.setSpacing(10)
        top_layout.setContentsMargins(0, 0, 0, 0)
        
        input_image = InputImageWidget()
        kernel_config = KernelConfigWidget()
        output_image = OutputImageWidget()
        
        kernel_config.setFixedWidth(150)
        
        top_layout.addWidget(input_image, 1)
        top_layout.addWidget(kernel_config, 0)
        top_layout.addWidget(output_image, 1)
        
        filter_calculations = FilterCalculationsWidget()
        
        left_layout.addWidget(top_row, 60)
        left_layout.addWidget(filter_calculations, 40)
        
        return left_widget
    
    def _create_right_side(self) -> QWidget:
        import importlib
        
        control_panel_module = importlib.import_module('ui.5_control_panel')
        ControlPanelWidget = control_panel_module.ControlPanelWidget
        
        control_panel = ControlPanelWidget()
        control_panel.setFixedWidth(300)
        
        return control_panel
    # end - CONFIGURE UI ######################################################