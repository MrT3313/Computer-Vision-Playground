from src.core.image_data import ImageData
from src.ui.common.pixel_grid_base import PixelGridBase
from src.consts.defaults import DEFAULT_IMAGE_GRID_CELL_SIZE


class ComputedPixelValuesWidget(PixelGridBase):
    def __init__(self, image_data: ImageData, parent=None, cell_size: int = DEFAULT_IMAGE_GRID_CELL_SIZE):
        super().__init__(
            image_data=image_data,
            show_values=True,
            parent=parent,
            cell_size=cell_size
        )
