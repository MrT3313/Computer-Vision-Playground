from .base_filter import BaseFilterCalculator


class GaussianFilterCalculator(BaseFilterCalculator):
    def _calculate_output(self, total_sum: float, kernel_area: int, calculations: list) -> float:
        return total_sum