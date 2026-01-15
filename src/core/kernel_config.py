from dataclasses import dataclass, field

@dataclass
class KernelConfig:
    """
    Configuration for a convolution kernel (filter).
    
    A kernel is a small matrix that slides over the image to perform operations.
    For example, a 3x3 mean filter kernel would average 9 pixels at a time.
    
    Attributes:
        size: Dimension of the square kernel (e.g., 3 for a 3x3 kernel)
        filter_type: Type of filter being applied (e.g., "Mean", "Blur", "Sharpen")
        values: 2D list of kernel weights/coefficients [row][col]
    """
    size: int = 3
    filter_type: str = "Mean"
    values: list[list[float]] = field(default_factory=list)

    def __post_init__(self):
        """Initialize kernel values to zeros if not provided."""
        if not self.values:
            self.values = [[0.0 for _ in range(self.size)] for _ in range(self.size)]

    @property
    def half_size(self) -> int:
        """
        Get half the kernel size (used for finding the center pixel).
        
        Returns:
            Integer division of size by 2 (e.g., 3x3 kernel returns 1)
        """
        return self.size // 2

    def get_value(self, row: int, col: int) -> float:
        """
        Get the kernel value at a specific position.
        
        Args:
            row: Row index in the kernel
            col: Column index in the kernel
            
        Returns:
            Kernel value at that position, or 0.0 if out of bounds
        """
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.values[row][col]
        return 0.0

    def set_value(self, row: int, col: int, value: float):
        """
        Set the kernel value at a specific position.
        
        Args:
            row: Row index in the kernel
            col: Column index in the kernel
            value: New kernel value
        """
        if 0 <= row < self.size and 0 <= col < self.size:
            self.values[row][col] = value

    def resize(self, new_size: int):
        """
        Resize the kernel and reset all values to zero.
        
        Args:
            new_size: New dimension for the square kernel
        """
        self.size = new_size
        self.values = [[0.0 for _ in range(new_size)] for _ in range(new_size)]

    def get_flat_values(self) -> list[float]:
        """
        Get all kernel values as a flat list (row by row).
        
        Returns:
            1D list of all kernel values
        """
        return [value for row in self.values for value in row]


@dataclass
class KernelPosition:
    """
    Tracks the current position of a kernel as it moves across an image.
    
    In convolution, a kernel slides across the image from top-left to bottom-right,
    computing a value at each valid position. This class manages that position.
    
    Attributes:
        row: Current top-left row of the kernel on the image
        col: Current top-left column of the kernel on the image
        total_positions: Total number of valid positions the kernel can occupy
        current_index: Current position index (0 to total_positions-1)
    """
    row: int = 0
    col: int = 0
    total_positions: int = 0
    current_index: int = 0

    def calculate_total_positions(self, image_width: int, image_height: int, kernel_size: int) -> int:
        """
        Calculate how many valid positions the kernel can occupy on the image.
        
        For a 10x10 image with a 3x3 kernel:
        - Output width = 10 - 3 + 1 = 8
        - Output height = 10 - 3 + 1 = 8
        - Total positions = 8 * 8 = 64
        
        Args:
            image_width: Width of the input image
            image_height: Height of the input image
            kernel_size: Size of the kernel
            
        Returns:
            Total number of valid kernel positions
        """
        output_width = max(0, image_width - kernel_size + 1)
        output_height = max(0, image_height - kernel_size + 1)
        self.total_positions = output_width * output_height
        return self.total_positions

    def get_position_from_index(self, index: int, image_width: int, kernel_size: int) -> tuple[int, int]:
        """
        Convert a linear index to a 2D (row, col) position.
        
        Positions are numbered left-to-right, top-to-bottom:
        Index 0 = (0, 0), Index 1 = (0, 1), ..., Index n = (row, col)
        
        Args:
            index: Linear position index
            image_width: Width of the input image
            kernel_size: Size of the kernel
            
        Returns:
            (row, col) tuple representing the top-left corner of the kernel
        """
        output_width = max(1, image_width - kernel_size + 1)
        row = index // output_width  # Integer division gives row
        col = index % output_width   # Remainder gives column
        return row, col

    def set_position(self, index: int, image_width: int, kernel_size: int):
        """
        Move the kernel to a specific position index.
        
        Args:
            index: Target position index (will be clamped to valid range)
            image_width: Width of the input image
            kernel_size: Size of the kernel
        """
        # Clamp index to valid range [0, total_positions-1]
        self.current_index = max(0, min(index, self.total_positions - 1))
        # Convert index to 2D position
        self.row, self.col = self.get_position_from_index(self.current_index, image_width, kernel_size)
