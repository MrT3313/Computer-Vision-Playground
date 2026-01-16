from PySide6.QtWidgets import QInputDialog


def show_number_input_dialog(
    parent,
    title: str,
    label: str,
    current_value: float,
    min_value: float,
    max_value: float,
    decimals: int = 2
) -> tuple[float, bool]:
    value, ok = QInputDialog.getDouble(
        parent,
        title,
        label,
        current_value,
        min_value,
        max_value,
        decimals
    )
    
    return value, ok
