from utils.kernel_utils import flip_kernel_180
from .base_filter import BaseFilterCalculator


class CustomFilterCalculator(BaseFilterCalculator):
    def calculate(self, constant: float, filter_type: str = "Cross-Correlation") -> dict:
        if filter_type == "Convolution":
            return self._calculate_convolution(constant)
        else:
            return super().calculate(constant, filter_type)
    
    def _calculate_convolution(self, constant: float) -> dict:
        affected_cells = self._coordinator.get_affected_cells()
        output_cell = self._coordinator.get_output_cell()
        
        kernel_size = self._kernel_model.get_grid_size()
        kernel_data = flip_kernel_180(self._kernel_model.get_grid_data())
        input_data = self._input_model.get_grid_data()
        
        calculations = []
        total_sum = 0.0
        
        for idx, (row, col) in enumerate(affected_cells):
            offset_row = row - output_cell[0]
            offset_col = col - output_cell[1]
            
            input_row = output_cell[0] - offset_row
            input_col = output_cell[1] - offset_col
            
            if 0 <= input_row < len(input_data) and 0 <= input_col < len(input_data[0]):
                input_value = input_data[input_row][input_col]
            else:
                input_value = 0
            
            kernel_row, kernel_col = self._offset_to_kernel_indices(offset_row, offset_col, kernel_size)
            kernel_value = kernel_data[kernel_row][kernel_col]
            final_kernel_value = kernel_value * constant
            result = input_value * final_kernel_value
            bounded_result = max(0, min(255, result))
            
            calculations.append({
                'index': idx,
                'coordinate': (input_row, input_col),
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
    
    def _calculate_output(self, total_sum: float, kernel_area: int, calculations: list) -> float:
        return total_sum
