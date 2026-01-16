import importlib

input_image = importlib.import_module('.1_input_image', package='ui')
kernel_config = importlib.import_module('.2_kernel_config', package='ui')
output_image = importlib.import_module('.3_output_image', package='ui')
filter_calculations = importlib.import_module('.4_filter_calculations', package='ui')
control_panel = importlib.import_module('.5_control_panel', package='ui')

from .main_window import MainWindow

__all__ = ["MainWindow", "input_image", "kernel_config", "output_image", "filter_calculations", "control_panel"]
