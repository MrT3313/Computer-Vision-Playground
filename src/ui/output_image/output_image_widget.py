from src.core.image_data import ImageData
from src.ui.common.pixel_grid_base import PixelGridBase


class OutputImageWidget(PixelGridBase):
    def __init__(self, image_data: ImageData, parent=None, cell_size: int = 20):
        super().__init__(
            image_data=image_data,
            show_values=False,
            parent=parent,
            cell_size=cell_size
        )
