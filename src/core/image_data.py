from dataclasses import dataclass, field

from src.consts.defaults import (
    DEFAULT_IMAGE_WIDTH,
    DEFAULT_IMAGE_HEIGHT,
    DEFAULT_WHITE_PIXEL,
    DEFAULT_BLACK_PIXEL,
)

@dataclass
class ImageData:
    """
    Represents image data as a 2D grid of pixel values.
    
    Pixels are stored as grayscale values (0-255) where:
    - 0 = black
    - 255 = white
    - None = no value computed yet (for output images)
    
    Attributes:
        width: Number of columns in the image
        height: Number of rows in the image
        pixels: 2D list of pixel values [row][col]
    """
    width: int = DEFAULT_IMAGE_WIDTH
    height: int = DEFAULT_IMAGE_HEIGHT
    pixels: list[list[int | None]] = field(default_factory=list)

    def __post_init__(self):
        if not self.pixels:
            self.pixels = [[DEFAULT_WHITE_PIXEL for _ in range(self.width)] for _ in range(self.height)]

    def get_pixel(self, row: int, col: int) -> int | None:
        """
        Get the pixel value at a specific position.
        
        Args:
            row: Row index
            col: Column index
            
        Returns:
            Pixel value (0-255) or None if position is out of bounds
        """
        if 0 <= row < self.height and 0 <= col < self.width:
            return self.pixels[row][col]
        return None

    def set_pixel(self, row: int, col: int, value: int):
        """
        Set the pixel value at a specific position.
        
        Args:
            row: Row index
            col: Column index
            value: Pixel value (0-255)
        """
        if 0 <= row < self.height and 0 <= col < self.width:
            self.pixels[row][col] = value

    def toggle_pixel(self, row: int, col: int):
        current = self.get_pixel(row, col)
        self.set_pixel(row, col, DEFAULT_BLACK_PIXEL if current == DEFAULT_WHITE_PIXEL else DEFAULT_WHITE_PIXEL)

    def resize(self, new_width: int, new_height: int):
        self.width = new_width
        self.height = new_height
        self.pixels = [[DEFAULT_WHITE_PIXEL for _ in range(new_width)] for _ in range(new_height)]
    
    def clear(self):
        self.pixels = [[DEFAULT_WHITE_PIXEL for _ in range(self.width)] for _ in range(self.height)]
