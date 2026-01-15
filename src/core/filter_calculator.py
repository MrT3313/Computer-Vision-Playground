from dataclasses import dataclass

from src.core.image_data import ImageData
from src.core.kernel_config import KernelPosition, KernelConfig


@dataclass
class ConvolutionResult:
    coordinates: list[tuple[int, int]]
    values: list[int]
    kernel_values: list[list[float]]
    flipped_kernel: list[list[float]]
    constant: float
    result: float
    center_row: int
    center_col: int

@dataclass
class CrossCorrelationResult:
    coordinates: list[tuple[int, int]]
    values: list[int]
    kernel_values: list[list[float]]
    constant: float
    result: float
    center_row: int
    center_col: int

@dataclass
class MedianFilterResult:
    coordinates: list[tuple[int, int]]
    values: list[int]
    sorted_values: list[int]
    median: float
    constant: float
    result: float
    center_row: int
    center_col: int


class FilterCalculator:
    """
    Performs filter calculations on image data.
    Supports convolution, cross-correlation, and median filtering.
    """
    
    @staticmethod
    def calculate_convolution(
        image_data: ImageData,
        kernel_position: KernelPosition,
        kernel_config: KernelConfig
    ) -> ConvolutionResult | None:
        if kernel_position.total_positions == 0:
            return None
        
        kernel_size = kernel_config.size
        
        if kernel_config.filter_selection == "Mean":
            coordinates = []
            values = []
            
            for kr in range(kernel_size):
                for kc in range(kernel_size):
                    r = kernel_position.row + kr
                    c = kernel_position.col + kc
                    pixel_value = image_data.get_pixel(r, c)
                    coordinates.append((r, c))
                    values.append(pixel_value)
            
            mean_value = sum(values) / len(values)
            final_result = mean_value * kernel_config.constant
            
            center_row = kernel_position.row + kernel_size // 2
            center_col = kernel_position.col + kernel_size // 2
            
            kernel = [[1.0 for _ in range(kernel_size)] for _ in range(kernel_size)]
            
            return ConvolutionResult(
                coordinates=coordinates,
                values=values,
                kernel_values=kernel,
                flipped_kernel=kernel,
                constant=kernel_config.constant,
                result=final_result,
                center_row=center_row,
                center_col=center_col
            )
        else:
            kernel = kernel_config.values
            
            flipped_kernel = [[kernel[kernel_size - 1 - r][kernel_size - 1 - c] 
                              for c in range(kernel_size)] 
                             for r in range(kernel_size)]
            
            coordinates = []
            values = []
            result_sum = 0.0
            
            for kr in range(kernel_size):
                for kc in range(kernel_size):
                    r = kernel_position.row + kr
                    c = kernel_position.col + kc
                    pixel_value = image_data.get_pixel(r, c)
                    coordinates.append((r, c))
                    values.append(pixel_value)
                    result_sum += pixel_value * flipped_kernel[kr][kc]
            
            final_result = result_sum * kernel_config.constant
            
            center_row = kernel_position.row + kernel_size // 2
            center_col = kernel_position.col + kernel_size // 2
            
            return ConvolutionResult(
                coordinates=coordinates,
                values=values,
                kernel_values=kernel,
                flipped_kernel=flipped_kernel,
                constant=kernel_config.constant,
                result=final_result,
                center_row=center_row,
                center_col=center_col
            )
    
    @staticmethod
    def calculate_cross_correlation(
        image_data: ImageData,
        kernel_position: KernelPosition,
        kernel_config: KernelConfig
    ) -> CrossCorrelationResult | None:
        if kernel_position.total_positions == 0:
            return None
        
        kernel_size = kernel_config.size
        
        if kernel_config.filter_selection == "Mean":
            coordinates = []
            values = []
            
            for kr in range(kernel_size):
                for kc in range(kernel_size):
                    r = kernel_position.row + kr
                    c = kernel_position.col + kc
                    pixel_value = image_data.get_pixel(r, c)
                    coordinates.append((r, c))
                    values.append(pixel_value)
            
            mean_value = sum(values) / len(values)
            final_result = mean_value * kernel_config.constant
            
            center_row = kernel_position.row + kernel_size // 2
            center_col = kernel_position.col + kernel_size // 2
            
            kernel = [[1.0 for _ in range(kernel_size)] for _ in range(kernel_size)]
            
            return CrossCorrelationResult(
                coordinates=coordinates,
                values=values,
                kernel_values=kernel,
                constant=kernel_config.constant,
                result=final_result,
                center_row=center_row,
                center_col=center_col
            )
        else:
            kernel = kernel_config.values
            
            coordinates = []
            values = []
            result_sum = 0.0
            
            for kr in range(kernel_size):
                for kc in range(kernel_size):
                    r = kernel_position.row + kr
                    c = kernel_position.col + kc
                    pixel_value = image_data.get_pixel(r, c)
                    coordinates.append((r, c))
                    values.append(pixel_value)
                    result_sum += pixel_value * kernel[kr][kc]
            
            final_result = result_sum * kernel_config.constant
            
            center_row = kernel_position.row + kernel_size // 2
            center_col = kernel_position.col + kernel_size // 2
            
            return CrossCorrelationResult(
                coordinates=coordinates,
                values=values,
                kernel_values=kernel,
                result=final_result,
                center_row=center_row,
                center_col=center_col
            )
    
    @staticmethod
    def calculate_median_filter(
        image_data: ImageData,
        kernel_position: KernelPosition,
        kernel_size: int,
        constant: float
    ) -> MedianFilterResult | None:
        if kernel_position.total_positions == 0:
            return None
        
        coordinates = []
        values = []
        
        for kr in range(kernel_size):
            for kc in range(kernel_size):
                r = kernel_position.row + kr
                c = kernel_position.col + kc
                pixel_value = image_data.get_pixel(r, c)
                coordinates.append((r, c))
                values.append(pixel_value)
        
        sorted_values = sorted(values)
        median = sorted_values[len(sorted_values) // 2]
        final_result = median * constant
        
        center_row = kernel_position.row + kernel_size // 2
        center_col = kernel_position.col + kernel_size // 2
        
        return MedianFilterResult(
            coordinates=coordinates,
            values=values,
            sorted_values=sorted_values,
            median=float(median),
            constant=constant,
            result=final_result,
            center_row=center_row,
            center_col=center_col
        )
