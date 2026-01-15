from dataclasses import dataclass

from src.core.image_data import ImageData
from src.core.kernel_config import KernelPosition


@dataclass
class MeanFilterResult:
    coordinates: list[tuple[int, int]]
    values: list[int]
    total: int
    mean: float
    center_row: int
    center_col: int


class FilterCalculator:
    @staticmethod
    def calculate_mean_filter(
        image_data: ImageData,
        kernel_position: KernelPosition,
        kernel_size: int
    ) -> MeanFilterResult | None:
        if kernel_position.total_positions == 0:
            return None
        
        coordinates = []
        values = []
        
        for kr in range(kernel_size):
            for kc in range(kernel_size):
                r = kernel_position.row + kr
                c = kernel_position.col + kc
                coordinates.append((r, c))
                values.append(image_data.get_pixel(r, c))
        
        total = sum(values)
        mean = total / len(values)
        
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
