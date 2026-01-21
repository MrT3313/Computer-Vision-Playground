from abc import ABC, abstractmethod
from typing import Any


class BaseFilterCalculator(ABC):
    """
    Base class for filter calculators providing common convolution/cross-correlation logic.
    
    Subclasses must implement _calculate_output() to define how the final result is computed
    from the weighted sum of input pixels.
    """
    def __init__(self, input_model, kernel_model, coordinator):
        self._input_model = input_model
        self._kernel_model = kernel_model
        self._coordinator = coordinator
    
    def calculate(self, constant: float, filter_type: str = "Cross-Correlation") -> dict[str, Any]:
        affected_cells = self._coordinator.get_affected_cells()
        output_cell = self._coordinator.get_output_cell()
        
        kernel_size = self._kernel_model.get_grid_size()
        kernel_data = self._kernel_model.get_grid_data()
        input_data = self._input_model.get_grid_data()
        
        calculations = []
        total_sum = 0.0
        
        for idx, (row, col) in enumerate(affected_cells):
            input_value = input_data[row][col]
            
            offset_row, offset_col = self._map_coordinates_to_kernel(row, col, output_cell, kernel_size, filter_type)
            kernel_row, kernel_col = self._offset_to_kernel_indices(offset_row, offset_col, kernel_size)
            
            kernel_value = kernel_data[kernel_row][kernel_col]
            final_kernel_value = kernel_value * constant
            result = input_value * final_kernel_value
            bounded_result = max(0, min(255, result))
            
            calculations.append({
                'index': idx,
                'coordinate': (row, col),
                'input_value': input_value,
                'kernel_value': kernel_value,
                'constant': constant,
                'final_kernel_value': final_kernel_value,
                'calculation': f"({input_value}×{final_kernel_value:.2f})",
                'result': result,
                'bounded_result': bounded_result
            })
            
            total_sum += bounded_result
        
        kernel_area = kernel_size * kernel_size
        final_output = self._calculate_output(total_sum, kernel_area, calculations)
        
        return {
            'calculations': calculations,
            'total_sum': total_sum,
            'kernel_area': kernel_area,
            'output': final_output,
            'output_cell': output_cell
        }
    
    def _map_coordinates_to_kernel(self, row: int, col: int, output_cell: tuple[int, int], 
                                   kernel_size: int, filter_type: str) -> tuple[int, int]:
        offset_row = row - output_cell[0]
        offset_col = col - output_cell[1]
        return offset_row, offset_col
    
    def _offset_to_kernel_indices(self, offset_row: int, offset_col: int, kernel_size: int) -> tuple[int, int]:
        kernel_row = offset_row + (kernel_size // 2)
        kernel_col = offset_col + (kernel_size // 2)
        return kernel_row, kernel_col
    
    @abstractmethod
    def _calculate_output(self, total_sum: float, kernel_area: int, calculations: list[dict]) -> float:
        """
        Calculate the final output value from the weighted sum.
        
        Args:
            total_sum: Sum of all weighted pixel values
            kernel_area: Total number of kernel elements
            calculations: List of per-cell calculation details
            
        Returns:
            Final output pixel value
        """
        pass
