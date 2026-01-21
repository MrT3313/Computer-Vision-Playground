from .base_filter import BaseFilterCalculator


class MeanFilterCalculator(BaseFilterCalculator):
    def _calculate_output(self, total_sum: float, kernel_area: int, calculations: list) -> float:
        return total_sum / kernel_area