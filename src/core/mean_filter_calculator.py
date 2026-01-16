class MeanFilterCalculator:
    def __init__(self, input_model, kernel_model, coordinator):
        self._input_model = input_model
        self._kernel_model = kernel_model
        self._coordinator = coordinator
    
    def calculate(self, constant: float) -> dict:
        affected_cells = self._coordinator.get_affected_cells()
        output_cell = self._coordinator.get_output_cell()
        
        kernel_size = self._kernel_model.get_grid_size()
        kernel_data = self._kernel_model.get_grid_data()
        input_data = self._input_model.get_grid_data()
        
        calculations = []
        total_sum = 0.0
        
        for idx, (row, col) in enumerate(affected_cells):
            input_value = input_data[row][col]
            
            offset_row = row - output_cell[0]
            offset_col = col - output_cell[1]
            kernel_row = offset_row + (kernel_size // 2)
            kernel_col = offset_col + (kernel_size // 2)
            
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
        final_output = total_sum / kernel_area
        
        return {
            'calculations': calculations,
            'total_sum': total_sum,
            'kernel_area': kernel_area,
            'output': final_output,
            'output_cell': output_cell
        }
