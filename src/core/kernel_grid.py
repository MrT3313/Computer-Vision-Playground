from PySide6.QtCore import QObject, Signal


class KernelGridModel(QObject):
    grid_changed = Signal(int, list)
    
    def __init__(self, size: int):
        super().__init__()
        self._size = size
        self._grid_data = self._create_grid(size)
    
    def _create_grid(self, size: int) -> list[list[float]]:
        return [[1.0 for _ in range(size)] for _ in range(size)]
    
    def set_grid_size(self, size: int) -> None:
        self._size = size
        self._grid_data = self._create_grid(size)
        self.grid_changed.emit(size, self._grid_data)
    
    def get_grid_data(self) -> list[list[float]]:
        return self._grid_data
    
    def get_grid_size(self) -> int:
        return self._size
    
    def set_cell(self, row: int, col: int, value: float) -> None:
        if 0 <= row < self._size and 0 <= col < self._size:
            self._grid_data[row][col] = value
            self.grid_changed.emit(self._size, self._grid_data)
    
    def get_value(self, row: int, col: int) -> float:
        if 0 <= row < self._size and 0 <= col < self._size:
            return self._grid_data[row][col]
        return 0.0
    
    def set_all_values(self, value: float) -> None:
        for row in range(self._size):
            for col in range(self._size):
                self._grid_data[row][col] = value
        self.grid_changed.emit(self._size, self._grid_data)