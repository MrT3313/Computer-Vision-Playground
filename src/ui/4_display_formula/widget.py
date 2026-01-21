from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt, QSize
from utils.latex_renderer import render_latex_to_pixmap
from ui.common.title_bar_widget import TitleBarWidget


class FormulaDisplayWidget(QFrame):
    def __init__(self):
        super().__init__()
        # Store the current filter selection (e.g., "Mean", "Custom", etc.)
        self._filter_selection = "Mean"
        # Store the current filter type (e.g., "Cross-Correlation", "Convolution")
        self._filter_type = "Cross-Correlation"
        # Store the current filter category (e.g., "Linear", "Non-Linear")
        self._filter_category = "Linear"
        self._setup_ui()
    
    def _setup_ui(self):
        # Configure the frame's visual appearance with a box border
        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(2)  # Set border thickness to 2 pixels
        
        # Create the main vertical layout that will contain all child widgets
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)  # Remove padding around edges
        main_layout.setSpacing(0)  # Remove spacing between child widgets
        
        title_bar = TitleBarWidget("4. Display Formula")
        
        # Create the content area widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 10, 10, 10)  # Add 10px padding on all sides
        
        # Create label to display the rendered formula image
        self._formula_label = QLabel()
        self._formula_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the formula image
        content_layout.addWidget(self._formula_label)
        
        # Create vertical container for variable key rows
        self._variable_key_container = QWidget()
        self._variable_key_container_layout = QVBoxLayout(self._variable_key_container)
        self._variable_key_container_layout.setContentsMargins(0, 5, 0, 0)
        self._variable_key_container_layout.setSpacing(5)
        self._first_row_widget = None
        self._second_row_widget = None
        self._setup_variable_key()
        content_layout.addWidget(self._variable_key_container)
        
        # Add both the title bar and content area to the main layout
        main_layout.addWidget(title_bar)  # Title bar at the top
        main_layout.addWidget(content_widget, 1)  # Content area below with stretch factor 1
        
        # Render the initial formula
        self._render_formula()
    
    def set_filter(self, filter_name: str) -> None:
        # Update the filter selection and re-render the corresponding formula
        self._filter_selection = filter_name
        self._render_formula()
    
    def set_filter_type(self, filter_type: str) -> None:
        # Update the filter type and re-render the corresponding formula
        self._filter_type = filter_type
        self._render_formula()
    
    def set_category(self, category: str) -> None:
        # Update the filter category and update the variable key
        self._filter_category = category
        self._update_variable_key()

    
    def _render_formula(self) -> None:
        # Generate the appropriate LaTeX formula based on filter selection
        if self._filter_selection == "Mean":
            formula = self._create_mean_formula()
        elif self._filter_selection == "Gaussian":
            # Gaussian filter always uses cross-correlation (implementation doesn't support filter_type)
            formula = self._create_gaussian_formula()
        elif self._filter_selection == "Custom":
            formula = self._create_custom_formula()
        elif self._filter_selection == "Median":
            formula = self._create_median_formula()
        else:
            # Fallback message for unsupported filter types
            formula = "No formula available"
        
        pixmap = render_latex_to_pixmap(formula)
        self._formula_label.setPixmap(pixmap)
    
    def _create_mean_formula(self) -> str:
        # Return the LaTeX string for the mean filter formula
        # G(i,j) = output pixel at position (i,j)
        # (2k+1)^2 = kernel area (total number of elements)
        # F(u+i, v+j) = input pixel values within kernel window
        return r'$G(i,j) = \frac{1}{(2k + 1)^2} \sum_{u=-k}^{k} \,\, \sum_{v=-k}^{k} F(u+i, v+j)$'
    
    def _create_gaussian_formula(self) -> str:
        # Return the LaTeX string for the Gaussian filter formula
        # Gaussian filter always uses cross-correlation (symmetric kernels make convolution equivalent)
        return r'$G(i, j) = \sum_{u=-k}^{k} \,\, \sum_{v=-k}^{k} H(u, v) \cdot F(i + u, j + v)$'
    
    def _create_custom_formula(self) -> str:
        # Return the LaTeX string for the custom filter formula
        # Different formula based on Cross-Correlation vs Convolution
        if self._filter_type == "Convolution":
            # Convolution: G(i,j) = sum H(u,v) F(i-u, j-v)
            return r'$G(i, j) = \sum_{u=-k}^{k} \,\, \sum_{v=-k}^{k} H(u, v) \cdot F(i - u, j - v)$'
        else:
            # Cross-Correlation: G(i,j) = sum H(u,v) F(i+u, j+v)
            return r'$G(i, j) = \sum_{u=-k}^{k} \,\, \sum_{v=-k}^{k} H(u, v) \cdot F(i + u, j + v)$'
    
    def _create_median_formula(self) -> str:
        # Return the LaTeX string for the custom filter formula
        return r'$G(i, j) = \operatorname{med}_{(u,v) \in W} \, F(i+u, j+v)$'
    
    def _setup_variable_key(self) -> None:
        self._update_variable_key()
    
    def _update_variable_key(self) -> None:
        # Remove existing rows if they exist
        if self._first_row_widget is not None:
            self._variable_key_container_layout.removeWidget(self._first_row_widget)
            self._first_row_widget.deleteLater()
        if self._second_row_widget is not None:
            self._variable_key_container_layout.removeWidget(self._second_row_widget)
            self._second_row_widget.deleteLater()
        
        # Create first row with F, G, H or W
        first_row = QWidget()
        first_row_layout = QHBoxLayout(first_row)
        first_row_layout.setContentsMargins(0, 0, 0, 0)
        first_row_layout.setSpacing(15)
        first_row_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        if self._filter_category == "Non-Linear":
            first_row_variables = [
                ("F", "Input (original) image"),
                ("G", "Output (filtered) image"),
                ("W", "Kernel window (for non-weighted operations)")
            ]
        else:
            first_row_variables = [
                ("F", "Input (original) image"),
                ("G", "Output (filtered) image"),
                ("H", "Kernel weights (for weighted operations)")
            ]
        
        for i, (variable, meaning) in enumerate(first_row_variables):
            label = QLabel()
            label.setText(f"<b>{variable}</b>: {meaning}")
            label.setStyleSheet("color: white; font-size: 11px;")
            first_row_layout.addWidget(label)
            
            if i < len(first_row_variables) - 1:
                separator = QLabel("|")
                separator.setStyleSheet("color: #666; font-size: 11px;")
                first_row_layout.addWidget(separator)
        
        self._first_row_widget = first_row
        self._variable_key_container_layout.addWidget(first_row)
        
        # Create second row with i, j, u, v, k
        second_row = QWidget()
        second_row_layout = QHBoxLayout(second_row)
        second_row_layout.setContentsMargins(0, 0, 0, 0)
        second_row_layout.setSpacing(15)
        second_row_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        second_row_variables = [
            ("i, j", "Current pixel position (what you are computing)"),
            ("u, v", "Kernel offset from center (-k to +k)"),
            ("k", "Kernel radius (half the kernel size)")
        ]
        
        for i, (variable, meaning) in enumerate(second_row_variables):
            label = QLabel()
            label.setText(f"<b>{variable}</b>: {meaning}")
            label.setStyleSheet("color: white; font-size: 11px;")
            second_row_layout.addWidget(label)
            
            if i < len(second_row_variables) - 1:
                separator = QLabel("|")
                separator.setStyleSheet("color: #666; font-size: 11px;")
                second_row_layout.addWidget(separator)
        
        self._second_row_widget = second_row
        self._variable_key_container_layout.addWidget(second_row)
    
    def sizeHint(self) -> QSize:
        # Return the preferred size for this widget
        return QSize(600, 80)
