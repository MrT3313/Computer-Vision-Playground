from dataclasses import dataclass, field


@dataclass
class KernelConfig:
    size: int = 3
    filter_type: str = "Blur"
    values: list[list[float]] = field(default_factory=list)

    def __post_init__(self):
        if not self.values:
            self.values = [[0.0 for _ in range(self.size)] for _ in range(self.size)]

    @property
    def half_size(self) -> int:
        return self.size // 2

    def get_value(self, row: int, col: int) -> float:
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.values[row][col]
        return 0.0

    def set_value(self, row: int, col: int, value: float):
        if 0 <= row < self.size and 0 <= col < self.size:
            self.values[row][col] = value

    def resize(self, new_size: int):
        self.size = new_size
        self.values = [[0.0 for _ in range(new_size)] for _ in range(new_size)]

    def get_flat_values(self) -> list[float]:
        return [value for row in self.values for value in row]


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
