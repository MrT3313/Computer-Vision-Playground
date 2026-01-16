from enum import Enum
from PySide6.QtCore import QObject, Signal


class ApplicationState(Enum):
    INITIAL = "initial"
    NAVIGATING = "navigating"


class KernelApplicationCoordinator(QObject):
    position_changed = Signal(int, int)
    state_changed = Signal(object)
    
    def __init__(self, grid_size: int, kernel_size: int):
        super().__init__()
        self._grid_size = grid_size
        self._kernel_size = kernel_size
        self._current_row = kernel_size
        self._current_col = kernel_size
        self._state = ApplicationState.INITIAL
    
    def start(self) -> None:
        if self._state == ApplicationState.INITIAL:
            self._state = ApplicationState.NAVIGATING
            self.state_changed.emit(self._state)
            self.position_changed.emit(self._current_row, self._current_col)
    
    def reset(self) -> None:
        self._current_row = self._kernel_size
        self._current_col = self._kernel_size
        self._state = ApplicationState.INITIAL
        self.state_changed.emit(self._state)
        self.position_changed.emit(self._current_row, self._current_col)
    
    def next(self) -> None:
        if self._state != ApplicationState.NAVIGATING or not self.can_go_next():
            return
        
        self._current_col += 1
        if self._current_col > self._get_max_col():
            self._current_col = self._get_min_col()
            self._current_row += 1
        
        self.position_changed.emit(self._current_row, self._current_col)
    
    def previous(self) -> None:
        if self._state != ApplicationState.NAVIGATING or not self.can_go_previous():
            return
        
        self._current_col -= 1
        if self._current_col < self._get_min_col():
            self._current_row -= 1
            self._current_col = self._get_max_col()
        
        self.position_changed.emit(self._current_row, self._current_col)
    
    def can_go_next(self) -> bool:
        if self._state != ApplicationState.NAVIGATING:
            return False
        return not (self._current_row == self._get_max_row() and 
                   self._current_col == self._get_max_col())
    
    def can_go_previous(self) -> bool:
        if self._state != ApplicationState.NAVIGATING:
            return False
        return not (self._current_row == self._get_min_row() and 
                   self._current_col == self._get_min_col())
    
    def get_affected_cells(self) -> list[tuple[int, int]]:
        cells = []
        kernel_radius = self._kernel_size
        
        for row_offset in range(-kernel_radius, kernel_radius + 1):
            for col_offset in range(-kernel_radius, kernel_radius + 1):
                cell_row = self._current_row + row_offset
                cell_col = self._current_col + col_offset
                
                if 0 <= cell_row < self._grid_size and 0 <= cell_col < self._grid_size:
                    cells.append((cell_row, cell_col))
        
        return cells
    
    def get_output_cell(self) -> tuple[int, int]:
        return (self._current_row, self._current_col)
    
    def get_state(self) -> ApplicationState:
        return self._state
    
    def set_grid_size(self, size: int) -> None:
        self._grid_size = size
        self.reset()
    
    def set_kernel_size(self, size: int) -> None:
        self._kernel_size = size
        self.reset()
    
    def _get_min_row(self) -> int:
        return self._kernel_size
    
    def _get_min_col(self) -> int:
        return self._kernel_size
    
    def _get_max_row(self) -> int:
        return self._grid_size - 1 - self._kernel_size
    
    def _get_max_col(self) -> int:
        return self._grid_size - 1 - self._kernel_size
