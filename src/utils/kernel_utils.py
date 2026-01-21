from typing import TypeVar

T = TypeVar('T', int, float)


def flip_kernel_180(kernel_data: list[list[T]]) -> list[list[T]]:
    """
    Flip a kernel 180 degrees for convolution operations.
    
    This is needed because convolution requires the kernel to be flipped
    compared to cross-correlation.
    """
    size = len(kernel_data)
    return [[kernel_data[size - 1 - row][size - 1 - col] 
             for col in range(size)] 
            for row in range(size)]
