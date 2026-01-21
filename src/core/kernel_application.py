from enum import Enum
from PySide6.QtCore import QObject, Signal


class ApplicationState(Enum):
    # Initial state before navigation has started
    INITIAL = "initial"
    # Active state when user is navigating through grid positions
    NAVIGATING = "navigating"


class KernelApplicationCoordinator(QObject):
    """
    Coordinates kernel position and navigation state during filter application.
    
    Manages the current position of the kernel as it moves across the input grid,
    tracking which cells are affected and where output values should be written.
    """
    position_changed = Signal(int, int)
    state_changed = Signal(object)
    
    def __init__(self, grid_size: int, kernel_size: int):
        super().__init__()
        # Store the size of the input grid
        self._grid_size = grid_size
        # Store the kernel radius (k, where full kernel is 2k+1)
        self._kernel_size = kernel_size
        # Initialize current position to the first valid position (kernel_size, kernel_size)
        self._current_row = kernel_size
        self._current_col = kernel_size
        # Start in INITIAL state
        self._state = ApplicationState.INITIAL
    
    def start(self) -> None:
        # Begin navigation if currently in INITIAL state
        if self._state == ApplicationState.INITIAL:
            # Transition to NAVIGATING state
            self._state = ApplicationState.NAVIGATING
            self.state_changed.emit(self._state)
            # Emit the initial position
            self.position_changed.emit(self._current_row, self._current_col)
    
    def reset(self) -> None:
        # Reset position to the initial starting position
        self._current_row = self._kernel_size
        self._current_col = self._kernel_size
        # Return to INITIAL state
        self._state = ApplicationState.INITIAL
        self.state_changed.emit(self._state)
        # Emit the reset position
        self.position_changed.emit(self._current_row, self._current_col)
    
    def next(self) -> None:
        # Only proceed if in NAVIGATING state and can move forward
        if self._state != ApplicationState.NAVIGATING or not self.can_go_next():
            return
        
        # Move to next column position
        self._current_col += 1
        # If reached end of row, wrap to next row's first column
        if self._current_col > self._get_max_col():
            self._current_col = self._get_min_col()
            self._current_row += 1
        
        # Emit the new position
        self.position_changed.emit(self._current_row, self._current_col)
    
    def previous(self) -> None:
        # Only proceed if in NAVIGATING state and can move backward
        if self._state != ApplicationState.NAVIGATING or not self.can_go_previous():
            return
        
        # Move to previous column position
        self._current_col -= 1
        # If reached start of row, wrap to previous row's last column
        if self._current_col < self._get_min_col():
            self._current_row -= 1
            self._current_col = self._get_max_col()
        
        # Emit the new position
        self.position_changed.emit(self._current_row, self._current_col)
    
    def can_go_next(self) -> bool:
        # Cannot navigate if not in NAVIGATING state
        if self._state != ApplicationState.NAVIGATING:
            return False
        # Can go next if not at the last valid position (bottom-right corner)
        return not (self._current_row == self._get_max_row() and 
                   self._current_col == self._get_max_col())
    
    def can_go_previous(self) -> bool:
        # Cannot navigate if not in NAVIGATING state
        if self._state != ApplicationState.NAVIGATING:
            return False
        # Can go previous if not at the first valid position (top-left corner)
        return not (self._current_row == self._get_min_row() and 
                   self._current_col == self._get_min_col())
    
    def get_affected_cells(self) -> list[tuple[int, int]]:
        # Return list of all grid cells that fall within the kernel centered at current position
        cells = []
        kernel_radius = self._kernel_size
        
        # Iterate through all positions in the kernel window
        for row_offset in range(-kernel_radius, kernel_radius + 1):
            for col_offset in range(-kernel_radius, kernel_radius + 1):
                # Calculate absolute grid coordinates
                cell_row = self._current_row + row_offset
                cell_col = self._current_col + col_offset
                
                # Only include cells that are within the grid bounds
                if 0 <= cell_row < self._grid_size and 0 <= cell_col < self._grid_size:
                    cells.append((cell_row, cell_col))
        
        return cells
    
    def get_output_cell(self) -> tuple[int, int]:
        # Return the current center position (the output cell for the convolution)
        return (self._current_row, self._current_col)
    
    def get_state(self) -> ApplicationState:
        # Return the current application state
        return self._state
    
    def set_grid_size(self, size: int) -> None:
        # Update grid size and reset to initial state
        self._grid_size = size
        self.reset()
    
    def set_kernel_size(self, size: int) -> None:
        # Update kernel size and reset to initial state
        self._kernel_size = size
        self.reset()
    
    def _get_min_row(self) -> int:
        # Minimum valid row position (kernel radius from top edge)
        return self._kernel_size
    
    def _get_min_col(self) -> int:
        # Minimum valid column position (kernel radius from left edge)
        return self._kernel_size
    
    def _get_max_row(self) -> int:
        # Maximum valid row position (kernel radius from bottom edge)
        return self._grid_size - 1 - self._kernel_size
    
    def _get_max_col(self) -> int:
        # Maximum valid column position (kernel radius from right edge)
        return self._grid_size - 1 - self._kernel_size