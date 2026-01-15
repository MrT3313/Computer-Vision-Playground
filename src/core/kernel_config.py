from dataclasses import dataclass


@dataclass
class KernelConfig:
    size: int = 3
    filter_type: str = "Blur"

    @property
    def half_size(self) -> int:
        return self.size // 2


@dataclass
class KernelPosition:
    row: int = 0
    col: int = 0
    total_positions: int = 0
    current_index: int = 0

    def calculate_total_positions(self, image_width: int, image_height: int, kernel_size: int) -> int:
        output_width = max(0, image_width - kernel_size + 1)
        output_height = max(0, image_height - kernel_size + 1)
        self.total_positions = output_width * output_height
        return self.total_positions

    def get_position_from_index(self, index: int, image_width: int, kernel_size: int) -> tuple[int, int]:
        output_width = max(1, image_width - kernel_size + 1)
        row = index // output_width
        col = index % output_width
        return row, col

    def set_position(self, index: int, image_width: int, kernel_size: int):
        self.current_index = max(0, min(index, self.total_positions - 1))
        self.row, self.col = self.get_position_from_index(self.current_index, image_width, kernel_size)
