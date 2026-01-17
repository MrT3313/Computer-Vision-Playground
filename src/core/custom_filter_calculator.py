class CustomFilterCalculator:
    def __init__(self, input_model, kernel_model, coordinator):
        # Store reference to the input image grid model
        self._input_model = input_model
        # Store reference to the kernel grid model
        self._kernel_model = kernel_model
        # Store reference to the application coordinator for position tracking
        self._coordinator = coordinator
    
    def calculate(self, constant: float, filter_type: str = "Cross-Correlation") -> dict:
        # Get the list of input cells affected by the kernel at current position
        affected_cells = self._coordinator.get_affected_cells()
        # Get the current output cell position (center of kernel)
        output_cell = self._coordinator.get_output_cell()
        
        # Get kernel dimensions and data
        kernel_size = self._kernel_model.get_grid_size()
        kernel_data = self._kernel_model.get_grid_data()
        # Get input image data
        input_data = self._input_model.get_grid_data()
        
        # If using convolution (not cross-correlation), flip the kernel 180 degrees
        if filter_type == "Convolution":
            # Create a new kernel with rows and columns reversed (180-degree rotation)
            kernel_data = [[kernel_data[kernel_size - 1 - row][kernel_size - 1 - col] 
                           for col in range(kernel_size)] 
                          for row in range(kernel_size)]
        
        # Initialize list to store step-by-step calculation details
        calculations = []
        # Initialize accumulator for the sum of all weighted pixel values
        total_sum = 0.0
        
        # Iterate through each cell affected by the kernel
        for idx, (row, col) in enumerate(affected_cells):
            # Get the input pixel value at this position
            input_value = input_data[row][col]
            
            # Calculate the offset from the output cell to map to kernel coordinates
            offset_row = row - output_cell[0]
            offset_col = col - output_cell[1]
            # Convert offset to kernel array indices (kernel center is at kernel_size // 2)
            kernel_row = offset_row + (kernel_size // 2)
            kernel_col = offset_col + (kernel_size // 2)
            
            # Get the kernel weight at this position (possibly flipped if convolution)
            kernel_value = kernel_data[kernel_row][kernel_col]
            # Apply the constant multiplier to get the final kernel weight
            final_kernel_value = kernel_value * constant
            # Calculate weighted pixel value (input × kernel weight)
            result = input_value * final_kernel_value
            
            # Clamp result to valid pixel range [0, 255]
            bounded_result = max(0, min(255, result))
            
            # Store detailed calculation information for this cell
            calculations.append({
                'index': idx,  # Sequential index of this calculation
                'coordinate': (row, col),  # Grid position of input cell
                'input_value': input_value,  # Original input pixel value
                'kernel_value': kernel_value,  # Base kernel weight (possibly flipped)
                'constant': constant,  # Constant multiplier
                'final_kernel_value': final_kernel_value,  # Final kernel weight (kernel_value × constant)
                'calculation': f"({input_value}×{final_kernel_value:.2f})",  # Human-readable calculation string
                'result': result,  # Raw calculation result (may be outside [0, 255])
                'bounded_result': bounded_result  # Clamped result within valid pixel range
            })
            
            # Add this weighted value to the running total
            total_sum += bounded_result
        
        # Calculate kernel area (total number of kernel elements)
        kernel_area = kernel_size * kernel_size
        # For custom filter, output is the sum (not averaged like mean filter)
        final_output = total_sum
        
        # Return comprehensive calculation results
        return {
            'calculations': calculations,  # List of per-cell calculation details
            'total_sum': total_sum,  # Sum of all weighted pixel values
            'kernel_area': kernel_area,  # Total number of kernel elements
            'output': final_output,  # Final output value (sum, not averaged)
            'output_cell': output_cell  # Position where output will be written
        }