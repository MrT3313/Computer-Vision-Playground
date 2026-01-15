from dataclasses import dataclass, field


@dataclass
class ImageData:
    width: int = 10
    height: int = 10
    pixels: list[list[int | None]] = field(default_factory=list)

    def __post_init__(self):
        if not self.pixels:
            self.pixels = [[255 for _ in range(self.width)] for _ in range(self.height)]

    def get_pixel(self, row: int, col: int) -> int | None:
        if 0 <= row < self.height and 0 <= col < self.width:
            return self.pixels[row][col]
        return None

    def set_pixel(self, row: int, col: int, value: int):
        if 0 <= row < self.height and 0 <= col < self.width:
            self.pixels[row][col] = value

    def toggle_pixel(self, row: int, col: int):
        current = self.get_pixel(row, col)
        self.set_pixel(row, col, 0 if current == 255 else 255)

    def resize(self, new_width: int, new_height: int):
        self.width = new_width
        self.height = new_height
        self.pixels = [[255 for _ in range(new_width)] for _ in range(new_height)]
    
    def clear(self):
        self.pixels = [[255 for _ in range(self.width)] for _ in range(self.height)]
