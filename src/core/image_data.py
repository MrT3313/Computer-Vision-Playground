from dataclasses import dataclass, field

# [!NOTE]
# The @dataclass decorator automatically generates an __init__ method for you behind the scenes. Therefore when main_window.py calls ImageData(width=width, height=height), it will automatically call the __init__ method with the provided width and height. 
# so while 10 is the default here, it will be overridden by the width and height passed in from main_window.py

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
    width: int = 10
    height: int = 10
    pixels: list[list[int | None]] = field(default_factory=list)

    def __post_init__(self):
        """Initialize pixel grid with white pixels if not provided."""
        if not self.pixels:
            self.pixels = [[255 for _ in range(self.width)] for _ in range(self.height)]

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
        """
        Toggle a pixel between black (0) and white (255).
        Used for drawing on the input image.
        
        Args:
            row: Row index
            col: Column index
        """
        current = self.get_pixel(row, col)
        self.set_pixel(row, col, 0 if current == 255 else 255)

    def resize(self, new_width: int, new_height: int):
        """
        Resize the image grid and reset all pixels to white.
        
        Args:
            new_width: New number of columns
            new_height: New number of rows
        """
        self.width = new_width
        self.height = new_height
        self.pixels = [[255 for _ in range(new_width)] for _ in range(new_height)]
    
    def clear(self):
        """Reset all pixels to white (255)."""
        self.pixels = [[255 for _ in range(self.width)] for _ in range(self.height)]
