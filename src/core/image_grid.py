from PySide6.QtCore import QObject, Signal


class ImageGridModel(QObject):
    grid_changed = Signal(int, list)
    
    def __init__(self, size: int, initial_value: int | None = 255):
        super().__init__()
        self._size = size
        self._initial_value = initial_value
        self._grid_data = self._create_grid(size, initial_value)
    
    def _create_grid(self, size: int, initial_value: int | None = 255) -> list[list[int | None]]:
        return [[initial_value for _ in range(size)] for _ in range(size)]
    
    def set_grid_size(self, size: int) -> None:
        self._size = size
        self._grid_data = self._create_grid(size, self._initial_value)
        self.grid_changed.emit(size, self._grid_data)
    
    def get_grid_data(self) -> list[list[int | None]]:
        return self._grid_data
    
    def get_grid_size(self) -> int:
        return self._size
    
    def set_cell(self, row: int, col: int, value: int | None) -> None:
        if 0 <= row < self._size and 0 <= col < self._size:
            self._grid_data[row][col] = value
            self.grid_changed.emit(self._size, self._grid_data)
    
    def clear_grid(self) -> None:
        self._grid_data = self._create_grid(self._size, None)
        self.grid_changed.emit(self._size, self._grid_data)
    
    def set_grid_data(self, size: int, grid_data: list[list[int]]) -> None:
        self._size = size
        self._grid_data = grid_data
        self.grid_changed.emit(self._size, self._grid_data)