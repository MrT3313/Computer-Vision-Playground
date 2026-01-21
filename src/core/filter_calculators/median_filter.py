class MedianFilterCalculator:
    def __init__(self, input_model, kernel_model, coordinator):
        self._input_model = input_model
        self._kernel_model = kernel_model
        self._coordinator = coordinator
    
    def calculate(self, constant: float) -> dict:
        affected_cells = self._coordinator.get_affected_cells()
        output_cell = self._coordinator.get_output_cell()
        
        kernel_size = self._kernel_model.get_grid_size()
        input_data = self._input_model.get_grid_data()
        
        calculations = []
        pixel_values = []
        
        for idx, (row, col) in enumerate(affected_cells):
            input_value = input_data[row][col]
            pixel_values.append(input_value)
            
            calculations.append({
                'index': idx,
                'coordinate': (row, col),
                'input_value': input_value,
                'kernel_value': 1.0,
                'constant': constant,
                'final_kernel_value': 1.0,
                'calculation': str(input_value),
                'result': input_value,
                'bounded_result': input_value
            })
        
        sorted_values = sorted(pixel_values)
        num_values = len(sorted_values)
        
        if num_values == 0:
            median_value = 0.0
            median_index = 0
            left_index = 0
            right_index = 0
        elif num_values % 2 == 1:
            median_index = num_values // 2
            median_value = float(sorted_values[median_index])
            left_index = median_index
            right_index = median_index
        else:
            left_index = (num_values - 1) // 2
            right_index = num_values // 2
            median_index = left_index
            median_value = (sorted_values[left_index] + sorted_values[right_index]) / 2.0
        
        sorted_with_indices = sorted(enumerate(pixel_values), key=lambda x: x[1])
        for sorted_pos, (original_idx, value) in enumerate(sorted_with_indices):
            calculations[original_idx]['sorted_index'] = sorted_pos
            calculations[original_idx]['is_median'] = (sorted_pos == median_index) or (num_values % 2 == 0 and sorted_pos in [left_index, right_index])
        
        return {
            'calculations': calculations,
            'sorted_values': sorted_values,
            'median_index': median_index,
            'output': median_value,
            'output_cell': output_cell
        }
