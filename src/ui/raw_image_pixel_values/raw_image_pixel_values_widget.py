from src.core.image_data import ImageData
from src.ui.common.pixel_grid_base import PixelGridBase


class RawImagePixelValuesWidget(PixelGridBase):
    def __init__(self, image_data: ImageData, parent=None, cell_size: int = 20):
        super().__init__(
            image_data=image_data,
            show_values=True,
            parent=parent,
            cell_size=cell_size
        )
