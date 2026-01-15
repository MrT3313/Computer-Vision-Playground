from dataclasses import dataclass

from src.core.image_data import ImageData
from src.core.kernel_config import KernelPosition


@dataclass
class MeanFilterResult:
    """
    Contains the results of a mean filter calculation at a specific kernel position.
    
    Attributes:
        coordinates: List of (row, col) tuples for each pixel under the kernel
        values: List of pixel values at those coordinates
        total: Sum of all pixel values
        mean: Average of all pixel values (total / number of values)
        center_row: Row index where the calculated mean value should be placed
        center_col: Column index where the calculated mean value should be placed
    """
    coordinates: list[tuple[int, int]]
    values: list[int]
    total: int
    mean: float
    center_row: int
    center_col: int


class FilterCalculator:
    """
    Performs convolution filter calculations on image data.
    Currently supports mean (average) filtering.
    """
    
    @staticmethod
    def calculate_mean_filter(
        image_data: ImageData,
        kernel_position: KernelPosition,
        kernel_size: int
    ) -> MeanFilterResult | None:
        """
        Calculate the mean (average) value of pixels under a kernel at a specific position.
        
        The mean filter works by:
        1. Taking all pixel values under the kernel window
        2. Summing them together
        3. Dividing by the number of pixels
        4. Placing the result at the center of the kernel position
        
        Args:
            image_data: The input image containing pixel values
            kernel_position: Current position of the kernel on the image
            kernel_size: Size of the kernel (e.g., 3 for a 3x3 kernel)
            
        Returns:
            MeanFilterResult containing coordinates, values, and calculated mean,
            or None if there are no valid positions
        """
        # Return None if kernel cannot be placed on the image
        if kernel_position.total_positions == 0:
            return None
        
        # Collect all pixel coordinates and values under the kernel
        coordinates = []
        values = []
        
        # Loop through each position in the kernel (row by row)
        for kr in range(kernel_size):
            for kc in range(kernel_size):
                # Calculate absolute image position
                r = kernel_position.row + kr
                c = kernel_position.col + kc
                # Store coordinate and pixel value
                coordinates.append((r, c))
                values.append(image_data.get_pixel(r, c))
        
        # Calculate the sum and mean of all values
        total = sum(values)
        mean = total / len(values)
        
        # Determine where to place the result (center of the kernel)
        center_row = kernel_position.row + kernel_size // 2
        center_col = kernel_position.col + kernel_size // 2
        
        return MeanFilterResult(
            coordinates=coordinates,
            values=values,
            total=total,
            mean=mean,
            center_row=center_row,
            center_col=center_col
        )
